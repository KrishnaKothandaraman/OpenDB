from datetime import datetime
from typing import List, Dict, Any

from src.app.models.pricing_data_model import PricingData
from sqlalchemy.orm import Session
from sqlalchemy import update, case, literal, Engine, select, func


class PricingDataRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_pricing_data(self, sku, activate_pricing_tool, bm_listing_id, model_name, bm_listing_quantity,
                            rf_listing_quantity, update_time, bm_minimum_price, bm_selling_price, rf_minimum_price,
                            rf_selling_price, rf_buybox_state, rf_buybox_price, rf_suggested_buybox_price,
                            grab_rf_buybox):
        with self.engine.connect() as conn:
            session = Session(conn)
            activate_pricing_tool = True if activate_pricing_tool == "Yes" else False
            grab_rf_buybox = True if grab_rf_buybox == "Yes" else False

            # parse String of format dd/mm/yyyy hh:mm:ss to datetime object
            update_time = datetime.strptime(update_time, "%d/%m/%Y %H:%M:%S")

            pricing_data = PricingData(sku=sku, activate_pricing_tool=activate_pricing_tool, bm_listing_id=bm_listing_id,
                                       model_name=model_name,
                                       bm_listing_quantity=bm_listing_quantity, rf_listing_quantity=rf_listing_quantity,
                                       update_time=update_time,
                                       bm_minimum_price=bm_minimum_price, bm_selling_price=bm_selling_price,
                                       rf_minimum_price=rf_minimum_price, rf_selling_price=rf_selling_price,
                                       rf_buybox_state=rf_buybox_state, rf_buybox_price=rf_buybox_price,
                                       rf_suggested_buybox_price=rf_suggested_buybox_price,
                                       grab_rf_buybox=grab_rf_buybox)
            session.add(pricing_data)
            session.commit()
            session.close()

    def batch_update_pricing_data(self, updates):
        with self.engine.connect() as conn:
            session = Session(conn)
            print(f"updates: {updates}")
            # create a reverse mapping for updates where each column name is mapped to a here each column name is mapped
            # to a tuple of (sku, new_value)
            # e.g. {"bm_minimum_price": [("sku1", 10.0), ("sku2", 20.0)]}
            # this is needed to construct the case statement
            col_name_to_sku_new_value = {}
            for sku, new_values in updates.items():
                for col_name, new_value in new_values.items():
                    if col_name not in col_name_to_sku_new_value:
                        col_name_to_sku_new_value[col_name] = []
                    col_name_to_sku_new_value[col_name].append((sku, new_value))

            # construct set statement for each key in col_name_to_sku_new_value e.g. set column_name = case when sku =
            # sku1 then 10.0 when sku = sku2 then 20.0 end, set column2 = case when sku = sku1 then 10.0 when sku = sku2
            # then 20.0 end Construct the CASE statements for each column and SKU
            set_statements = {}
            for col, sku_new_values in col_name_to_sku_new_value.items():
                cases = [
                    (
                        PricingData.sku == sku,
                        literal(new_value)
                    )
                    for sku, new_value in sku_new_values]
                case_stmt = case(
                    *cases,
                    else_="NULL")
                set_statements[getattr(PricingData, col)] = case_stmt
                # create set statement for each column

            update_statement = update(PricingData). \
                where(PricingData.sku.in_(updates.keys())). \
                values(set_statements)

            session.execute(update_statement)
            session.commit()
            session.close()

    def update_pricing_data(self, sku, new_values):
        with self.engine.connect() as conn:
            session = Session(bind=conn)
            # Construct update query
            update_query = PricingData.__table__.update().where(PricingData.sku == sku)
            for col_name, new_value in new_values.items():
                update_query = update_query.values({col_name: new_value})
            # Execute update query
            session.execute(update_query)
            session.commit()
            session.close()

    def delete_pricing_data(self, sku):
        with self.engine.connect() as conn:
            session = Session(bind=conn)
            session.query(PricingData).filter_by(sku=sku).delete()
            session.commit()

    def create_pricing_data(self, sku):
        with self.engine.connect() as conn:
            session = Session(bind=conn)
            session.add(PricingData(sku=sku, activate_pricing_tool=True))
            session.commit()
            session.close()

    def get_data(self, filters: Dict[str, Any] = None):
        with self.engine.connect() as conn:
            if not filters:
                # select pricing data order by swd_stock + rf_listing_quantity desc
                stmt = select(PricingData).order_by(PricingData.rf_listing_quantity.desc())
            else:
                stmt = select(PricingData).where(
                    *[(getattr(PricingData, col) == value) for col, value in filters.items()])\
                    .order_by(PricingData.rf_listing_quantity.desc())

            session = Session(bind=conn)

            result = session.execute(stmt).scalars().all()
            session.close()

        return result

    def handle_sales(self, sales):
        print(sales)
        with self.engine.connect() as conn:
            session = Session(bind=conn)
            for sale in sales:
                sku = sale["sku"]
                quantity = sale["quantity"]
                stmt = PricingData.__table__.update().where(PricingData.sku == sku).values(
                    {"swd_stock": PricingData.swd_stock - quantity})
                session.execute(stmt)
            session.commit()
            session.close()

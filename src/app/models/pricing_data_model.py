from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class PricingData(Base):
    __tablename__ = 'pricing_data'

    sku = Column(String(20), primary_key=True)
    activate_pricing_tool = Column(Boolean, nullable=False, default=False)
    bm_listing_id = Column(String(20))
    model_name = Column(String(150))

    bm_listing_quantity = Column(Integer)
    rf_listing_quantity = Column(Integer)
    update_time = Column(DateTime)
    bm_minimum_price = Column(Float)
    bm_selling_price = Column(Float)
    rf_minimum_price = Column(Float)
    rf_selling_price = Column(Float)
    rf_buybox_state = Column(String(25))
    rf_buybox_price = Column(Float)
    rf_suggested_buybox_price = Column(Float)
    grab_rf_buybox = Column(Boolean, default=False)

    @hybrid_property
    def total_quantity(self):
        # check if listing_quantity is not none and return the sum of both else return 0
        return self.bm_listing_quantity + self.rf_listing_quantity if self.bm_listing_quantity and self.rf_listing_quantity else 0

    def get_col_name(self, col) -> str:
        print(col)
        # return column name of the given column
        if col == "SKU":
            return "sku"
        if col == "Activate Pricing Tool":
            return "activate_pricing_tool"
        if col == "BM Listing ID":
            return "bm_listing_id"
        if col == "Model Name":
            return "model_name"
        if col == "BM Listing Quantity":
            return "bm_listing_quantity"
        if col == "RF Listing Quantity":
            return "rf_listing_quantity"
        if col == "Update Time":
            return "update_time"
        if col == "BM Minimum Price":
            return "bm_minimum_price"
        if col == "BM Selling Price":
            return "bm_selling_price"
        if col == "RF Minimum Price":
            return "rf_minimum_price"
        if col == "RF Selling Price":
            return "rf_selling_price"
        if col == "RF Buybox State":
            return "rf_buybox_state"
        if col == "RF Buybox Price":
            return "rf_buybox_price"
        if col == "RF Suggested Buybox Price":
            return "rf_suggested_buybox_price"
        if col == "Grab RF Buybox":
            return "grab_rf_buybox"

    def get_data_as_list(self):
        return list(map(
            lambda x: self.get_str(x),
            [
                self.sku,
                self.activate_pricing_tool,
                self.bm_listing_id,
                self.model_name,
                self.total_quantity,
                self.bm_listing_quantity,
                self.rf_listing_quantity,
                self.update_time,
                self.bm_minimum_price,
                self.bm_selling_price,
                self.rf_minimum_price,
                self.rf_selling_price,
                self.rf_buybox_state,
                self.rf_buybox_price,
                self.rf_suggested_buybox_price,
                self.grab_rf_buybox
            ]))

    def to_dict(self):
        return {
            "sku": self.sku,
            "activate_pricing_tool": self.activate_pricing_tool,
            "bm_listing_id": self.bm_listing_id,
            "model_name": self.model_name,
            "total_quantity": self.total_quantity,
            "bm_listing_quantity": self.bm_listing_quantity,
            "rf_listing_quantity": self.rf_listing_quantity,
            "update_time": self.update_time,
            "bm_minimum_price": self.bm_minimum_price,
            "bm_selling_price": self.bm_selling_price,
            "rf_minimum_price": self.rf_minimum_price,
            "rf_selling_price": self.rf_selling_price,
            "rf_buybox_state": self.rf_buybox_state,
            "rf_buybox_price": self.rf_buybox_price,
            "rf_suggested_buybox_price": self.rf_suggested_buybox_price,
            "grab_rf_buybox": self.grab_rf_buybox
        }
    @staticmethod
    def get_str(string) -> str:
        # if string is of type str return it
        if isinstance(string, str):
            return string
        # if string is datetime return it formatted in dd/mm/yyyy HH:MM:SS
        if isinstance(string, datetime):
            return string.strftime("%d/%m/%Y %H:%M:%S")
        # if string is boolean return "Yes" or "No"
        if isinstance(string, bool):
            return "Yes" if string else "No"
        # if string is None return empty string
        if string is None:
            return ""
        # if string is of any other type return it as string
        return str(string)


from flask_sqlalchemy.query import Query

from src.app.repositories.pricing_data_repository import PricingDataRepository
from src.app.validators.pricing_data_validator import PricingDataValidator


class PricingDataService:
    def __init__(self, pool):
        self.repository = PricingDataRepository(pool)
        self.validator = PricingDataValidator()

    def create_pricing_data(self, data):
        try:
            self.validator.validate_create_pricing_data(data)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))

        sku = data["sku"]
        return self.repository.create_pricing_data(sku)

    def insert_pricing_data(self, data):
        try:
            self.validator.validate_insert_pricing_data(data)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))

        return self.repository.insert_pricing_data(
            sku=data["sku"],
            activate_pricing_tool=data["activate_pricing_tool"],
            bm_listing_id=data["bm_listing_id"],
            model_name=data["model_name"],
            bm_listing_quantity=data["bm_listing_quantity"],
            rf_listing_quantity=data["rf_listing_quantity"],
            update_time=data["update_time"],
            bm_minimum_price=data["bm_minimum_price"],
            bm_selling_price=data["bm_selling_price"],
            rf_minimum_price=data["rf_minimum_price"],
            rf_selling_price=data["rf_selling_price"],
            rf_buybox_state=data["rf_buybox_state"],
            rf_buybox_price=data["rf_buybox_price"],
            rf_suggested_buybox_price=data["rf_suggested_buybox_price"],
            grab_rf_buybox=data["grab_rf_buybox"]
        )

    def batch_update_pricing_data(self, data):
        try:
            self.validator.validate_batch_update_pricing_data(data)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))

        # concvert data from the format of {"updates": [{"sku": string, "new_values": {field_name: field_val}}]} to
        # {<sku>: {<field_name>: <field_val>}}
        data = {item["sku"]: item["new_values"] for item in data["updates"]}

        return self.repository.batch_update_pricing_data(data)

    def update_pricing_data(self, json_data):
        try:
            self.validator.validate_update_pricing_data(json_data)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))
        sku = json_data["sku"]
        new_values = json_data["new_values"]
        return self.repository.update_pricing_data(sku, new_values)

    def delete_pricing_data(self, data):
        """Support both single SKU and multiple SKUs for deletion"""
        try:
            # Support both formats: {"sku": "ABC"} or {"skus": ["ABC", "DEF"]}
            if isinstance(data, dict):
                if "skus" in data and isinstance(data["skus"], list):
                    skus = data["skus"]
                else:
                    skus = [data.get("sku")]
            elif isinstance(data, list):
                skus = data
            else:
                skus = [data]

            skus = [str(s).strip() for s in skus if s]

            if not skus:
                raise ValueError("No valid SKUs provided for deletion")

            logger.info(f"Deleting {len(skus)} SKUs: {skus}")

            results = []
            for sku in skus:
                try:
                    result = self.repository.delete_pricing_data(sku)
                    results.append({"sku": sku, "status": "success"})
                except Exception as e:
                    logger.error(f"Failed to delete {sku}: {e}")
                    results.append({"sku": sku, "status": "failed", "error": str(e)})

            return {
                "deleted_count": len([r for r in results if r["status"] == "success"]),
                "results": results
            }

        except Exception as e:
            logger.exception("Delete failed in PricingDataService")
            raise

    def get_data(self, filters):
        try:
            self.validator.validate_get_pricing_data(filters)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))

        res = self.repository.get_data(filters["filter"])
        # return res in the form of [{field_name: field_val}]
        return [item.to_dict_with_metadata() for item in res]

    def handle_sales(self, sales):
        try:
            self.validator.validate_handle_sales(sales)
            sales = sales["sales"]
            self.repository.handle_sales(sales)
        except Exception as e:
            raise ValueError("Invalid JSON format: " + str(e))


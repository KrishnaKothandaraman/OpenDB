import unittest
from src.app.validators.pricing_data_validator import PricingDataValidator


class TestPricingDataValidator(unittest.TestCase):
    def test_validate_create_pricing_data_no_sku(self):
        with self.assertRaises(ValueError):
            PricingDataValidator.validate_create_pricing_data(
                {}
            )

    def test_validate_create_pricing_data_integer_sku(self):
        with self.assertRaises(ValueError):
            PricingDataValidator.validate_create_pricing_data(
                {
                    "sku": 123,
                }
            )

    def test_validate_create_pricing_data_with_additional_fields_raises_error(self):

        data = {
            "sku": "123",
            "additional_fields": {
                "activate_pricing_tool": True,
                "bm_listing_id": "123345",
                "model_name": "iPhone 14 Pro EUS 256",
                "bm_listing_quantity": 0,
                "rf_listing_quantity": 0,
                "update_time": "2021-09-01T00:00:00+00:00",
                "bm_minimum_price": 0.0,
                "bm_selling_price": 0.0,
                "rf_minimum_price": 0.0,
                "rf_selling_price": 0.0,
                "rf_buybox_state": "New",
                "rf_buybox_price": 0.0,
                "rf_suggested_buybox_price": 0.0,
                "grab_rf_buybox": True
            }
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_create_pricing_data, data)

    def test_validate_create_pricing_data_with_no_error(self):

        data = {
            "sku": "123",
        }
        try:
            PricingDataValidator.validate_create_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in create pricing data validation")

    def test_insert_pricing_data_no_sku_raises_error(self):
        data = {
            "activate_pricing_tool": True,
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_insert_pricing_data, data)

    def test_insert_pricing_data_no_error(self):
        data = {
            "sku": "123",
            "activate_pricing_tool": True,
            "bm_listing_id": "123345",
            "model_name": "iPhone 14 Pro EUS 256",
            "bm_listing_quantity": 0,
            "rf_listing_quantity": 0,
            "update_time": "2021-09-01T00:00:00+00:00",
            "bm_minimum_price": 0.0,
            "bm_selling_price": 0.0,
            "rf_minimum_price": 0.0,
            "rf_selling_price": 0.0,
            "rf_buybox_state": "New",
            "rf_buybox_price": 0.0,
            "rf_suggested_buybox_price": 0.0,
            "grab_rf_buybox": True
        }
        try:
            PricingDataValidator.validate_insert_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in insert pricing data validation")

    def test_validate_insert_pricing_data_integer_sku(self):
        data = {
            "sku": 123,
            "activate_pricing_tool": True,
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_insert_pricing_data, data)

    def test_validate_insert_pricing_data_missing_fields_raises_error(self):
        data = {
            "sku": "123",
            "activate_pricing_tool": True,
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_insert_pricing_data, data)

    def test_validate_update_pricing_data_no_sku(self):
        with self.assertRaises(ValueError):
            PricingDataValidator.validate_update_pricing_data(
                {
                    "new_values": {}
                }
            )

    def test_validate_update_pricing_data_integer_sku(self):
        with self.assertRaises(ValueError):
            PricingDataValidator.validate_update_pricing_data(
                {
                    "sku": 123,
                    "new_values": {}
                }
            )

    def test_validate_update_pricing_data_with_additional_fields_raises_no_error(self):

        data = {
            "sku": "123",
            "new_values": {
                "activate_pricing_tool": True,
                "bm_listing_id": "123345",
                "model_name": "iPhone 14 Pro EUS 256",
                "bm_listing_quantity": 0,
                "rf_listing_quantity": 0,
                "update_time": "2021-09-01T00:00:00+00:00",
                "bm_minimum_price": 0.0,
                "bm_selling_price": 0.0,
                "rf_minimum_price": 0.0,
                "rf_selling_price": 0.0,
                "rf_buybox_state": "New",
                "rf_buybox_price": 0.0,
                "rf_suggested_buybox_price": 0.0,
                "grab_rf_buybox": True
            }
        }
        try:
            PricingDataValidator.validate_update_pricing_data(data)
        except ValueError:
            self.fail("validate_update_pricing_data raised ValueError unexpectedly!")

    def test_delete_pricing_data_no_sku_raises_error(self):
        data = {}
        self.assertRaises(ValueError, PricingDataValidator.validate_delete_pricing_data, data)

    def test_delete_pricing_data_integer_sku_raises_error(self):
        data = {
            "sku": 123
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_delete_pricing_data, data)

    def test_delete_pricing_data_additional_fields_raises_error(self):
        data = {
            "sku": "123",
            "activate_pricing_tool": True,
            "bm_listing_id": "123345",
            "model_name": "iPhone 14 Pro EUS 256",
            "bm_listing_quantity": 0,
            "rf_listing_quantity": 0,
            "update_time": "2021-09-01T00:00:00+00:00",
            "bm_minimum_price": 0.0,
            "bm_selling_price": 0.0,
            "rf_minimum_price": 0.0,
            "rf_selling_price": 0.0,
            "rf_buybox_state": "New",
            "rf_buybox_price": 0.0,
            "rf_suggested_buybox_price": 0.0,
            "grab_rf_buybox": True
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_delete_pricing_data, data)

    def test_delete_pricing_data_raises_no_error(self):
        data = {
            "sku": "123"
        }
        try:
            PricingDataValidator.validate_delete_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in delete pricing data validation")

    def test_validate_get_data_with_no_filter_raises_error(self):
        data = {}
        self.assertRaises(ValueError, PricingDataValidator.validate_get_pricing_data, data)

    def test_validate_get_data_with_filter_raises_no_error(self):
        data = {
            "filter": {
                "sku": "123"
            }
        }
        try:
            PricingDataValidator.validate_get_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in get pricing data validation")

    def test_validate_batch_update_with_no_sku_raises_error(self):
        data = {
            "new_values": {}
        }
        self.assertRaises(ValueError, PricingDataValidator.validate_batch_update_pricing_data, data)

    def test_validate_batch_update_with_single_sku_raises_no_error(self):
        data = {
            "updates": [
                {
                    "sku": "123",
                    "new_values": {
                        "activate_pricing_tool": True,
                    }
                }
            ]
        }
        try:
            PricingDataValidator.validate_batch_update_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in batch update pricing data validation")

    def test_validate_batch_update_with_multiple_skus_no_error(self):
        data = {
            "updates": [
                {
                    "sku": "123",
                    "new_values": {
                        "activate_pricing_tool": True,
                    }
                },
                {
                    "sku": "456",
                    "new_values": {
                        "activate_pricing_tool": True,
                    }
                }
            ]
        }
        try:
            PricingDataValidator.validate_batch_update_pricing_data(data)
        except ValueError:
            self.fail("Unexpected ValueError in batch update pricing data validation")
import unittest
from unittest.mock import MagicMock, patch
from src.app.services.pricing_data_service import PricingDataService


class PricingDataServiceTests(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.data_service = PricingDataService(self.mock_session)

    def test_create_pricing_data_valid(self):
        data = {
            "sku": "ABC123",
            "additional_fields": {
                "activate_pricing_tool": False,
                "bm_listing_id": "123456",
                "model_name": "Product Model",
                "bm_listing_quantity": 10,
                "rf_listing_quantity": 20,
                "update_time": "2023-05-25T10:00:00Z",
                "bm_minimum_price": 9.99,
                "bm_selling_price": 19.99,
                "rf_minimum_price": 29.99,
                "rf_selling_price": 39.99,
                "rf_buybox_state": "Active",
                "rf_buybox_price": 49.99,
                "rf_suggested_buybox_price": 59.99,
                "grab_rf_buybox": True
            }
        }

        with patch.object(self.data_service.validator, "validate_create_pricing_data"):
            with patch.object(self.data_service.repository, "create_pricing_data") as mock_create_pricing_data:
                result = self.data_service.create_pricing_data(data)

        mock_create_pricing_data.assert_called_once_with("ABC123")
        self.assertEqual(result, mock_create_pricing_data.return_value)

    def test_create_pricing_data_invalid(self):
        data = {
            "notsku": "ABC123",
        }

        with patch.object(self.data_service.validator, "validate_create_pricing_data") as mock_validate:
            mock_validate.side_effect = Exception("Invalid JSON format")
            with patch.object(self.data_service.repository, "create_pricing_data") as mock_create_pricing_data:
                with self.assertRaises(ValueError):
                    self.data_service.create_pricing_data(data)

    def test_insert_pricing_data_valid(self):
        data = {
            "sku": "ABC123",
            "activate_pricing_tool": False,
            "bm_listing_id": "123456",
            "model_name": "Product Model",
            "bm_listing_quantity": 10,
            "rf_listing_quantity": 20,
            "update_time": "2023-05-25T10:00:00Z",
            "bm_minimum_price": 9.99,
            "bm_selling_price": 19.99,
            "rf_minimum_price": 29.99,
            "rf_selling_price": 39.99,
            "rf_buybox_state": "Active",
            "rf_buybox_price": 49.99,
            "rf_suggested_buybox_price": 59.99,
            "grab_rf_buybox": True
        }

        with patch.object(self.data_service.validator, "validate_insert_pricing_data"):
            with patch.object(self.data_service.repository, "insert_pricing_data") as mock_insert_pricing_data:
                result = self.data_service.insert_pricing_data(data)

        mock_insert_pricing_data.assert_called_once_with(
            sku="ABC123",
            activate_pricing_tool=False,
            bm_listing_id="123456",
            model_name="Product Model",
            bm_listing_quantity=10,
            rf_listing_quantity=20,
            update_time="2023-05-25T10:00:00Z",
            bm_minimum_price=9.99,
            bm_selling_price=19.99,
            rf_minimum_price=29.99,
            rf_selling_price=39.99,
            rf_buybox_state="Active",
            rf_buybox_price=49.99,
            rf_suggested_buybox_price=59.99,
            grab_rf_buybox=True
        )

        # Assert the result
        self.assertEqual(result, mock_insert_pricing_data.return_value)

    def test_update_pricing_data_valid(self):
        updates = {
            "sku": "ABC123",
            "new_values": {
                "activate_pricing_tool": True,
                "bm_listing_id": "123456",
                "model_name": "Product Model",
                "bm_listing_quantity": 10,
                "rf_listing_quantity": 20,
                "update_time": "2023-05-25T10:00:00Z",
                "bm_minimum_price": 9.99,
                "bm_selling_price": 19.99,
                "rf_minimum_price": 29.99,
                "rf_selling_price": 39.99,
                "rf_buybox_state": "Active",
                "rf_buybox_price": 49.99,
                "rf_suggested_buybox_price": 59.99,
                "grab_rf_buybox": True
            }
        }

        with patch.object(self.data_service.validator, "validate_update_pricing_data") as mock_validator:
            with patch.object(self.data_service.repository,
                              "update_pricing_data") as mock_update_pricing_data:
                result = self.data_service.update_pricing_data(updates)

        mock_validator.assert_called_once_with(updates)
        mock_update_pricing_data.assert_called_once_with(updates["sku"], updates["new_values"])
        self.assertEqual(result, mock_update_pricing_data.return_value)

    def test_update_pricing_data_invalid(self):
        updates = [
            {
                "sku": "ABC123",
                "new_values": {
                    "activate_pricing_tool": True,
                    "bm_listing_id": "123456",
                    "model_name": "Product Model",
                    "bm_listing_quantity": 10,
                    "rf_listing_quantity": 20,
                    "update_time": "2023-05-25T10:00:00Z",
                    "bm_minimum_price": 9.99,
                    "bm_selling_price": 19.99,
                    "rf_minimum_price": 29.99,
                    "rf_selling_price": 39.99,
                    "rf_buybox_state": "Active",
                    "rf_buybox_price": 49.99,
                    "rf_suggested_buybox_price": 59.99,
                    "grab_rf_buybox": "Invalid"  # Invalid type, should be boolean
                }
            }
        ]

        with patch.object(self.data_service.validator, "validate_update_pricing_data",
                          side_effect=ValueError("Invalid JSON format")) as mock_validator:
            with self.assertRaises(ValueError):
                self.data_service.update_pricing_data(updates)

        mock_validator.assert_called_once_with(updates)

    def test_delete_pricing_data_valid(self):
        data = {
            "sku": "ABC123",
        }

        with patch.object(self.data_service.validator, "validate_delete_pricing_data"):
            with patch.object(self.data_service.repository, "delete_pricing_data") as mock_delete_pricing_data:
                result = self.data_service.delete_pricing_data(data)

        mock_delete_pricing_data.assert_called_once_with("ABC123")
        self.assertEqual(result, mock_delete_pricing_data.return_value)

    def test_delete_pricing_data_invalid(self):
        data = {
            "notsku": "ABC123",
        }

        with patch.object(self.data_service.validator, "validate_delete_pricing_data",
                          side_effect=ValueError("Invalid JSON format")) as mock_validator:
            with self.assertRaises(ValueError):
                self.data_service.delete_pricing_data(data)

        mock_validator.assert_called_once_with(data)

    def test_get_pricing_data_valid(self):
        data = {
            "filter": {
                "sku": "ABC123",
            }
        }

        with patch.object(self.data_service.validator, "validate_get_pricing_data"):
            with patch.object(self.data_service.repository, "get_data") as mock_get_pricing_data:
                result = self.data_service.get_data(data)

        mock_get_pricing_data.assert_called_once_with(data["filter"])
        self.assertEqual(result, mock_get_pricing_data.return_value)

    def test_get_pricing_data_invalid(self):
        data = {
            "filter": {
                "notsku": "ABC123",
            }
        }

        with patch.object(self.data_service.validator, "validate_get_pricing_data",
                          side_effect=ValueError("Invalid JSON format")) as mock_validator:
            with self.assertRaises(ValueError):
                self.data_service.get_data(data)

        mock_validator.assert_called_once_with(data)

    def test_batch_update_valid(self):
        updates = {
            "updates": [
                {
                    "sku": "ABC123",
                    "new_values": {
                        "activate_pricing_tool": True,
                        "bm_listing_id": "123456",
                        "model_name": "Product Model",
                        "bm_listing_quantity": 10,
                        "rf_listing_quantity": 20,
                        "update_time": "2023-05-25T10:00:00Z",
                        "bm_minimum_price": 9.99,
                        "bm_selling_price": 19.99,
                        "rf_minimum_price": 29.99,
                        "rf_selling_price": 39.99,
                        "rf_buybox_state": "Active",
                        "rf_buybox_price": 49.99,
                        "rf_suggested_buybox_price": 59.99,
                        "grab_rf_buybox": True
                    }
                },
                {
                    "sku": "ZYX987",
                    "new_values": {
                        "activate_pricing_tool": True,
                        "bm_listing_id": "123456",
                        "model_name": "Product Model",
                        "bm_listing_quantity": 10,
                        "rf_listing_quantity": 20,
                        "update_time": "2023-05-25T10:00:00Z",
                        "bm_minimum_price": 9.99,
                        "bm_selling_price": 19.99,
                        "rf_minimum_price": 29.99,
                        "rf_selling_price": 39.99,
                        "rf_buybox_state": "Active",
                        "rf_buybox_price": 49.99,
                        "rf_suggested_buybox_price": 59.99,
                        "grab_rf_buybox": True
                    }
                }
            ]
        }

        with patch.object(self.data_service.validator, "validate_batch_update_pricing_data") as mock_validator:
            with patch.object(self.data_service.repository,
                              "batch_update_pricing_data") as mock_batch_update_pricing_data:
                result = self.data_service.batch_update_pricing_data(updates)

        mock_validator.assert_called_once_with(updates)
        expectedCallParam = {item["sku"]: item["new_values"] for item in updates["updates"]}
        mock_batch_update_pricing_data.assert_called_once_with(expectedCallParam)
        self.assertEqual(result, mock_batch_update_pricing_data.return_value)

    def test_batch_update_invalid(self):
        updates = {
            "updates": [
                {
                    "sku": "ABC123",
                    "new_values": {
                        "activate_pricing_tool": "Invalid",  # Invalid type, should be boolean
                        "bm_listing_id": "123456",
                        "model_name": "Product Model",
                        "bm_listing_quantity": 10,
                        "rf_listing_quantity": 20,
                        "update_time": "2023-05-25T10:00:00Z",
                        "bm_minimum_price": 9.99,
                        "bm_selling_price": 19.99,
                        "rf_minimum_price": 29.99,
                        "rf_selling_price": 39.99,
                        "rf_buybox_state": "Active",
                        "rf_buybox_price": 49.99,
                        "rf_suggested_buybox_price": 59.99,
                        "grab_rf_buybox": False
                    }
                }
            ]
        }

        with patch.object(self.data_service.validator, "validate_batch_update_pricing_data",
                          side_effect=ValueError("Invalid JSON format")) as mock_validator:
            with self.assertRaises(ValueError):
                self.data_service.batch_update_pricing_data(updates)

        mock_validator.assert_called_once_with(updates)

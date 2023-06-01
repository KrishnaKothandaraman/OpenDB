from jsonschema import validate, ValidationError


class PricingDataValidator:
    @staticmethod
    def validate_create_pricing_data(data):
        schema = {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
            },
            "required": ["sku"],
            "additionalProperties": False
        }

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

    @staticmethod
    def validate_insert_pricing_data(data):
        schema = {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
                "activate_pricing_tool": {"type": "boolean"},
                "bm_listing_id": {"type": "string", "maxLength": 20},
                "model_name": {"type": "string", "maxLength": 150},
                "bm_listing_quantity": {"type": "integer"},
                "rf_listing_quantity": {"type": "integer"},
                "update_time": {"type": "string", "format": "date-time"},
                "bm_minimum_price": {"type": "number"},
                "bm_selling_price": {"type": "number"},
                "rf_minimum_price": {"type": "number"},
                "rf_selling_price": {"type": "number"},
                "rf_buybox_state": {"type": "string", "maxLength": 25},
                "rf_buybox_price": {"type": "number"},
                "rf_suggested_buybox_price": {"type": "number"},
                "grab_rf_buybox": {"type": "boolean"}
            },
            "required": ["sku", "activate_pricing_tool", "bm_listing_id", "model_name", "bm_listing_quantity",
                         "rf_listing_quantity", "update_time", "bm_minimum_price", "bm_selling_price",
                         "rf_minimum_price", "rf_selling_price", "rf_buybox_state", "rf_buybox_price",
                         "rf_suggested_buybox_price", "grab_rf_buybox"],
            "additionalProperties": False
        }

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

    @staticmethod
    def validate_update_pricing_data(data):
        schema = {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
                "new_values": {
                    "type": "object",
                    "properties": {
                        "activate_pricing_tool": {"type": "boolean"},
                        "bm_listing_id": {"type": "string", "maxLength": 20},
                        "model_name": {"type": "string", "maxLength": 150},
                        "bm_listing_quantity": {"type": "integer"},
                        "rf_listing_quantity": {"type": "integer"},
                        "update_time": {"type": "string", "format": "date-time"},
                        "bm_minimum_price": {"type": "number"},
                        "bm_selling_price": {"type": "number"},
                        "rf_minimum_price": {"type": "number"},
                        "rf_selling_price": {"type": "number"},
                        "rf_buybox_state": {"type": "string", "maxLength": 25},
                        "rf_buybox_price": {"type": "number"},
                        "rf_suggested_buybox_price": {"type": "number"},
                        "grab_rf_buybox": {"type": "boolean"}
                    },
                    "additionalProperties": False
                }
            },
            "required": ["sku", "new_values"],
            "additionalProperties": False
        }

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

    @staticmethod
    def validate_delete_pricing_data(data):
        schema = {
            "type": "object",
            "properties": {
                "sku": {"type": "string"},
            },
            "required": ["sku"],
            "additionalProperties": False
        }

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

    @staticmethod
    def validate_get_pricing_data(data):
        # expected format : {"filter" : {field_name: field_value}}
        schema = {
            "type": "object",
            "properties": {
                "filter": {
                    "type": "object",
                    "properties": {
                        "sku": {"type": "string"},
                        "activate_pricing_tool": {"type": "boolean"},
                        "bm_listing_id": {"type": "string", "maxLength": 20},
                        "model_name": {"type": "string", "maxLength": 150},
                        "bm_listing_quantity": {"type": "integer"},
                        "rf_listing_quantity": {"type": "integer"},
                        "update_time": {"type": "string", "format": "date-time"},
                        "bm_minimum_price": {"type": "number"},
                        "bm_selling_price": {"type": "number"},
                        "rf_minimum_price": {"type": "number"},
                        "rf_selling_price": {"type": "number"},
                        "rf_buybox_state": {"type": "string", "maxLength": 25},
                        "rf_buybox_price": {"type": "number"},
                        "rf_suggested_buybox_price": {"type": "number"},
                        "grab_rf_buybox": {"type": "boolean"}
                    },
                    "additionalProperties": False
                }
            },
            "required": ["filter"],
            "additionalProperties": False
        }

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

    @staticmethod
    def validate_batch_update_pricing_data(data):
        # format : {"updates": [{"sku": string, "new_values": {field_name: field_value}}]}
        schema = {
            "type": "object",
            "properties": {
                "updates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sku": {"type": "string"},
                            "new_values": {
                                "type": "object",
                                "properties": {
                                    "activate_pricing_tool": {"type": "boolean"},
                                    "bm_listing_id": {"type": "string", "maxLength": 20},
                                    "model_name": {"type": "string", "maxLength": 150},
                                    "bm_listing_quantity": {"type": "integer"},
                                    "rf_listing_quantity": {"type": "integer"},
                                    "update_time": {"type": "string", "format": "date-time"},
                                    "bm_minimum_price": {"type": "number"},
                                    "bm_selling_price": {"type": "number"},
                                    "rf_minimum_price": {"type": "number"},
                                    "rf_selling_price": {"type": "number"},
                                    "rf_buybox_state": {"type": "string", "maxLength": 25},
                                    "rf_buybox_price": {"type": "number"},
                                    "rf_suggested_buybox_price": {"type": "number"},
                                    "grab_rf_buybox": {"type": "boolean"}
                                },
                                "additionalProperties": False
                            }
                        },
                        "required": ["sku", "new_values"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["updates"],
        }
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError("Invalid JSON format: " + e.args[0])

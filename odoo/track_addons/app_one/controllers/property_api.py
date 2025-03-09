import json
from odoo.exceptions import ValidationError, UserError
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class PropertyController(http.Controller):

    @http.route("/api/create", methods=["POST"], type="json", auth="public", csrf=False)
    def create_property(self):
        try:

            data_request = request.httprequest.data.decode()
            vals = json.loads(data_request)


            required_fields = ['name', 'postcode', 'expected_price']
            for field in required_fields:
                if field not in vals:
                    raise UserError(f"Missing required field: {field}")


            property_record = request.env['property'].sudo().create(vals)


            if property_record:
                _logger.info(f"Property created successfully with ID {property_record.id}")
                return request.make_json_response({
                    "message": "Property has been created successfully",
                    "property_id": property_record.id
                }, status=201)
            else:
                raise UserError("Failed to create property")

        except json.JSONDecodeError as e:
            _logger.error(f"JSON Decode Error: {e}")
            return request.make_json_response({
                "error": "Invalid JSON data"
            }, status=400)

        except UserError as e:
            _logger.error(f"Validation Error: {e.name}")
            return request.make_json_response({
                "error": e.name,
                "message": str(e)
            }, status=400)

        except Exception as e:
            _logger.exception(f"Unexpected error: {e}")
            return request.make_json_response({
                "error": "Unexpected error occurred",
                "message": str(e)
            }, status=500)

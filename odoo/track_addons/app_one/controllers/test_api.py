from odoo import http
from odoo.http import request
import json



class TestAPI(http.Controller):

    @http.route("/api/test", methods=["GET"], type="http", auth="public", csrf=False)
    def test(self):

        return "Test API Working"

    @http.route("/v1/create/", methods=["POST"], type="http", auth="public", csrf=False)
    def create(self):
        data_request = request.httprequest.data.decode()
        vals = json.loads(data_request)

        return json.dumps({"status": "success", "data": vals})



from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response

class ExpenseCategoryAPI(http.Controller):

    @http.route('/api/easy_apps/categories', type='http', auth='public', methods=['GET'], csrf=False)
    def get_categories(self, **kwargs):
        """Retrieve all expense categories (JWT required)"""
        try:
            # Validate JWT
            JWTAuth.authenticate_request()  # Will raise AccessDenied if invalid

            # Fetch categories
            categories = request.env['easy_expenses.category'].sudo().search([])

            return _http_success_response(
                [{'id': cat.id, 'name': cat.name, 'description': cat.description} for cat in categories],
                "Categories retrieved successfully"
            )
        except AccessDenied as e:
            return _http_error_response(str(e), 401)  # Convert Odoo AccessDenied into JSON response
        except Exception as e: 
            return _http_error_response(f"Error getting categories: {str(e)}", 500)  # Log other errors

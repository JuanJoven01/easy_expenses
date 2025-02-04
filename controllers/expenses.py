from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response

class ExpenseAPI(http.Controller):

    @http.route('/api/easy_apps/expenses', type='http', auth='public', methods=['GET'], csrf=False)
    @http.route('/api/easy_apps/expenses/<int:category_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_expenses(self, category_id=None, **kwargs):
        """Retrieve all expenses or filter by category (JWT required)"""
        try:
            # Validate JWT
            JWTAuth.authenticate_request()  # Will raise AccessDenied if invalid

            domain = [('category_id', '=', category_id)] if category_id else []

            # Fetch expenses
            expenses = request.env['easy_expenses.expense'].sudo().search(domain)

            return _http_success_response(
                [{'id': exp.id, 'name': exp.name, 'category_id': exp.category_id.id, 'category_name': exp.category_id.name}
                 for exp in expenses],
                "Expenses retrieved successfully"
            )
        except AccessDenied as e:
            return _http_error_response(str(e), 401)  # Convert Odoo AccessDenied into JSON response
        except Exception as e:
            return _http_error_response(f"Error getting expenses: {str(e)}", 500)  # Log other errors

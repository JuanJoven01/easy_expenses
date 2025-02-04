from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response


class UserExpenseAPI(http.Controller):

    ## 🔹 [GET] Retrieve User Expenses (Filtered by Category if Provided)
    @http.route('/api/easy_apps/user_expenses/category', type='http', auth='public', methods=['GET'], csrf=False)
    @http.route('/api/easy_apps/user_expenses/category/<int:category_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_expenses_by_category(self, category_id=None, **kwargs):
        """Retrieve user expenses filtered by category, or all if none provided (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            # If category_id is provided, filter by category; otherwise, get all
            domain = [('user_id', '=', user_id)]
            if category_id:
                domain.append(('category_id', '=', category_id))

            expenses = request.env['easy_expenses.user_expense'].sudo().search(domain)

            return _http_success_response(
                [{'id': exp.id, 'name': exp.name, 'category_id': exp.category_id.id, 'category_name': exp.category_id.name}
                for exp in expenses],
                "User Expenses retrieved successfully"
            )
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error getting user expenses: {str(e)}", 500)

    ## 🔹 [POST] Create a User Expense
    @http.route('/api/easy_apps/user_expenses/create', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def create_user_expense(self, **kwargs):
        """Create a new user expense (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            name = kwargs.get("name")
            category_id = kwargs.get("category_id")

            if not name or not category_id:
                return _http_error_response("Expense name and category ID are required", 400)

            # Ensure the category belongs to the user
            category = request.env['easy_expenses.user_category'].sudo().search([('id', '=', category_id), ('user_id', '=', user_id)], limit=1)
            if not category:
                return _http_error_response("Invalid category ID", 404)

            new_expense = request.env['easy_expenses.user_expense'].sudo().create({
                'name': name,
                'category_id': category_id,
                'user_id': user_id
            })

            return _http_success_response({'id': new_expense.id, 'name': new_expense.name, 'category_id': new_expense.category_id.id},
                                          "User Expense created successfully", 201)
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error creating user expense: {str(e)}", 500)

    ## 🔹 [PUT] Update a User Expense
    @http.route('/api/easy_apps/user_expenses/update/<int:expense_id>', type='jsonrpc', auth='public', methods=['PUT'], csrf=False)
    def update_user_expense(self, expense_id, **kwargs):
        """Update an existing user expense (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            expense = request.env['easy_expenses.user_expense'].sudo().search([('id', '=', expense_id), ('user_id', '=', user_id)], limit=1)
            if not expense:
                return _http_error_response("User Expense not found", 404)

            name = kwargs.get("name")
            category_id = kwargs.get("category_id")

            if name:
                expense.sudo().write({'name': name})
            if category_id:
                # Ensure the new category belongs to the user
                category = request.env['easy_expenses.user_category'].sudo().search([('id', '=', category_id), ('user_id', '=', user_id)], limit=1)
                if not category:
                    return _http_error_response("Invalid category ID", 404)
                expense.sudo().write({'category_id': category_id})

            return _http_success_response({'id': expense.id, 'name': expense.name, 'category_id': expense.category_id.id},
                                          "User Expense updated successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error updating user expense: {str(e)}", 500)

    ## 🔹 [DELETE] Delete a User Expense
    @http.route('/api/easy_apps/user_expenses/delete/<int:expense_id>', type='jsonrpc', auth='public', methods=['DELETE'], csrf=False)
    def delete_user_expense(self, expense_id, **kwargs):
        """Delete a user expense (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            expense = request.env['easy_expenses.user_expense'].sudo().search([('id', '=', expense_id), ('user_id', '=', user_id)], limit=1)
            if not expense:
                return _http_error_response("User Expense not found", 404)

            expense.sudo().unlink()
            return _http_success_response({}, "User Expense deleted successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error deleting user expense: {str(e)}", 500)

## 🔹 [GET] Retrieve All User Expenses
    # @http.route('/api/easy_apps/user_expenses', type='http', auth='public', methods=['GET'], csrf=False)
    # def get_user_expenses(self, **kwargs):
    #     """Retrieve all user expenses (JWT required)"""
    #     try:
    #         user_data = JWTAuth.authenticate_request()  # Validate JWT
    #         user_id = user_data.get("user_id")

    #         expenses = request.env['easy_expenses.user_expense'].sudo().search([('user_id', '=', user_id)])

    #         return _http_success_response(
    #             [{'id': exp.id, 'name': exp.name, 'category_id': exp.category_id.id, 'category_name': exp.category_id.name}
    #              for exp in expenses],
    #             "User Expenses retrieved successfully"
    #         )
    #     except AccessDenied as e:
    #         return _http_error_response(str(e), 401)
    #     except Exception as e:
    #         return _http_error_response(f"Error getting user expenses: {str(e)}", 500)
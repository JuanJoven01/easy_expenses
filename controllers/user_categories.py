from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response


class UserExpenseCategoryAPI(http.Controller):

    ## 🔹 [GET] Retrieve All User Expense Categories
    @http.route('/api/easy_apps/user_categories/get', type='http', auth='public', methods=['GET'], csrf=False)
    def get_user_categories(self, **kwargs):
        """Retrieve all user expense categories (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()  # Validate JWT
            
            # Fetch only categories that belong to the authenticated user
            user_id = user_data.get("user_id")
            categories = request.env['easy_expenses.user_category'].sudo().search([('user_id', '=', user_id)])

            return _http_success_response(
                [{'id': cat.id, 'name': cat.name, 'description': cat.description} for cat in categories],
                "User Categories retrieved successfully"
            )
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error getting user categories: {str(e)}", 500)

    ## 🔹 [POST] Create a New User Expense Category
    @http.route('/api/easy_apps/user_categories/create', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def create_user_category(self, **kwargs):
        """Create a new user expense category (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()  # Validate JWT
            user_id = user_data.get("user_id")

            name = kwargs.get("name")
            description = kwargs.get("description", "")

            if not name:
                return _http_error_response("Category name is required", 400)

            new_category = request.env['easy_expenses.user_category'].sudo().create({
                'name': name,
                'description': description,
                'user_id': user_id
            })

            return _http_success_response({'id': new_category.id, 'name': new_category.name, 'description': new_category.description},
                                          "User Category created successfully", 201)
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error creating user category: {str(e)}", 500)

    ## 🔹 [PUT] Update an Existing User Expense Category
    @http.route('/api/easy_apps/user_categories/update/<int:category_id>', type='jsonrpc', auth='public', methods=['PUT'], csrf=False)
    def update_user_category(self, category_id, **kwargs):
        """Update an existing user expense category (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()  # Validate JWT
            user_id = user_data.get("user_id")

            category = request.env['easy_expenses.user_category'].sudo().search([('id', '=', category_id), ('user_id', '=', user_id)], limit=1)
            if not category:
                return _http_error_response("User Expense Category not found", 404)

            name = kwargs.get("name")
            description = kwargs.get("description")

            if name:
                category.sudo().write({'name': name})
            if description:
                category.sudo().write({'description': description})

            return _http_success_response({'id': category.id, 'name': category.name, 'description': category.description},
                                          "User Category updated successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error updating user category: {str(e)}", 500)

    ## 🔹 [DELETE] Delete a User Expense Category
    @http.route('/api/easy_apps/user_categories/delete/<int:category_id>', type='jsonrpc', auth='public', methods=['DELETE'], csrf=False)
    def delete_user_category(self, category_id, **kwargs):
        """Delete a user expense category (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()  # Validate JWT
            user_id = user_data.get("user_id")

            category = request.env['easy_expenses.user_category'].sudo().search([('id', '=', category_id), ('user_id', '=', user_id)], limit=1)
            if not category:
                return _http_error_response("User Expense Category not found", 404)

            category.sudo().unlink()
            return _http_success_response({}, "User Category deleted successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error deleting user category: {str(e)}", 500)

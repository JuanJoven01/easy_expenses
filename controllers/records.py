from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from .auth import JWTAuth
from ._helpers import _http_success_response, _http_error_response


class ExpenseRecordAPI(http.Controller):

    ## 🔹 [GET] Retrieve All Records (Filtered by Date, Category, or User Category)
    @http.route('/api/easy_apps/records/get', type='http', auth='public', methods=['GET'], csrf=False)
    def get_records(self, **kwargs):
        """
        Retrieve all expense records for the authenticated user (JWT required).
        Optional filters:
        - start_date (YYYY-MM-DD)
        - end_date (YYYY-MM-DD)
        - category_id (Global Category)
        - user_category_id (User Custom Category)
        """
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            domain = [('user_id', '=', user_id)]

            # Date filtering
            start_date = kwargs.get('start_date')
            end_date = kwargs.get('end_date')

            if start_date:
                domain.append(('date', '>=', start_date))
            if end_date:
                domain.append(('date', '<=', end_date))

            # Category filtering
            category_id = kwargs.get('category_id')
            user_category_id = kwargs.get('user_category_id')

            if category_id:
                domain.append(('category_id', '=', int(category_id)))

            if user_category_id:
                domain.append(('user_category_id', '=', int(user_category_id)))

            # Fetch records
            records = request.env['easy_expenses.record'].sudo().search(domain)

            return _http_success_response(
                [{'id': rec.id, 'date': rec.date, 'amount': rec.amount, 'note': rec.note,
                  'category_type': rec.category_type,
                  'category_id': rec.category_id.id if rec.category_id else None,
                  'user_category_id': rec.user_category_id.id if rec.user_category_id else None,
                  'expense_id': rec.expense_id.id if rec.expense_id else None,
                  'user_expense_id': rec.user_expense_id.id if rec.user_expense_id else None}
                 for rec in records],
                "Expense Records retrieved successfully"
            )
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error getting records: {str(e)}", 500)


    ## 🔹 [GET] Retrieve Single Record by ID
    @http.route('/api/easy_apps/records/<int:record_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_record(self, record_id, **kwargs):
        """Retrieve a single expense record by ID (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            record = request.env['easy_expenses.record'].sudo().search([('id', '=', record_id), ('user_id', '=', user_id)], limit=1)
            if not record:
                return _http_error_response("Expense Record not found", 404)

            return _http_success_response({
                'id': record.id, 'date': record.date, 'amount': record.amount, 'note': record.note,
                'category_type': record.category_type,
                'category_id': record.category_id.id if record.category_id else None,
                'user_category_id': record.user_category_id.id if record.user_category_id else None,
                'expense_id': record.expense_id.id if record.expense_id else None,
                'user_expense_id': record.user_expense_id.id if record.user_expense_id else None
            }, "Expense Record retrieved successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error getting record: {str(e)}", 500)


    ## 🔹 [POST] Create a New Record
    @http.route('/api/easy_apps/records/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_record(self, **kwargs):
        """Create a new expense record (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            required_fields = ['amount', 'category_type']
            if not all(kwargs.get(field) for field in required_fields):
                return _http_error_response("Missing required fields", 400)

            category_type = kwargs.get('category_type')
            category_id = kwargs.get('category_id') if category_type == 'global' else None
            user_category_id = kwargs.get('user_category_id') if category_type == 'user' else None
            expense_id = kwargs.get('expense_id') if category_type == 'global' else None
            user_expense_id = kwargs.get('user_expense_id') if category_type == 'user' else None

            record = request.env['easy_expenses.record'].sudo().create({
                'category_type': category_type,
                'category_id': category_id,
                'user_category_id': user_category_id,
                'expense_id': expense_id,
                'user_expense_id': user_expense_id,
                'amount': float(kwargs.get('amount')),
                'date': kwargs.get('date'),
                'note': kwargs.get('note'),
                'user_id': user_id
            })

            return _http_success_response({'id': record.id}, "Expense Record created successfully", 201)
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error creating record: {str(e)}", 500)


    ## 🔹 [PUT] Update an Existing Record
    @http.route('/api/easy_apps/records/update/<int:record_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_record(self, record_id, **kwargs):
        """Update an existing expense record (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            record = request.env['easy_expenses.record'].sudo().search([('id', '=', record_id), ('user_id', '=', user_id)], limit=1)
            if not record:
                return _http_error_response("Expense Record not found", 404)

            record.sudo().write({
                'category_type': kwargs.get('category_type', record.category_type),
                'category_id': kwargs.get('category_id', record.category_id.id if record.category_id else None),
                'user_category_id': kwargs.get('user_category_id', record.user_category_id.id if record.user_category_id else None),
                'expense_id': kwargs.get('expense_id', record.expense_id.id if record.expense_id else None),
                'user_expense_id': kwargs.get('user_expense_id', record.user_expense_id.id if record.user_expense_id else None),
                'amount': float(kwargs.get('amount', record.amount)),
                'date': kwargs.get('date', record.date),
                'note': kwargs.get('note', record.note),
            })

            return _http_success_response({'id': record.id}, "Expense Record updated successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error updating record: {str(e)}", 500)


    ## 🔹 [DELETE] Remove an Expense Record
    @http.route('/api/easy_apps/records/delete/<int:record_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_record(self, record_id, **kwargs):
        """Delete an expense record (JWT required)"""
        try:
            user_data = JWTAuth.authenticate_request()
            user_id = user_data.get("user_id")

            record = request.env['easy_expenses.record'].sudo().search([('id', '=', record_id), ('user_id', '=', user_id)], limit=1)
            if not record:
                return _http_error_response("Expense Record not found", 404)

            record.sudo().unlink()

            return _http_success_response({'id': record_id}, "Expense Record deleted successfully")
        except AccessDenied as e:
            return _http_error_response(str(e), 401)
        except Exception as e:
            return _http_error_response(f"Error deleting record: {str(e)}", 500)

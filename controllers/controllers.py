# -*- coding: utf-8 -*-
# from odoo import http


# class /opt/odoo18/customAddons/easyExpenses(http.Controller):
#     @http.route('//opt/odoo18/custom_addons/easy_expenses//opt/odoo18/custom_addons/easy_expenses', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//opt/odoo18/custom_addons/easy_expenses//opt/odoo18/custom_addons/easy_expenses/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/opt/odoo18/custom_addons/easy_expenses.listing', {
#             'root': '//opt/odoo18/custom_addons/easy_expenses//opt/odoo18/custom_addons/easy_expenses',
#             'objects': http.request.env['/opt/odoo18/custom_addons/easy_expenses./opt/odoo18/custom_addons/easy_expenses'].search([]),
#         })

#     @http.route('//opt/odoo18/custom_addons/easy_expenses//opt/odoo18/custom_addons/easy_expenses/objects/<model("/opt/odoo18/custom_addons/easy_expenses./opt/odoo18/custom_addons/easy_expenses"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/opt/odoo18/custom_addons/easy_expenses.object', {
#             'object': obj
#         })


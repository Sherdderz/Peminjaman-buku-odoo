# -*- coding: utf-8 -*-
# from odoo import http


# class GaezBuku(http.Controller):
#     @http.route('/gaez_buku/gaez_buku', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gaez_buku/gaez_buku/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gaez_buku.listing', {
#             'root': '/gaez_buku/gaez_buku',
#             'objects': http.request.env['gaez_buku.gaez_buku'].search([]),
#         })

#     @http.route('/gaez_buku/gaez_buku/objects/<model("gaez_buku.gaez_buku"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gaez_buku.object', {
#             'object': obj
#         })

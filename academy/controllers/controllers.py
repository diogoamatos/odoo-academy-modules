# -*- coding: utf-8 -*-
from odoo import http


class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['academy.teachers']
        return http.request.render('academy.index', {
            'teachers': Teachers.search([])
        })

    @http.route('/academy/<name>/', auth='public', website=True)
    def teacher(self, name):
        # return http.request.render('academy.teacher', {
        #     'teacher': Teachers.search([['name', '=', name], ])
        # })
        return '<h1>{}</h1>'.format(name)


    # @http.route('/academy/academy/<int:id>/', auth='public', website=True)
    # def teacher(self, id):
    #     Teachers = http.request.env['academy.teachers']
    #     return '<h1>{} ({})</h1>'.format(Teachers.search(id=id), type(id).__name__)

#     @http.route('/academy/academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('academy.listing', {
#             'root': '/academy/academy',
#             'objects': http.request.env['academy.academy'].search([]),
#         })

#     @http.route('/academy/academy/objects/<model("academy.academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academy.object', {
#             'object': obj
#         })

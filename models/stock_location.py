# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'stock.location'

    prioridad_despacho = fields.Integer(string='Prioridad Despacho')
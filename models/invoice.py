# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'account.invoice'

    order_id = fields.Many2one(comodel_name='purchase.order', string='Orden de compra')




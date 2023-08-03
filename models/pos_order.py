# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'pos.order'

    config_id = fields.Many2one(
        comodel_name='pos.config', 
        string='Point of Sale',
        related='session_id.config_id',
        help="The physical point of sale you will use.",
        required=True,
        index=True)






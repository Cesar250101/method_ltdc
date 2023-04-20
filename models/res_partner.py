# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'

    es_paris = fields.Boolean(string='Es Paris?',help="Indica si corresponde a la tienda Paris")

    
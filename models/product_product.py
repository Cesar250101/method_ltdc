# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    tienda_paris = fields.Boolean(string='Tienda Paris')
    sku_paris = fields.Char(string='SKU Paris')
    componente_id = fields.Many2one(comodel_name='method_ltdc.producto_composicion', string='Composición',required=True)
    temporada_id = fields.Many2one(comodel_name='method_ltdc.producto_temporada', string='Temporada',required=True)


class ProductoComposicion(models.Model):
    _name = 'method_ltdc.producto_composicion'
    _description = 'Composición del producto o materias primas'

    name = fields.Char(string='Nombre')
    active = fields.Boolean(string='Activo?',default=True)
        
class ProductoTemporada(models.Model):
    _name = 'method_ltdc.producto_temporada'
    _description = 'Temporada a la cual pertenece el producto'

    name = fields.Char(string='Nombre')
    active = fields.Boolean(string='Activo?',default=True)

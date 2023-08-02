# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    tienda_paris = fields.Boolean(string='Tienda Paris')
    sku_paris = fields.Char(string='SKU Paris')
    componente_id = fields.Many2one(comodel_name='method_ltdc.producto_composicion', 
                                    string='Composición',
                                    required=True,
                                    related="product_tmpl_id.componente_id")
    temporada_id = fields.Many2one(comodel_name='method_ltdc.producto_temporada', 
                                   string='Temporada',
                                   required=True,
                                   related='product_tmpl_id.temporada_id')
    
    componente_id_bak = fields.Many2one(comodel_name='method_ltdc.producto_composicion', 
                                    string='Composición bak',
                                    required=True,
                                    related="product_tmpl_id.componente_id")
    temporada_id_bak = fields.Many2one(comodel_name='method_ltdc.producto_temporada', 
                                   string='Temporada bak',
                                   required=True,
                                   related='product_tmpl_id.temporada_id')


    @api.multi
    def generar_sku(self):
        if self.seller_ids:
            for s in self.seller_ids:
                if s.name and s.product_code:
                    nombre_completo=s.name.name.split()
                    nro_elementos=len(nombre_completo)
                    if nro_elementos==1:
                        nombre=s.name.name.split()
                        inicial_nombre=nombre[0][0:2]
                        sku_generado=inicial_nombre.upper()+'-'+s.product_code                    
                    else:
                        nombre=nombre_completo[0]
                        apellido=nombre_completo[1]                        
                        inicial_nombre=nombre[0]
                        inicial_apellido=apellido[0]
                        sku_generado=inicial_nombre.upper()+inicial_apellido.upper()+'-'+s.product_code
                for a in self.attribute_value_ids:
                    print(a)
                    sku_generado+='-'+a.name[0:2]
            self.default_code=sku_generado
            self.barcode=sku_generado

    @api.onchange('default_code')
    def onchange_default_code(self):
        if self.default_code:
            self.barcode=self.default_code

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

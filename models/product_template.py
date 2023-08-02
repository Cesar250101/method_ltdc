# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    tienda_paris = fields.Boolean(string='Tienda Paris')
    sku_paris = fields.Char(string='SKU Paris')
    componente_id = fields.Many2one(comodel_name='method_ltdc.producto_composicion', string='Composición',required=True)
    temporada_id = fields.Many2one(comodel_name='method_ltdc.producto_temporada', string='Temporada',required=True)

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
                        nombre,apellido,otros=s.name.name.split()
                        inicial_nombre=nombre[0]
                        inicial_apellido=apellido[0]
                        sku_generado=inicial_nombre.upper()+inicial_apellido.upper()+'-'+s.product_code
                for a in self.attribute_value_ids:
                    print(a)
                    sku_generado+='-'+a.name[0:2]
            self.default_code=sku_generado
            self.barcode=sku_generado





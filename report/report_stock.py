# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, tools

class StockProveedor(models.Model):
    _name = 'method_ltdc.stock_report_proveedor'
    _description = "Stock por proveedor"
    _auto = False
    # _order = 'product_id desc'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Proveedor')
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    atributo_id = fields.Many2one(comodel_name='product.attribute.value', string='Atributo')
    ubicacion_id = fields.Many2one(comodel_name='stock.location', string='Ubicación')
    stock = fields.Integer(string='Stock')
    categoria_id = fields.Many2one(comodel_name='product.category', string='Categoria Producto')
    composicion_id = fields.Many2one(comodel_name='method_ltdc.producto_composicion', string='Composición')
    temporada_id = fields.Many2one(comodel_name='method_ltdc.producto_temporada', string='Temporada')
    costo = fields.Integer(string='Costo')
    costo_total = fields.Integer(string='Costo Total')
    


    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT ROW_NUMBER() OVER() AS id, rp.id partner_id,pp.id product_id,pav.id atributo_id,
sl.id ubicacion_id,sq.quantity stock,pt.categ_id  categoria_id, pt.componente_id composicion_id,pt.temporada_id  temporada_id,
(select cost from product_price_history pph
                	where pph.product_id =pp.id
							order by datetime desc
							limit 1) costo,
				(sq.quantity*(select cost from product_price_history pph where pph.product_id =pp.id order by datetime desc limit 1)) costo_total                                                  
from product_template pt left join res_partner rp  on pt.proveedor_id =rp.id
inner join product_product pp on pt.id=pp.product_tmpl_id 
left join product_attribute_value_product_product_rel pavppr on pavppr.product_product_id  =pp.id 
left join product_attribute_value pav on pavppr.product_attribute_value_id=pav.id 
inner join  stock_quant sq on pp.id=sq.product_id
inner join stock_location sl on sq.location_id =sl.id
where  sl.usage='internal'  
                          
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))


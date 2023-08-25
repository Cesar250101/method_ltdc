# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, tools

class Ventas(models.Model):
    _name = 'method_ltdc.ventas_report_proveedor'
    _description = "Ventas por proveedor"
    _auto = False
    # _order = 'product_id desc'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Proveedor')
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Plantilla Producto')
    atributo_id = fields.Many2one(comodel_name='product.attribute.value', string='Atributo')
    categ_id = fields.Many2one(comodel_name='product.category', string='Categoria Producto')
    composicion_id = fields.Many2one(comodel_name='method_ltdc.producto_composicion', string='Composición')
    temporada_id = fields.Many2one(comodel_name='method_ltdc.producto_temporada', string='Temporada')
    cantidad = fields.Integer(string='Cantidad')
    price_subtotal = fields.Integer(string='Subtotal')
    price_subtotal_incl = fields.Integer(string='Total')
    fecha_orden = fields.Date(string='Fecha Orden')
    origen = fields.Char(string='Origen')
    pos = fields.Char(string='Punto de Venta')


    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT ROW_NUMBER() OVER() AS id, ps.name partner_id,pp.id product_id,pt.id product_tmpl_id,pt.categ_id,
mlpc.id composicion_id,mlpt.id  temporada_id,pol.qty cantidad,pol.price_subtotal,pol.price_subtotal_incl ,
po.date_order fecha_orden,'Punto de Venta' origen,pc2.name pos
from pos_order po inner join pos_order_line pol on po.id=pol.order_id 
inner join product_product pp on pol.product_id =pp.id 
inner join product_template pt on pp.product_tmpl_id =pt.id 
inner join product_category pc on pt.categ_id =pc.id 
left join product_supplierinfo ps on ps.product_tmpl_id =pt.id 
left join method_ltdc_producto_composicion mlpc on pt.componente_id =mlpc.id 
left join method_ltdc_producto_temporada mlpt on pt.temporada_id =mlpt.id
inner join pos_session ps2 on po.session_id =ps2.id 
inner join pos_config pc2 on ps2.config_id =pc2.id 
union 
Select ROW_NUMBER() OVER() AS id, ps.name partner_id,pp.id product_id,pt.id product_tmpl_id,pt.categ_id,
mlpc.id composicion_id,mlpt.id  temporada_id,sol.product_uom_qty cantidad,sol.price_subtotal,sol.price_total ,
so.date_order fecha_orden ,'Web' origen,'Web' 
from sale_order so inner join sale_order_line sol  on so.id=sol.order_id  
inner join product_product pp on sol.product_id =pp.id 
inner join product_template pt on pp.product_tmpl_id =pt.id 
inner join product_category pc on pt.categ_id =pc.id 
left join product_supplierinfo ps on ps.product_tmpl_id =pt.id 
left join method_ltdc_producto_composicion mlpc on pt.componente_id =mlpc.id 
left join method_ltdc_producto_temporada mlpt on pt.temporada_id =mlpt.id 
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))


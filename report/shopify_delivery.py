# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, tools

class PickingShopify(models.Model):
    _name = 'method_ltdc.shopify_report_delivery'
    _description = "Moviemto de productos por Shopify"
    _auto = False
    # _order = 'product_id desc'

    origin = fields.Char(string='Orden')
    date_done = fields.Datetime(string='Fecha Picking')
    picking = fields.Char(string='Nombre Picking')
    picking_id = fields.Many2one(comodel_name='stock.picking', string='Picking')
    location_id = fields.Many2one(comodel_name='stock.location', string='Ubicación')    
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    qty_done = fields.Integer(string='Cantidad')
    product_uom_id = fields.Many2one(comodel_name='uom.uom', string='Und')


    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT ROW_NUMBER() OVER() AS id, origin ,sp.date_done,
                    sp.name picking,sp.id picking_id,sml.location_id,sml.product_id,
                    sml.qty_done,sml.product_uom_id
                    from stock_picking sp,stock_move_line sml,stock_location sl  
                    where coalesce(sp.sale_id,0)!=0 
                    and sp.id=sml.picking_id 
                    and sml.location_id =sl.id  
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))


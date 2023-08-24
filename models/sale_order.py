# -*- coding: utf-8 -*-

from datetime import timedelta
# from addons.sh_shopify_connector.models.sale_order import MAP_INVOICE_TYPE_PARTNER_TYPE
from odoo import fields, models,_,api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            # 'date_order': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        if self.workflow_id:
            ubicacion_id=False
            stock_suficiente=True
            if self.workflow_id.validate_order:
                if self.workflow_id.force_transfer:
                    for picking in self.picking_ids:
                        tienda=self.env['sh.shopify.configuration'].search([],limit=1)
                        vals_picking={
                            'location_id':tienda.location_id.id
                        }
                        picking.write(vals_picking)

                        ubicacion_stock=self.env['stock.location'].search([('prioridad_despacho','>=',1)],order="prioridad_despacho")

                        for move in picking.move_lines:
                            cantidad_mover=move.product_uom_qty
                            domain=[('location_id','=',move.location_id.id),
                                    ('product_id','=',move.product_id.id)]
                                    
                            disponible=self.env['stock.quant'].search(domain,limit=1).quantity
                            if disponible<cantidad_mover:
                                for u in ubicacion_stock:
                                    #Si el producto esta totalmente disponible en la nueva ubicación sale y va a insertar la linea al final
                                    domain=[('location_id','=',u.id),
                                            ('product_id','=',move.product_id.id)
                                            ]
                                    disponible=self.env['stock.quant'].search(domain,limit=1).quantity
                                    if disponible>0 and cantidad_mover>0: 
                                        if disponible<=cantidad_mover:
                                            self.env['stock.move.line'].create({
                                                    'picking_id':picking.id,
                                                    'move_id':move.id,
                                                    'date':move.date,
                                                    'reference':move.reference,
                                                    'origin':move.origin,
                                                    'qty_done':disponible,
                                                    'product_id':move.product_id.id,
                                                    'product_uom_id':move.product_uom.id,
                                                    'location_id':u.id,
                                                    'location_dest_id':move.location_dest_id.id
                                                })                                       
                                        #Si el producto esta parcialmente disponible en la nueva ubicación hace un ciclo hasta cubrir toda la cantidad
                                        else:
                                            self.env['stock.move.line'].create({
                                                    'picking_id':picking.id,
                                                    'move_id':move.id,
                                                    'date':move.date,
                                                    'reference':move.reference,
                                                    'origin':move.origin,
                                                    'qty_done':cantidad_mover,
                                                    'product_id':move.product_id.id,
                                                    'product_uom_id':move.product_uom.id,
                                                    'location_id':u.id,
                                                    'location_dest_id':move.location_dest_id.id
                                                })                                       
                                        cantidad_mover=cantidad_mover-disponible
                            else:
                                ubicacion_id=move.location_id
                                self.env['stock.move.line'].create({
                                        'picking_id':picking.id,
                                        'move_id':move.id,
                                        'date':move.date,
                                        'reference':move.reference,
                                        'origin':move.origin,
                                        'qty_done':move.product_uom_qty,
                                        'product_id':move.product_id.id,
                                        'product_uom_id':move.product_uom.id,
                                        'location_id':ubicacion_id.id,
                                        'location_dest_id':move.location_dest_id.id
                                    })
                        picking.button_validate()
                        if picking.state != 'done':
                            try:
                                sms = self.env['confirm.stock.sms'].create({ 
                                    'picking_id': picking.id,
                                })
                                sms.send_sms()
                            except:
                                pass



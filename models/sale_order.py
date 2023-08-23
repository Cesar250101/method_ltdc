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

        # return True
        if self.workflow_id:
            ubicacion_id=False
            if self.workflow_id.validate_order and self.picking_ids:
                if self.workflow_id.force_transfer:
                    for picking in self.picking_ids:
                        tienda=self.env['sh.shopify.configuration'].search([],limit=1)
                        vals_picking={
                            'location_id':tienda.location_id.id
                        }
                        picking.write(vals_picking)

                        ubicacion_stock=self.env['stock.location'].search([('prioridad_despacho','>',1)],order="prioridad_despacho")

                        for stock_move in picking.move_ids_without_package:
                            disponible=self.env['stock.quant'].search([('location_id','=',stock_move.location_id.id),
                                                                       ('product_id','=',stock_move.product_id.id)],limit=1).quantity
                            disponible=disponible-stock_move.product_qty
                            if disponible<0:
                                for u in ubicacion_stock:
                                    disponible=self.env['stock.quant'].search([('location_id','=',u.id),
                                                                            ('product_id','=',stock_move.product_id.id)],limit=1).quantity
                                    disponible=disponible-stock_move.product_qty
                                    if disponible>0:
                                        ubicacion_id=u.id
                                        break
                                    else:
                                        disponible=self.env['stock.quant'].search([('location_id','=',u.id),
                                                                                ('product_id','=',stock_move.product_id.id)],limit=1).quantity
                                        disponible=disponible-stock_move.product_qty
                                        if disponible>0:
                                            ubicacion_id=u.id
                                            break
                            else:
                                ubicacion_id=tienda.location_id.id
                            if ubicacion_id==False:
                                ubicacion_id=tienda.location_id.id
                            if stock_move.move_line_ids:
                                stock_move.move_line_ids.update({
                                    'qty_done':stock_move.product_uom_qty,
                                })
                            else:
                                self.env['stock.move.line'].create({
                                    'picking_id':picking.id,
                                    'move_id':stock_move.id,
                                    'date':stock_move.date,
                                    'reference':stock_move.reference,
                                    'origin':stock_move.origin,
                                    'qty_done':stock_move.product_uom_qty,
                                    'product_id':stock_move.product_id.id,
                                    'product_uom_id':stock_move.product_uom.id,
                                    # 'location_id':tienda.location_id.id,
                                    'location_id':ubicacion_id,
                                    'location_dest_id':stock_move.location_dest_id.id
                                })
                        picking.button_validate()
                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({ 
                                'picking_id': picking.id,
                            })
                            sms.send_sms()
                            
                else:
                    for picking in self.picking_ids:
                        picking.button_validate()

                        wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, picking.id)]})
                        wiz.process()

                        if picking.state != 'done':
                            sms = self.env['confirm.stock.sms'].create({ 
                                'picking_id': picking.id,
                            })
                            sms.send_sms()
                            ret = picking.button_validate()
                            if 'res_model' in ret and ret['res_model'] == 'stock.backorder.confirmation':
                                backorder_wizard = self.env['stock.backorder.confirmation'].create({
                                    'pick_ids':[(4,picking.id)]
                                })
                                backorder_wizard.process()                    
                    
            if self.workflow_id.create_invoice:
                # invoice = self._create_invoices()
                invoice = self._create_invoices()
                if  self.workflow_id.sale_journal:
                    invoice.write({
                        'journal_id' : self.workflow_id.sale_journal.id
                    })
                
                if self.workflow_id.validate_invoice:
                    invoice.action_invoice_open()

                    if self.workflow_id.send_invoice_by_email:
                        template_id = self.env.ref('account.email_template_edi_invoice')
                        template_id.with_context(model_description='').sudo().send_mail(invoice.id, force_send=True,notif_layout="mail.mail_notification_paynow")

                    if self.workflow_id.register_payment:
                        
                        # payment_methods = self.env['account.payment.method'].search([('payment_type','=','inbound')])
                        # journal = self.env['account.journal'].search([('type','in',('bank','cash'))])
                        payment = self.env['account.payment'].create({
                            'currency_id': invoice.currency_id.id,
                            'amount':invoice.amount_total,
                            'payment_type': 'inbound',
                            'partner_id': invoice.commercial_partner_id.id,
                            'partner_type': MAP_INVOICE_TYPE_PARTNER_TYPE[invoice.type],
                            'communication': invoice.display_name,
                            'invoice_ids': [(6, 0, invoice.ids)],
                            'payment_method_id':self.workflow_id.payment_method.id,
                            'journal_id':self.workflow_id.payment_journal.id,
                            'payment_date':invoice.date_invoice
                        })
                    
                        payment.post()

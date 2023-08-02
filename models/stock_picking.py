# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class Partner(models.Model):
    _inherit = 'stock.picking'


    @api.multi
    def reponer_ventas(self):
        ubicacion_cliente=self.env['stock.location'].search([('usage','=','customer')])
        ubicacion=[]

        dias_a_restar = 1 # Cambia el número de dias que deseas restar
        fecha_actual = datetime.datetime.now()
        fecha_nueva = fecha_actual - datetime.timedelta(days=dias_a_restar)
        fecha_inicial = fecha_nueva.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_final = fecha_nueva.replace(hour=23, minute=55, second=55, microsecond=0)
        for u in ubicacion_cliente:
            ubicacion.append(u.id)
        domain=[
            ('location_dest_id','in',ubicacion),
            ('create_date','>=',fecha_inicial),
            ('create_date','<=',fecha_final),
            ('state','=','done')
        ]
        ventas_dia_anterior=self.env['stock.move'].search(domain)

        for v in ventas_dia_anterior:
            val={
                    'name':v.product_id.name,
                    'picking_id':self.id,
                    'product_id':v.product_id.id,
                    'product_uom_qty':v.product_qty,
                    'product_uom':v.product_uom.id,
                    'location_dest_id':self.location_dest_id.id,
                    'location_id':self.location_id.id,
                    'price_unit':v.product_id.list_price

                }   
            stock_move_id=self.env['stock.move'].sudo().create(val)                

    
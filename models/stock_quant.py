# -*- coding: utf-8 -*-

from odoo import models, fields, api
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ProductProduct(models.Model):
    _inherit = 'stock.quant'


    @api.model
    def enviar_correo_reposicion(self):        
        # Configuración del servidor SMTP
        cuenta_correo=self.env['ir.mail_server'].search([],limit=1)
        smtp_host = cuenta_correo.smtp_host
        smtp_port = cuenta_correo.smtp_port
        smtp_username = cuenta_correo.smtp_user
        smtp_password = cuenta_correo.smtp_pass

        # Crear objeto de mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = 'noreply@method.cl'
        # mensaje['To'] = 'ventas@latiendadecarolina.cl'
        mensaje['To'] = 'cesar@method.cl'
        mensaje['Subject'] = 'Traspaso de productos a bodega desde sucursales'

        product_id=self.search([('location_id','=',12),('quantity','<',0)])
        productos=""
        for p in product_id:
            try:
                productos+=p.product_id.default_code+" "+p.product_id.name +"\n"
            except:
                productos+=p.product_id.name +"\n"
        # Cuerpo del mensaje
        cuerpo_mensaje = """
        Estimada Usuario,

        se requiere el traspaso de productos desde sucursales
        hacia la bodega de los siguientes productos:
        {}
        Saludos,
        Remitente
        """.format(productos)

        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

        # Establecer conexión segura con el servidor SMTP
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)

        # Enviar correo electrónico
        smtp.send_message(mensaje)

        # Cerrar conexión con el servidor SMTP
        smtp.quit()



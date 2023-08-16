# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductSupplier(models.Model):
    _inherit = 'product.supplierinfo'

    
    def unificar_proveedor(self):
        query="""
            select product_tmpl_id  
            from product_supplierinfo ps 
            group by product_tmpl_id 
            having count(*) >1
            """
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()

        if result:
            for i in result:
                r=1
                product_template_ids=self.search([('product_tmpl_id','=',i[0])])
                for pt in product_template_ids:
                    if r>1:
                        query="delete from product_supplierinfo where id={}".format(pt.id)        
                        self.env.cr.execute(query)
                    r+=1
                    pt.product_id=False
            return True
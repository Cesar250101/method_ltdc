# -*- coding: utf-8 -*-
{
    'name': "method_ltdc",

    'summary': """
        Localización cliente LTDC
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Method ERP",
    'website': "https://www.method.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','l10n_cl_fe'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_product.xml',
        'views/templates.xml',
        'views/res_partner.xml',
        # 'report/layout.xml',
        'data/data.xml',
        'views/invoice.xml',
        'views/stock_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
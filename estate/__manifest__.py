# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
    Manage real estate properties and transactions
    """,

    'version': '1.0',
    'depends': ['base'],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'security/estate_security.xml',

        'views/res_users_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        
        'views/estate_menus.xml',
    ]
}
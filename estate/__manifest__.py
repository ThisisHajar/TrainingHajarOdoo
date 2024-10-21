{
    'name': 'Real Estate',
    "sequence":1,
    # we call wizard before estate_property_views because we have action in wizard to call inside it
    'data':[
        'security/ir.model.access.csv',
        'wizard/sold_wizard_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer.xml',
        'views/res_users_view.xml',
        'views/estate_menus.xml',
        'report/estate_property_report.xml',
        'report/property_users_report.xml',

    ],

    'depends':['base'],
    'application': True,

}
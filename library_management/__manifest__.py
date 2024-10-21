{
    'name': 'Library Management',
    "sequence":3,
    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/library_author.xml',
        'views/library_book.xml',
        'views/library_reservations.xml',
        'views/library_menus.xml',
    ],


    'application': True,

}


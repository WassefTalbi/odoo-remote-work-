

{
    'name': 'app one',
    'version': '17.0.0.1.0',
    'category': '',
     'author':'Wassef Talbi',
    'summary': 'tracking remote work',


    'depends': ['base','sale_management','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/account_move_view.xml',
        'views/property_history_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
         'reports/property_report.xml'
          ],
       'assets': {
        'web.assets_backend': [
            #'app_one/static/src/css/property.css'
         ]
      },
    'application': True,


}

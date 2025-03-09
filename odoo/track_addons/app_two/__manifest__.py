

{
    'name': 'app two',
    'version': '17.0.0.1.0',
    'category': '',
     'author':'Wassef Talbi',
    'summary': 'todo remote work',


    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_view.xml',

          ],
       'assets': {
        'web.assets_backend': [
            #'app_two/static/src/css/property.css'
         ]
      },
    'application': True,


}

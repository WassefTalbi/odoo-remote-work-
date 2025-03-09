

{
    'name': 'remote work',
    'version': '17.0.0.1.0',
    'category': 'Human Resources',
     'author':'Wassef Talbi',
    'summary': 'Track employee work activities with check-in, pause, resume, and checkout.',


    'depends': ['base','hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        #'security/hr.attendance.rules.csv',
        'views/hr_attendance_menus.xml',
        'views/checkin_checkout_wizard_views.xml',
        'views/pause_reprise_wizard_views.xml',
        'views/hr_break_wizard_views.xml',


          ],
       'assets': {
        'web.assets_backend': [

         ]
      },
    'application': True,
    'installable': True,


}

{
    'name': 'HR Medical Checkups',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Ewidencja badań lekarskich pracowników',
    'author': 'Jarosław Kopacz',
    'depends': ['hr'],
    'data': [
        'views/medical_checkup_views.xml',
        'data/medical_checkup_cron.xml',
    ],
    'installable': True,
    'application': False,
}

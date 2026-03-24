# -*- coding: utf-8 -*-
{
    'name': "Maintenance Repair Integration",
    'summary': "Integrate Repair module features into Maintenance.",
    'description': """
        This module links Maintenance Requests and Maintenance Equipment with Repair Orders.
        It allows users to track and create repair orders directly from maintenance records.
    """,
    'author': "El Mario",
    'website': "",
    'category': 'Manufacturing/Maintenance',
    'version': '1.0',
    'depends': ['maintenance', 'repair'],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
        'views/repair_views.xml',
        'views/maintenance_equipment_copy_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

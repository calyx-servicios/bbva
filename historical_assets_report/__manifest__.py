# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Historical Assets Report",
    "summary": """
       This module adds to the wizard that generates a report a period of time.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["carlamiquetan"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "13.0.2.0.1",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [ "account_asset_management_menu",
        "account_asset_management",
        "account_asset_revalue",
        "report_xlsx",
        "revaluation_report"
                 ],
    'data': [
        'wizard/historical_asset_report.xml',
        'views/revaluation_historical_detail_view.xml',
        "report/historical_asset_report_xls.xml",
    ],

}

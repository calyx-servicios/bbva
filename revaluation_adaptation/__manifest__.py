# pylint: disable=missing-module-docstring,pointless-statement
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{

    "name": "Revaluation Adaptation",
    "summary": """
        This module adds columns to the revaluation amortization table.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["carlamiquetan"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "13.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [ "base",
        "account_asset_management_menu",
        "account_asset_management",
        "account_asset_revalue",],
    'data': [
        'views/revaluation_adaptation.xml',
    ],
}

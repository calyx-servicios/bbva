# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Depreciable Account Assets",
    "summary": """
        This module makes cosmetic changes is the account assets module.
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
    "depends": ["base", "account_asset_management_menu", "account_asset_management",],
    'data': [
        'views/asset_not_amortize.xml',
        'views/historical_asset_remove.xml',
    ],

}

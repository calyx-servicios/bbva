from odoo import _, api, fields, models

class AccountAssetRevaluateReport(models.TransientModel):
    _inherit = "account.asset.historical.report.detail"

    date_to = fields.Date("Date To")
    date_from = fields.Date("Date From")
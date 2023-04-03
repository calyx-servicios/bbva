# Copyright 2022 Calyx
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo import fields, models, _
import logging
logger = logging.getLogger(__name__)
from odoo.exceptions import ValidationError


class AccountAsset(models.Model):
    _inherit = "account.asset"

    def compute_depreciation_board(self):
        res = super(AccountAsset, self).compute_depreciation_board()

        self.compute_depreciation_inflation()

        return True #Retornar error correctamente

    def compute_depreciation_inflation(self):
        for asset in self:
            for line in asset.inflation_line_ids:
                if self.does_not_amortize:
                    line.update(
                        {
                            "depreciated_value": "0.00",
                            "depreciated_value_result": "0.00",
                            "depreciated_adjustment": "0.00",
                        }
                    )

    def _compute_depreciation_line(
            self,
            depreciated_value_posted,
            table_i_start,
            line_i_start,
            table,
            last_line,
            posted_lines,
    ):
        digits = self.env["decimal.precision"].precision_get("Account")
        company = self.company_id
        fiscalyear_lock_date = company.fiscalyear_lock_date or fields.Date.to_date(
            "1901-01-01"
        )

        seq = len(posted_lines)
        depr_line = last_line
        last_date = table[-1]["lines"][-1]["date"]
        depreciated_value = depreciated_value_posted
        amount_to_allocate = 0.0
        for entry in table[table_i_start:]:
            for line in entry["lines"][line_i_start:]:
                seq += 1
                name = self._get_depreciation_entry_name(seq)
                amount = line["amount"]
                if self.carry_forward_missed_depreciations:
                    if line["init"]:
                        amount_to_allocate += amount
                        amount = 0
                    else:
                        amount += amount_to_allocate
                        amount_to_allocate = 0.0
                if line["date"] == last_date:
                    # ensure that the last entry of the table always
                    # depreciates the remaining value
                    amount = self.depreciation_base - depreciated_value
                    if self.method in ["linear-limit", "degr-limit"]:
                        amount -= self.salvage_value
                if amount or self.carry_forward_missed_depreciations:
                    vals = {
                        "previous_id": depr_line.id,
                        "amount": round(amount, digits),
                        "asset_id": self.id,
                        "name": name,
                        "line_date": line["date"],
                        "line_days": line["days"],
                        "init_entry": fiscalyear_lock_date >= line["date"],
                    }
                    if self.does_not_amortize:
                        vals.update({
                            "amount": 0,
                        })
                    depreciated_value += round(amount, digits)
                    depr_line = self.env["account.asset.line"].create(vals)
                else:
                    seq -= 1
            line_i_start = 0



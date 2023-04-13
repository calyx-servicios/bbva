from odoo import _, api, fields, models

class AccountAssetAmortization(models.Model):
    _inherit = "account.asset.tax.amortization"


    update_effect_vr = fields.Float("Update Effect Vr", compute="_compute_update_effect_vr")
    updated_amortization = fields.Float("Updated Amortization", compute="_compute_updated_amortization")
    amortization_update_effect = fields.Float("Amortization Update Effect", compute="_compute_amortization_update_effect")

    @api.onchange("residual_value_updated", "residual_value_initial")
    def _onchange_compute_update_effect_vr(self):
        for rec in self:
            rec.update_effect_vr = abs(
                rec.residual_value_updated - rec.residual_value_initial
            )

    @api.depends("residual_value_updated", "residual_value_initial")
    def _compute_update_effect_vr(self):
        for rec in self:
            rec.update_effect_vr = abs(
                rec.residual_value_updated - rec.residual_value_initial
            )\

    @api.onchange("account_asset_id.historical_tax_residual_value_revalued", "residual_value_remaining", "coefficient")
    def _onchange_compute_updated_amortization(self):
        for rec in self:
            rec.updated_amortization = (rec.account_asset_id.historical_tax_residual_value_revalued / rec.residual_value_remaining) * rec.coefficient

    @api.depends("account_asset_id.historical_tax_residual_value_revalued", "residual_value_remaining", "coefficient")
    def _compute_updated_amortization(self):
        for rec in self:
            rec.updated_amortization = (rec.account_asset_id.historical_tax_residual_value_revalued / rec.residual_value_remaining) * rec.coefficient

    @api.onchange("updated_amortization", "amortization")
    def _onchange_amortization_update_effect(self):
        for rec in self:
            rec.amortization_update_effect = abs(rec.updated_amortization - rec.amortization)

    @api.depends("updated_amortization", "amortization")
    def _compute_amortization_update_effect(self):
        for rec in self:
            rec.amortization_update_effect = abs(rec.updated_amortization - rec.amortization)
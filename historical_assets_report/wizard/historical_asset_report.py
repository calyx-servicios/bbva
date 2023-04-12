from odoo import _, api, fields, models
from collections import defaultdict
from odoo.exceptions import ValidationError
import logging

class AsseRevaluationWizard(models.TransientModel):
    _inherit = "asset.revaluation.historical.wizard"
    _description = "Revaluation Historical Wizard"

    date_to = fields.Date("Date to")
    date_from = fields.Date("Date From")

    def amortize_button_asset(self):
        try:
            self.ensure_one()
            self.delete_entries()
        except Exception as e:
            logging.error(e)

        if self.excel:
            self.env.ref("revaluation_report.revaluation_historical_report_xls").report_action(self)
            return {
                'binding_type': 'report',
                'model': 'report.revaluation_report.revaluation_historical_report_xls',
                'name': 'sale',
                'report_file': 'revaluation_report.revaluation_historical_report_xls',
                'report_name': 'revaluation_report.revaluation_historical_report_xls',
                'report_type': 'xlsx',
                'type': 'ir.actions.report'
            }

        if self.detail:
            self.generate_entries()
            view_id_tree = self.env.ref('revaluation_report.view_account_assets_revaluation_historical').id
            context = {'group_by': 'profile_id'} if self.detail else {}
            return {
                'name': 'Report Revaluation',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'context': context,
                'res_model': 'account.asset.revaluate.historical',
                'views': [(view_id_tree, 'tree')],
                'target': 'current',
            }
        else:
            self.generate_entries_grouped()
            view_id_tree = self.env.ref('revaluation_report.view_account_assets_revaluation_historical_report').id
            return {
                'name': 'Report Revaluation Historical',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.asset.historical.report.detail',
                'views': [(view_id_tree, 'tree')],
                'target': 'current',
            }

    def _asset_amortization_in_period(self, asset):
        return self.env['account.historical.update'].search(
            [
                ('date_to', '>=', self.date_from),
                ('date_to', '<=', self.date_to) ,
                ('account_asset_id', '=', asset.id),
            ]
        )

    def _all_amorts_in_period(self, assets):
        return self.env['account.historical.update'].search(
            [
                ('date_to', '>=', self.date_from),
                ('date_to', '<=', self.date_to),
                ('account_asset_id', 'in', assets.ids),
            ]
        )

    def generate_entries(self):
        rows = []
        amorts_in_assets = self._get_amorts_per_asset_per_category()
        for amort in amorts_in_assets:
            category = amort.account_asset_id.profile_id
            row = {
                'period': amort.date_to,
                'name': amort.account_asset_id.name,
                'code': amort.account_asset_id.code,
                'profile_id': category.name,
                'historical_source_value': amort.historical_source_value,
                'inflation_index': amort.inflation_index,
                'historical_source_value_inflation': amort.historical_source_value_inflation,
                'origin_value_difference': amort.origin_value_difference,
                'historical_initial_residual_value_inception': amort.historical_initial_residual_value_inception,
                'historical_residual_value_current_period': amort.historical_residual_value_current_period,
                'remaining_useful_life_at_start': amort.remaining_useful_life_at_start,
                'historical_amortization_adjusted': amort.historical_amortization_adjusted,
                'historical_residual_value_adjusted_closing': amort.historical_residual_value_adjusted_closing,
                'historical_residual_value_at_sap_beginning': amort.historical_residual_value_at_sap_beginning,
                'sap_historical_amortization': amort.sap_historical_amortization,
                'sap_closing_historical_residual_value': amort.sap_closing_historical_residual_value,
                'historical_vri_updated_beginning_current_period': amort.historical_vri_updated_beginning_current_period,
                'depreciation_update_outside_sap': amort.depreciation_update_outside_sap,
                'difference_historical_vri_updated_closing': amort.difference_historical_vri_updated_closing,
            }
            rows.append(row)
        if not rows:
            raise ValidationError(_('There are no lines loaded in the table for that period'))

        self.env['account.asset.revaluate.historical'].create(rows)

    def generate_entries_for_xls(self):
        rows = []
        amorts_in_assets = self._get_amorts_per_asset_per_category()
        for a in amorts_in_assets:
            category = a.account_asset_id.profile_id
            row = {
                'date': a.date_to,
                'name': a.account_asset_id.name,
                'reference': a.account_asset_id.code,
                'profile_id': category.name,
                'historical_source_value': a.historical_source_value,
                'cpi_inflation_index': a.inflation_index,
                'historical_source_value_inflation': a.historical_source_value_inflation,
                'origin_value_difference': a.origin_value_difference,
                'historical_initial_residual_value_inception': a.historical_initial_residual_value_inception,
                'historical_residual_value_current_period': a.historical_residual_value_current_period,
                'remaining_useful_life_at_start': a.remaining_useful_life_at_start,
                'historical_amortization_adjusted': a.historical_amortization_adjusted,
                'historical_residual_value_adjusted_closing': a.historical_residual_value_adjusted_closing,
                'historical_residual_value_at_sap_beginning': a.historical_residual_value_at_sap_beginning,
                'sap_historical_amortization': a.sap_historical_amortization,
                'sap_closing_historical_residual_value': a.sap_closing_historical_residual_value,
                'historical_vri_updated_beginning_current_period': a.historical_vri_updated_beginning_current_period,
                'depreciation_update_outside_sap': a.depreciation_update_outside_sap,
                'difference_historical_vri_updated_closing': a.difference_historical_vri_updated_closing,
            }
            rows.append(row)
        if not rows:
            raise ValidationError(_('There are no lines loaded in the table for that period'))
        return rows

    def generate_entries_grouped(self):
        rows = []
        amorts_by_category = defaultdict(lambda: defaultdict(int))
        amorts_in_assets = self._get_amorts_per_asset_per_category()

        for amort in amorts_in_assets:
            category = amort.account_asset_id.profile_id

            amorts_by_category[category.id]["inflation_index"] = amort.inflation_index
            amorts_by_category[category.id]["profile_id"] = category.name

            amorts_by_category[category.id]["historical_source_value"] += amort.historical_source_value
            amorts_by_category[category.id][
                "historical_source_value_inflation"] += amort.historical_source_value_inflation
            amorts_by_category[category.id]["origin_value_difference"] += amort.origin_value_difference
            amorts_by_category[category.id][
                "historical_initial_residual_value_inception"] += amort.historical_initial_residual_value_inception
            amorts_by_category[category.id][
                "historical_residual_value_current_period"] += amort.historical_residual_value_current_period
            amorts_by_category[category.id]["remaining_useful_life_at_start"] += amort.remaining_useful_life_at_start
            amorts_by_category[category.id][
                "historical_amortization_adjusted"] += amort.historical_amortization_adjusted
            amorts_by_category[category.id][
                "historical_residual_value_adjusted_closing"] += amort.historical_residual_value_adjusted_closing
            amorts_by_category[category.id]["sap_historical_amortization"] += amort.sap_historical_amortization
            amorts_by_category[category.id][
                "historical_residual_value_at_sap_beginning"] += amort.historical_residual_value_at_sap_beginning
            amorts_by_category[category.id][
                "sap_closing_historical_residual_value"] += amort.sap_closing_historical_residual_value
            amorts_by_category[category.id][
                "historical_vri_updated_beginning_current_period"] += amort.historical_vri_updated_beginning_current_period
            amorts_by_category[category.id]["depreciation_update_outside_sap"] += amort.depreciation_update_outside_sap
            amorts_by_category[category.id][
                "difference_historical_vri_updated_closing"] += amort.difference_historical_vri_updated_closing

        for category, values in amorts_by_category.items():
            values["date_from"] = self.date_from
            values["date_to"] = self.date_to
            rows.append(values)

        self.env['account.asset.historical.report.detail'].create(rows)


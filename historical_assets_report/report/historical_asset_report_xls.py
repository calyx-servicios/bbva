from odoo import models, _

header_to_field = {
    'date': _("Date"),
    'name': _("Name"),
    'profile_id': _("Asset Profile"),
    'fixed_active_code': _("Fixed Active"),
    'historical_source_value': _("Historical source value"),
    'cpi_inflation_index': _("CPI inflation index"),
    'historical_source_value_inflation': _("Historical source value with inflation"),
    'origin_value_difference':  _("Origin Value Difference"),
    'historical_initial_residual_value_inception': _("Historical Initial Residual Adjusted Value at Inception"),
    'historical_residual_value_current_period': _("Historical residual value adjusted to the current period"),
    'remaining_useful_life_at_start': _("Remaining useful life at start"),
    'historical_amortization_adjusted': _("Adjusted historical amortization"),
    'historical_residual_value_adjusted_closing': _("Historical Residual Value Adjusted at Closing"),
    'historical_residual_value_at_sap_beginning': _("Historical residual value at SAP startup"),
    'sap_historical_amortization': _("SAP Historical Amortization"),
    'sap_closing_historical_residual_value': _("Historical Residual Value at SAP Closing"),
    'historical_vri_updated_beginning_current_period': _("Difference between historical VRI updated at the beginning of the current period"),
    'depreciation_update_outside_sap': _("Depreciation Update Outside of SAP"),
    'difference_historical_vri_updated_closing': _("Difference between Historical VRI updated at closing"),
}

class ReportRevaluationHistoricalXls(models.AbstractModel):
    _name = "report.historical_assets_report.historical_asset_report_xls"
    _inherit = "report.report_xlsx.abstract"
    _description = "Asset Revaluation Historical Report XLs"


    def _write_header(self, sheet, fmt):
        row = 0
        for colnum, col in enumerate(header_to_field.values()):
            sheet.write(row, colnum, _(col), fmt)

    def generate_xlsx_report(self, workbook, data, obj):
        rows = obj.generate_entries_for_xls()

        sheet = workbook.add_worksheet(_('Historical'))
        sheet.strings_to_numbers = True
        bold = workbook.add_format({
            'bold': True,
            'align': 'center',
        })
        sheet.set_column('A:A', 1)
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 1)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 1)
        sheet.set_column('C:C', 18)
        sheet.set_column('D:D', 1)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 1)
        sheet.set_column('E:E', 15)
        sheet.set_column('F:F', 1)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 1)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 1)
        sheet.set_column('H:H', 25)
        sheet.set_column('I:I', 1)
        sheet.set_column('I:I', 15)
        sheet.set_column('J:J', 1)
        sheet.set_column('J:J', 25)
        sheet.set_column('K:K', 1)
        sheet.set_column('K:K', 15)
        sheet.set_column('L:L', 1)
        sheet.set_column('L:L', 25)
        sheet.set_column('M:M', 1)
        sheet.set_column('M:M', 25)
        sheet.set_column('N:N', 1)
        sheet.set_column('N:N', 15)
        sheet.set_column('O:O', 1)
        sheet.set_column('O:O', 25)
        sheet.set_column('P:P', 1)
        sheet.set_column('P:P', 25)
        sheet.set_column('Q:Q', 1)
        sheet.set_column('Q:Q', 25)
        sheet.set_column('R:R', 1)
        sheet.set_column('R:R', 25)
        sheet.set_column('S:S', 1)
        sheet.set_column('S:S', 25)
        self._write_header(sheet, bold)

        for rnum, row in enumerate(rows):
            for colnum, col in enumerate(header_to_field.keys()):
                sheet.write(rnum + 1, colnum, str(row.get(col)))



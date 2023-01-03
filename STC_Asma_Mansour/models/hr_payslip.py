# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo import api, fields, models, _
from odoo.tools import float_round, date_utils, convert_file, html2plaintext

class HrPayslip(models.Model):
    # """
    # Employee contract based on the visa, work permits
    # allows to configure different Salary structure
    # """

    _inherit = "hr.payslip"
    _description = "Employee Pay Slip"

    stc = fields.Boolean(string="STC", related='payslip_run_id.stc', readonly=False, store= True, help="Calcul du STC")
    paie_par_jour = fields.Boolean(string="Paie par jour", related='payslip_run_id.paie_par_jour', readonly=False, store= True)
        # (string="Paie par jour", default=lambda self: self.env['hr.payslip.run'].search([('name', 'in', self.payslip_run_id.name)], limit=1).paie_par_jour)
                                   # related='payslip_run_id.paie_par_jour', readonly=False, store= True)

    def action_print_stc(self):
        return self.env.ref('STC_Asma_Mansour.report_payslip_stc1').report_action(self)

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    stc = fields.Boolean(string="STC", store= True)
    paie_par_jour = fields.Boolean(string="Paie par jour", store= True)

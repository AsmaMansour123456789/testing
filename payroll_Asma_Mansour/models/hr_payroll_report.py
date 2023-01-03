# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from psycopg2 import sql

from odoo import tools
from odoo import fields, models


class HrPayrollReport(models.Model):
    _inherit = "hr.payroll.report"
    _description = "Payroll Analysis Report"
    # _auto = False
    # _rec_name = 'date_from'
    # _order = 'date_from desc'


    count = fields.Integer('# Payslip', group_operator="sum", readonly=True)
    count_work = fields.Integer('Work Days', group_operator="sum", readonly=True)
    count_work_hours = fields.Integer('Work Hours', group_operator="sum", readonly=True)
    count_leave = fields.Integer('Days of Paid Time Off', group_operator="sum", readonly=True)
    count_leave_unpaid = fields.Integer('Days of Unpaid Time Off', group_operator="sum", readonly=True)
    count_unforeseen_absence = fields.Integer('Days of Unforeseen Absence', group_operator="sum", readonly=True)

    name = fields.Char('Payslip Name', readonly=True)
    date_from = fields.Date('Start Date', readonly=True)
    date_to = fields.Date('End Date', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    department_id = fields.Many2one('hr.department', 'Department', readonly=True)
    job_id = fields.Many2one('hr.job', 'Job Position', readonly=True)
    number_of_days = fields.Float('Number of Days', readonly=True)
    number_of_hours = fields.Float('Number of Hours', readonly=True)
    net_wage = fields.Float('Salaire Net', readonly=True)
    basic_wage = fields.Float('Salaire de base', readonly=True)
    gross_wage = fields.Float('Salaire Brut', readonly=True)
    tfp_wage = fields.Float('TFP', readonly=True)

    cnss = fields.Float('CNSS', readonly=True)
    cnss_pat = fields.Float('CNSS Patronale', readonly=True)
    cnss_pat_avg = fields.Float('CNSS Patronale Avantage', readonly=True)
    acc_trv = fields.Float('Accident de travail', readonly=True)
    nb_jours_travailles = fields.Float('Nombre des jours travailles', readonly=True)
    prime_comp_wage = fields.Float('Prime Complémentaire', readonly=True)
    brut_impo_wage = fields.Float('Brut Imposable', readonly=True)
    foprolos_wage = fields.Float('FOPROLOS', readonly=True)
    irpp_wage = fields.Float('IRPP', readonly=True)
    css_wage = fields.Float('CSS', readonly=True)
    avance = fields.Float('Avance', readonly=True)
    pret = fields.Float('Prêt', readonly=True)
    note_frais = fields.Float('Note de frais', readonly=True)
    retenu_transp = fields.Float('Retenue', readonly=True)
    indem_transport = fields.Float('Indemnité de transport', readonly=True)
    prime_presence = fields.Float('Prime de présence', readonly=True)
    nb_jour_ferie = fields.Float('Nombre Jours Fériés', readonly=True)
    jour_ferie = fields.Float('Jours Fériés', readonly=True)
    nb_jour_conge = fields.Float('Nombre Jours Congés', readonly=True)
    jour_conge = fields.Float('Jours Congés', readonly=True)
    nb_heures_sup_100 = fields.Float('Nombre des heures supplémentaires 100%', readonly=True)
    heures_sup_100 = fields.Float('Heures supplémentaires 100%', readonly=True)
    nb_heures_sup_175 = fields.Float('Nombre des heures supplémentaires 175%', readonly=True)
    heures_sup_175 = fields.Float('Heures supplémentaires 175%', readonly=True)





    leave_basic_wage = fields.Float('Basic Wage for Time Off', readonly=True)

    work_code = fields.Many2one('hr.work.entry.type', 'Work type', readonly=True)
    work_type = fields.Selection([
        ('1', 'Regular Working Day'),
        ('2', 'Paid Time Off'),
        ('3', 'Unpaid Time Off')], string='Work, (un)paid Time Off', readonly=True)

    def _select(self):
        super(HrPayrollReport, self)._select()
        return """
            SELECT
                p.id as id,
                CASE WHEN wd.id = min_id.min_line THEN 1 ELSE 0 END as count,
                CASE WHEN wet.is_leave THEN 0 ELSE wd.number_of_days END as count_work,
                CASE WHEN wet.is_leave THEN 0 ELSE wd.number_of_hours END as count_work_hours,
                CASE WHEN wet.is_leave and wd.amount <> 0 THEN wd.number_of_days ELSE 0 END as count_leave,
                CASE WHEN wet.is_leave and wd.amount = 0 THEN wd.number_of_days ELSE 0 END as count_leave_unpaid,
                CASE WHEN wet.is_unforeseen THEN wd.number_of_days ELSE 0 END as count_unforeseen_absence,
                CASE WHEN wet.is_leave THEN wd.amount ELSE 0 END as leave_basic_wage,
                p.name as name,
                p.date_from as date_from,
                p.date_to as date_to,
                e.id as employee_id,
                e.department_id as department_id,
                c.job_id as job_id,
                e.company_id as company_id,
                wet.id as work_code,
                CASE WHEN wet.is_leave IS NOT TRUE THEN '1' WHEN wd.amount = 0 THEN '3' ELSE '2' END as work_type,
                wd.number_of_days as number_of_days,
                wd.number_of_hours as number_of_hours,
                CASE WHEN wd.id = min_id.min_line THEN pln.total ELSE 0 END as net_wage,
                CASE WHEN wd.id = min_id.min_line THEN plb.total ELSE 0 END as basic_wage,
                CASE WHEN wd.id = min_id.min_line THEN plg.total ELSE 0 END as gross_wage,
                CASE WHEN wd.id = min_id.min_line THEN plc.total ELSE 0 END as nb_jours_travailles,
                CASE WHEN wd.id = min_id.min_line THEN plt.total ELSE 0 END as tfp_wage,
                CASE WHEN wd.id = min_id.min_line THEN pla.total ELSE 0 END as cnss,
                CASE WHEN wd.id = min_id.min_line THEN pld.total ELSE 0 END as prime_comp_wage,
                CASE WHEN wd.id = min_id.min_line THEN ple.total ELSE 0 END as brut_impo_wage,
                CASE WHEN wd.id = min_id.min_line THEN plf.total ELSE 0 END as foprolos_wage,
                CASE WHEN wd.id = min_id.min_line THEN plj.total ELSE 0 END as irpp_wage,
                CASE WHEN wd.id = min_id.min_line THEN plh.total ELSE 0 END as css_wage,
                CASE WHEN wd.id = min_id.min_line THEN pli.total ELSE 0 END as avance,
                CASE WHEN wd.id = min_id.min_line THEN plk.total ELSE 0 END as pret,
                CASE WHEN wd.id = min_id.min_line THEN pll.total ELSE 0 END as note_frais,
                CASE WHEN wd.id = min_id.min_line THEN plm.total ELSE 0 END as retenu_transp,
                CASE WHEN wd.id = min_id.min_line THEN plw.total ELSE 0 END as indem_transport,
                CASE WHEN wd.id = min_id.min_line THEN plo.total ELSE 0 END as prime_presence,
                CASE WHEN wd.id = min_id.min_line THEN plp.total ELSE 0 END as nb_jour_ferie,
                CASE WHEN wd.id = min_id.min_line THEN plq.total ELSE 0 END as jour_ferie,
                CASE WHEN wd.id = min_id.min_line THEN plr.total ELSE 0 END as nb_jour_conge,
                CASE WHEN wd.id = min_id.min_line THEN pls.total ELSE 0 END as jour_conge,
                CASE WHEN wd.id = min_id.min_line THEN plu.total ELSE 0 END as nb_heures_sup_100,
                CASE WHEN wd.id = min_id.min_line THEN plv.total ELSE 0 END as heures_sup_100,
                CASE WHEN wd.id = min_id.min_line THEN plx.total ELSE 0 END as nb_heures_sup_175,
                CASE WHEN wd.id = min_id.min_line THEN ply.total ELSE 0 END as heures_sup_175,
                CASE WHEN wd.id = min_id.min_line THEN plcn.total ELSE 0 END as cnss_pat,
                CASE WHEN wd.id = min_id.min_line THEN plcp.total ELSE 0 END as cnss_pat_avg,
                CASE WHEN wd.id = min_id.min_line THEN plca.total ELSE 0 END as acc_trv
                """


    def _from(self):
        super(HrPayrollReport, self)._from()
        return """FROM
            (SELECT * FROM hr_payslip WHERE state IN ('done', 'paid')) p
                left join hr_employee e on (p.employee_id = e.id)
                left join hr_payslip_worked_days wd on (wd.payslip_id = p.id)
                left join hr_work_entry_type wet on (wet.id = wd.work_entry_type_id)
                left join (select payslip_id, min(id) as min_line from hr_payslip_worked_days group by payslip_id) min_id on (min_id.payslip_id = p.id)
                left join hr_payslip_line pln on (pln.slip_id = p.id and pln.code = 'NET')
                left join hr_payslip_line plb on (plb.slip_id = p.id and plb.code = 'BASIC')
                left join hr_payslip_line plg on (plg.slip_id = p.id and plg.code = 'GROSS')
                left join hr_payslip_line plc on (plc.slip_id = p.id and plc.code = 'NTRV')
                left join hr_payslip_line plt on (plt.slip_id = p.id and plt.code = 'TFP')
                left join hr_payslip_line pla on (pla.slip_id = p.id and pla.code = 'CNSS')
                left join hr_payslip_line pld on (pld.slip_id = p.id and pld.code = 'PC')
                left join hr_payslip_line ple on (ple.slip_id = p.id and ple.code = 'C_IMP')
                left join hr_payslip_line plf on (plf.slip_id = p.id and plf.code = 'FOPROLOS')
                left join hr_payslip_line plj on (plj.slip_id = p.id and plj.code = 'IRPP')
                left join hr_payslip_line plh on (plh.slip_id = p.id and plh.code = 'CONSS')
                left join hr_payslip_line pli on (pli.slip_id = p.id and pli.code = 'ASSIG_SALARY')
                left join hr_payslip_line plk on (plk.slip_id = p.id and plk.code = 'ATTACH_SALARY')
                left join hr_payslip_line pll on (pll.slip_id = p.id and pll.code = 'EXPENSES')
                left join hr_payslip_line plm on (plm.slip_id = p.id and plm.code = 'AR')
                left join hr_payslip_line plw on (plw.slip_id = p.id and plw.code = 'INDMT')
                left join hr_payslip_line plo on (plo.slip_id = p.id and plo.code = 'INDMPR')
                left join hr_payslip_line plp on (plp.slip_id = p.id and plp.code = 'JF')
                left join hr_payslip_line plq on (plq.slip_id = p.id and plq.code = 'C_JF')
                left join hr_payslip_line plr on (plr.slip_id = p.id and plr.code = 'JC')
                left join hr_payslip_line pls on (pls.slip_id = p.id and pls.code = 'C_JC')
                left join hr_payslip_line plu on (plu.slip_id = p.id and plu.code = 'H_S100')
                left join hr_payslip_line plv on (plv.slip_id = p.id and plv.code = 'HS100')
                left join hr_payslip_line plx on (plx.slip_id = p.id and plx.code = 'H_S')
                left join hr_payslip_line ply on (ply.slip_id = p.id and ply.code = 'HS')
                left join hr_payslip_line plcn on (plcn.slip_id = p.id and plcn.code = 'CNSSP')
                left join hr_payslip_line plcp on (plcp.slip_id = p.id and plcp.code = 'CNSSPA')
                left join hr_payslip_line plca on (plca.slip_id = p.id and plca.code = 'ACCIDENT')
                left join hr_contract c on (p.contract_id = c.id)"""

    def _group_by(self):
        return """GROUP BY
            e.id,
            e.department_id,
            e.company_id,
            wd.id,
            wet.id,
            p.id,
            p.name,
            p.date_from,
            p.date_to,
            pln.total,
            plb.total,
            plg.total,
            plc.total,
            plt.total,
            pla.total,
            pld.total,
            ple.total,
            plf.total,
            plj.total,
            plh.total,
            pli.total,
            plk.total,
            pll.total,
            plm.total,
            plw.total,
            plo.total,
            plp.total,
            plq.total,
            plr.total,
            pls.total,
            plu.total,
            plv.total,
            plx.total,
            ply.total,
            plcn.total,
            plcp.total,
            plca.total,
            min_id.min_line,
            c.id"""


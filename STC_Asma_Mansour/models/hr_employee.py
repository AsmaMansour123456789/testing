# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _,exceptions
from datetime import date, datetime, timedelta
class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"



class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

class Hrcompany(models.Model):
    # """
    # Employee contract based on the visa, work permits
    # allows to configure different Salary structure
    # """

    _inherit = 'res.company'
    _description = "Company"

    affiliation_CNSS = fields.Char(string="Affiliation CNSS")

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class HrMedicalCheckup(models.Model):
    _name = 'hr.medical.checkup'
    _description = 'Badania lekarskie pracowników'

    employee_id = fields.Many2one('hr.employee', string='Pracownik', required=True)
    checkup_date = fields.Date(string='Data badania', required=True)
    next_checkup_date = fields.Date(string='Następne badanie')
    result = fields.Selection([
        ('ok', 'OK'),
        ('fail', 'Niezdany'),
    ], string='Wynik', required=True)

    def check_expiring_checkups(self):
        today = fields.Date.today()
        expiring = self.search([('next_checkup_date', '<=', today)])
        for record in expiring:
            _logger.info(f"Badanie wygasa dla: {record.employee_id.name}")

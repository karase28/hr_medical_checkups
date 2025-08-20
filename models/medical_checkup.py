from odoo import models, fields, api
from datetime import timedelta

class HrMedicalCheckup(models.Model):
    _name = 'hr.medical.checkup'
    _description = 'Badania lekarskie pracownika'

    employee_id = fields.Many2one('hr.employee', string='Pracownik', required=True)
    checkup_date = fields.Date(string='Data badania', required=True)
    next_checkup_date = fields.Date(string='Data kolejnego badania', required=True)
    result = fields.Selection([
        ('fit', 'Zdolny do pracy'),
        ('unfit', 'Niezdolny do pracy'),
    ], string='Wynik badania', required=True)

    @api.model
    def check_expiring_checkups(self):
        today = fields.Date.today()
        reminder_date = today + timedelta(days=30)
        expiring = self.search([('next_checkup_date', '<=', reminder_date)])
        for record in expiring:
            # Tu można dodać wysyłkę maila lub powiadomienie
            _logger.info(f"Badanie dla {record.employee_id.name} wygasa {record.next_checkup_date}")

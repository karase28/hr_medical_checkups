from odoo import models, fields
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class HrMedicalCheckup(models.Model):
    _name = 'hr.medical.checkup'
    _description = 'Badania lekarskie pracowników'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # umożliwia logi i powiadomienia

    employee_id = fields.Many2one('hr.employee', string='Pracownik', required=True)
    checkup_date = fields.Date(string='Data badania', required=True)
    next_checkup_date = fields.Date(string='Następne badanie')
    result = fields.Selection([
        ('ok', 'OK'),
        ('fail', 'Niezdany'),
    ], string='Wynik', required=True)

    def check_expiring_checkups(self):
        """Sprawdza badania wygasające w ciągu 30 dni i publikuje alerty w kanale Odoo"""
        today = fields.Date.today()
        limit_date = today + timedelta(days=30)
        expiring = self.search([
            ('next_checkup_date', '!=', False),
            ('next_checkup_date', '<=', limit_date),
        ])

        if not expiring:
            return

        # znajdź lub stwórz kanał do komunikacji
        channel = self.env['mail.channel'].search([('name', '=', 'HR – Badania lekarskie')], limit=1)
        if not channel:
            channel = self.env['mail.channel'].create({
                'name': 'HR – Badania lekarskie',
                'channel_type': 'channel',
                'public': 'private',
            })

        # wyślij wiadomości dla każdego wygasającego badania
        for record in expiring:
            msg = f"⚠️ Badania lekarskie pracownika <b>{record.employee_id.name}</b> wygasają w dniu <b>{record.next_checkup_date}</b>."
            channel.message_post(body=msg, subtype_xmlid="mail.mt_comment")
            _logger.info("Wysłano przypomnienie do kanału HR – Badania lekarskie: %s", msg)

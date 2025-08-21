from odoo import models, fields
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class HrMedicalCheckup(models.Model):
    _name = 'hr.medical.checkup'
    _description = 'Badania lekarskie pracowników'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Pracownik', required=True)
    checkup_date = fields.Date(string='Data badania', required=True)
    next_checkup_date = fields.Date(string='Następne badanie')
    result = fields.Selection([
        ('ok', 'OK'),
        ('fail', 'Niezdany'),
    ], string='Wynik', required=True)

    def check_expiring_checkups(self):
        """Sprawdza badania wygasające w ciągu 30 dni,
        wysyła alert do kanału i zakłada aktywność HR"""
        today = fields.Date.today()
        limit_date = today + timedelta(days=30)
        expiring = self.search([
            ('next_checkup_date', '!=', False),
            ('next_checkup_date', '<=', limit_date),
        ])

        if not expiring:
            return

        # znajdź lub stwórz kanał
        channel = self.env['mail.channel'].search([('name', '=', 'HR – Badania lekarskie')], limit=1)
        if not channel:
            channel = self.env['mail.channel'].create({
                'name': 'HR – Badania lekarskie',
                'channel_type': 'channel',
                'public': 'private',
            })

        # znajdź grupę HR i weź jej użytkowników
        hr_group = self.env.ref('hr.group_hr_user', raise_if_not_found=False)
        hr_users = hr_group.users if hr_group else self.env.user

        for record in expiring:
            msg = f"⚠️ Badania lekarskie pracownika <b>{record.employee_id.name}</b> wygasają {record.next_checkup_date}."
            channel.message_post(body=msg, subtype_xmlid="mail.mt_comment")

            # utwórz aktywności dla HR
            for user in hr_users:
                record.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    note=f"Wysłać pracownika {record.employee_id.name} na badania lekarskie (do {record.next_checkup_date})."
                )

            _logger.info("Dodano przypomnienie i aktywności HR dla: %s", record.employee_id.name)

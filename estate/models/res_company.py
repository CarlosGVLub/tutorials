from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    expiration_date = fields.Date(string="Fecha de Expiración de la Licencia")
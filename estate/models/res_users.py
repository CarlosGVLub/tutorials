from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string="Propiedades en Venta")
    is_property_manager = fields.Boolean(string="Es Gestor de Propiedades")
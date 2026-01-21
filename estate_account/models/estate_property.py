from odoo import models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        print("La propiedad ha sido vendida. Procesando acciones contables...")
        return super().action_set_sold()
    
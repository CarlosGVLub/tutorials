from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    
    name = fields.Char(string="Tipo de Propiedad", required=True)
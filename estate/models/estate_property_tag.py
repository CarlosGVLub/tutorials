from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag Model"
    
    name = fields.Char(string="Etiqueta", required=True)

    _check_name_unique = models.Constraint(
        'UNIQUE(name)',
        'El nombre de la etiqueta debe ser único.'
    )
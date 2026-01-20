from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type Model"
    _order = "sequence asc"
    
    name = fields.Char(string="Tipo de Propiedad", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Propiedades")
    sequence = fields.Integer(string="Secuencia", default=1, help="Determina el orden de los tipos de propiedad en las vistas.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Ofertas Relacionadas")
    offer_count = fields.Integer(string="Número de Ofertas", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
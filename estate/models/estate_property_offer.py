from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    
    price = fields.Float(string="Precio de la Oferta", required=True, digits=(12, 2))
    status = fields.Selection(
        string="Estatus de la Oferta",
        selection=[
            ('accepted', 'Aceptada'),
            ('refused', 'Rechazada')
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Comprador", required=True)
    property_id = fields.Many2one("estate.property", string="Propiedad", required=True)
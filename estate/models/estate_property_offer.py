from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

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
    validity = fields.Integer(string="Validez (días)", default=7)
    date_deadline = fields.Date(string="Fecha Límite", compute="_compute_date_deadline", store=True)

    _check_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'El precio de la oferta debe ser mayor que cero.'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in ['sold', 'cancelled']:
                raise UserError("No se puede aceptar una oferta para una propiedad que ya ha sido vendida o cancelada.")
            # Rechazar otras ofertas
            other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id)])
            other_offers.write({'status': 'refused'})
            # Aceptar esta oferta
            offer.status = 'accepted'
            # Actualizar la propiedad
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id.id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            
            # Revisar si hay otras ofertas, si hay, marcar la propiedad como 'offer_received'
            other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id), ('status', '!=', 'refused')])
            if other_offers:
                offer.property_id.state = 'offer_received'
            else:
                offer.property_id.state = 'new'

        return True
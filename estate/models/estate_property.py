from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    _order = "id desc"
    
    name = fields.Char(string="Nombre de la propiedad", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Disponible Desde", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Precio Esperado", required=True, digits=(12, 2))
    selling_price = fields.Float(string="Precio de Venta", digits=(12, 2), readonly=True, copy=False)
    bedrooms = fields.Integer(string="Número de Dormitorios", default=2)
    living_area = fields.Integer(string="Área Habitable (m²)")
    facades = fields.Integer(string="Número de Fachadas")
    garage = fields.Boolean(string="Garaje")
    garden = fields.Boolean(string="Jardín")
    garden_area = fields.Integer(string="Área del Jardín (m²)")
    garden_orientation = fields.Selection(
        string="Orientación del Jardín",
        selection=[
            ('north', 'Norte'),
            ('south', 'Sur'),
            ('east', 'Este'),
            ('west', 'Oeste')
        ]
    )
    active = fields.Boolean(string="Activo", default=True)
    state = fields.Selection(
        string="Estatus",
        selection=[
            ('new', 'Nuevo'),
            ('offer_received', 'Oferta Recibida'),
            ('offer_accepted', 'Oferta Aceptada'),
            ('sold', 'Vendido'),
            ('cancelled', 'Cancelado')
        ],
        required=True,
        copy=False,
        default='new'
    )
    property_type_id = fields.Many2one("estate.property.type", string="Tipo de Propiedad")
    buyer_id = fields.Many2one("res.partner", string="Comprador", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag", string="Etiquetas")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Ofertas")
    total_area = fields.Integer(string="Área Total (m²)", compute="_compute_total_area")
    best_price = fields.Float(string="Mejor Precio", compute="_compute_best_price")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'El precio esperado debe ser mayor que cero.'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'El precio de venta no puede ser negativo o cero.'
    )

    @api.model
    def create(self, vals):
        if 'selling_price' in vals and vals['selling_price'] > 0:
            raise ValidationError("No se puede establecer el precio de venta al crear una propiedad.")
        return super().create(vals)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        for record in self:
            # It should not be possible to delete a property which is not new or cancelled
            if record.state not in ['new', 'cancelled']:
                raise UserError("No se puede eliminar una propiedad que no esté en estado 'nuevo' o 'cancelado'.")

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                minimum_price = record.expected_price * 0.9
                if float_compare(record.selling_price, minimum_price, precision_digits=2) < 0:
                    raise ValidationError("El precio de venta debe ser al menos el 90% del precio esperado.")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    # @api.depends('garden_area')
    # def _compute_garden(self):
    #     for record in self:
    #         record.garden = record.garden_area > 0

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if not record.garden:
                record.garden_area = 0
                record.garden_orientation = False
            else:
                record.garden_area = 10
                record.garden_orientation = 'north'

    def action_set_sold(self):
        for property in self:
            if property.state != 'offer_accepted':
                raise UserError("Solo se puede marcar como vendida una propiedad con una oferta aceptada.")
            property.state = 'sold'
        return True

    def action_set_canceled(self):
        for property in self:
            if property.state in ['sold', 'cancelled']:
                raise UserError("No se puede cancelar una propiedad que ya ha sido vendida o cancelada.")
            property.state = 'cancelled'
        return True
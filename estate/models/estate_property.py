from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"
    
    name = fields.Char(string="Nombre de la propiedad", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Disponible Desde", copy=False, default=fields.Date.today() + relativedelta(months=3))
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
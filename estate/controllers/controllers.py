from odoo import http, fields
from odoo.http import request
import json
from datetime import timedelta

class EstateRegistration(http.Controller):

    @http.route('/api/register_estate', auth='public', methods=['POST'], csrf=False, cors='*', type='jsonrpc')
    def register_new_client(self, **post):
        # Recibimos datos del JSON
        data = request.params

        name = data.get('name')
        email = data.get('email')
        company_name = data.get('company_name')

        # 1. Crear la Compañía (El "Taller" o "Inmobiliaria")
        new_company = request.env['res.company'].sudo().create({
            'name': company_name,
            'expiration_date': fields.Date.today() + timedelta(days=15)
        })

        # 2. Crear el Usuario y asignarle la nueva compañía
        new_user = request.env['res.users'].sudo().create({
            'name': name,
            'login': email,
            'email': email,
            'company_id': new_company.id,
            'company_ids': [(4, new_company.id)],
        })
        
        # Asignar el grupo de usuario interno
        group_user = request.env.ref('base.group_user')
        new_user.sudo().write({'group_ids': [(4, group_user.id)]})

        new_user.sudo().action_reset_password()

        return {
            'status': 'success',
            'message': 'Correo de activación enviado a {}'.format(email)
        }
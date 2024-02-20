from datetime import timedelta
from odoo import api, exceptions, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "id desc"

    property_id = fields.Many2one('estate.property', string='Property', required=True)
    price = fields.Float(string='Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)

    # Check it
    # https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started/12_sprinkles.html#stat-buttons
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type',
        related='property_id.property_type_id',
        store=True,
        readonly=True
    )

    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='pending')

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state == 'new' or offer.property_id.state == 'offer_received':
                offer.property_id.write({
                    'buyer_id': offer.partner_id.id,
                    'selling_price': offer.price,
                    'state': 'sold',
                })
                offer.write({'status': 'accepted'})
            else:
                raise exceptions.UserError(("An offer can only be accepted for a property in 'new' or 'offer received' state."))
        return True

    def action_refuse(self):
        for offer in self:
            offer.write({'status': 'refused'})
        return True

    _sql_constraints = [
        ('price_positive', 'CHECK (price >  0)', 'The offer price must be positive!'),
    ]

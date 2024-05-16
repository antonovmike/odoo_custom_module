from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    name = fields.Char(string="Field", required=True)
    type = fields.Selection(
        [('new', 'New'), ('used', 'Used'), ('renovated', 'Renovated')], default='new'
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type names must be unique!'),
    ]

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

    # Check it
    # https://www.odoo.com/documentation/16.0/developer/tutorials/getting_started/12_sprinkles.html#stat-buttons
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(
        string='Offer Count',
        compute='_compute_offer_count'
    )

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

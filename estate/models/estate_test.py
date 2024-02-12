from dateutil.relativedelta import relativedelta
from odoo import fields, models
from odoo.fields import Datetime

class TestModel(models.Model):
    _name = "estate.property"
    _description = "Estate test module"

    date_in_three_months = Datetime.today() + relativedelta(months=3)

    name = fields.Char(required=True, default="Alice")
    description = fields.Text(required=True, help="Please describe the estate")
    postcode = fields.Char(required=True)
    date_availability = fields.Date(default=date_in_three_months, copy=False)
    expected_price = fields.Float(required=True, help="Enter the price")
    selling_price = fields.Float(required=True, copy=False)
    bedrooms = fields.Integer(default=0)
    living_area = fields.Integer(default=1)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer(default=0)
    garden_orientation = fields.Selection(
        [('east', 'East'), ('south', 'South'), ('west', 'West'), ('north', 'North')], required=False
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new'
    )

    property_type_id = fields.Many2one('estate.property.type', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=False,
        help="The person who bought the property",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        required=True,
        help="The user who sold the property",
        default=lambda self: self.env.user,
        copy=False,
    )

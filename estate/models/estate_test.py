from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models
from odoo.fields import Datetime
from odoo.tools.float_utils import float_compare, float_is_zero

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

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

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

    commission = fields.Float(compute="_compute_commission")

    @api.depends('selling_price')
    def _compute_commission(self):
        percent = 0.1
        for record in self:
            record.commission = record.selling_price * percent

    total_area = fields.Integer(compute="_compute_total_area", store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(compute="_compute_best_price", store=True)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise exceptions.UserError(("Cannot cancel a sold property."))
        return True

    def action_sell(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
            else:
                raise exceptions.UserError(("Cannot sell a canceled property."))
        return True

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag names must be unique!'),
        ('expected_price_positive', 'CHECK (expected_price >  0)', 'The expected price must be positive!'),
        ('selling_price_positive', 'CHECK (selling_price >=  0)', 'The selling price must be positive!'),
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.expected_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price *  0.9, precision_digits=2) <  0:
                    raise exceptions.ValidationError(("The selling price cannot be lower than  90% of the expected price."))

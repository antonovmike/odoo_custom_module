from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Field", required=True)
    type = fields.Selection(
        [('new', 'New'), ('used', 'Used'), ('renovated', 'Renovated')], default='new'
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Property type names must be unique!'),
    ]

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')

from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Field", required=True)
    type = fields.Selection(
        [('new', 'New'), ('used', 'Used'), ('renovated', 'Renovated')], default='new'
    )

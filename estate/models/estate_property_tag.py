from odoo import fields, models

class TagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for Real Estate Properties"
    _order = "name"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Tag names must be unique!'),
    ]

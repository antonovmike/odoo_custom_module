from odoo import fields, models

class TagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for Real Estate Properties"
    # _columns = []

    name = fields.Char(string="Name", required=True)
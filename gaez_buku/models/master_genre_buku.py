from odoo import models, fields, api, _

class GaezGenreBuku(models.Model):
    _name = 'gaez.genre.buku'
    _description = 'Master Genre Buku'
    _rec_name = 'name'

    name = fields.Char(string="Genre Buku")
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GaezBuku(models.Model):
    _name = 'gaez.buku'
    _description = 'Master Data Buku'
    _rec_name = 'name'

    name = fields.Char(string="Judul Buku", required=True)
    penulis = fields.Char(string="Penulis", required=True)
    terbit = fields.Char(string="Tahun Terbit", required=True) 
    genre = fields.Many2many(comodel_name='gaez.genre.buku', string="Genre") 
    is_skripsi = fields.Boolean(string="Skripsi?", default=False)
    denda = fields.Float(string="Denda", required=True)

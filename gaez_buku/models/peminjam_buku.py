from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError

class PeminjamBuku(models.Model):
    _name = 'gaez.peminjam.buku'
    _description = 'Peminjam Buku'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user, required=True)
    buku_id = fields.Many2one(comodel_name='gaez.buku', string="Buku", required=True)
    genre_ids = fields.Many2many(comodel_name='gaez.genre.buku', string="Genre")
    fakultas = fields.Selection([('fti', 'FTI'),('feb', 'FEB')], string="Fakultas")
    angkatan = fields.Integer(string="Angkatan")
    tanggal_pinjam = fields.Date(string="Tanggal Pinjam", default=fields.Date.today())
    today = fields.Date(string="Today", default=fields.Date.today(), invisible=True)
    tanggal_pengembalian = fields.Date(string="Tanggal Pengembalian")
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirm'),
            ('approved', 'Approved'),
            ('pinalty', 'Pinalty'),
            ('closed', 'Closed')
        ], string='Status', default='draft', track_visibility='onchange')
    denda = fields.Float(string="Denda", compute='_compute_denda', store=True)

    @api.onchange('buku_id')
    def _onchange_buku_id(self):
        for rec in self:
            if rec.buku_id:
                rec.genre_ids = rec.buku_id.genre

    @api.onchange('tanggal_pengembalian')
    def _onchange_tanggal_pengembalian(self):
        for rec in self:
            if rec.tanggal_pengembalian and rec.tanggal_pinjam:
                tanggal_pinjam = rec.tanggal_pinjam
                tanggal_pengembalian = rec.tanggal_pengembalian
                if rec.buku_id.is_skripsi == False and tanggal_pengembalian > tanggal_pinjam + timedelta(days=7):
                    raise UserError('Tidak Boleh Meminjam Buku Lebih Dari 7 Hari')
                if rec.buku_id.is_skripsi:
                    if tanggal_pengembalian > tanggal_pinjam + timedelta(days=30):
                        raise UserError('Tidak Boleh Meminjam Buku Skripsi Lebih Dari 30 Hari')
                
    @api.depends('tanggal_pengembalian', 'today')
    def _compute_denda(self):
        for rec in self:
            if rec.tanggal_pengembalian:
                if rec.tanggal_pengembalian > rec.today:
                    selisih_hari = (rec.tanggal_pengembalian - rec.today).days
                    tarif_denda = rec.buku_id.denda
                    rec.denda = selisih_hari * tarif_denda
                else:
                    rec.denda = 0.0

    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    def action_approved(self):
        self.write({'state': 'approved'})
    
    def action_pinalty(self):
        self.write({'state': 'pinalty'})

    def set_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_closed(self):
        self.write({'state': 'closed'})
        
    @api.model
    def _cron_compute_penalty(self):
        for rec in self:
            telat = self.search([('state', '=', 'confirm'), ('tanggal_pengembalian', '>', rec.today)])
            if telat:
                telat.write({'state' : 'pinalty'})

from odoo import models, fields, api, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PeminjamBuku(models.Model):
    _name = 'gaez.peminjam.buku'
    _description = 'Peminjam Buku'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.user, required=True)
    email = fields.Char(string="Email")
    buku_id = fields.Many2one(comodel_name='gaez.buku', string="Buku", required=True, domain=[('stock', '>=', 1)])
    stock_buku = fields.Integer(string="Stok Buku")
    genre_ids = fields.Many2many(comodel_name='gaez.genre.buku', string="Genre")
    fakultas = fields.Selection([('fti', 'FTI'),('feb', 'FEB')], string="Fakultas")
    angkatan = fields.Integer(string="Angkatan")
    tanggal_pinjam = fields.Date(string="Tanggal Pinjam", default=fields.Date.today())
    tanggal_pengembalian = fields.Date(string="Pengembalian")
    today = fields.Date(string="Today", default=fields.Date.today())
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
                rec.stock_buku = rec.buku_id.stock
                if rec.buku_id.stock == 0:
                    raise UserError('Stok dari buku yang anda pilih tidak tersedia')

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
                
    @api.depends('tanggal_pengembalian')
    def _compute_denda(self):
        for rec in self:
            if rec.tanggal_pengembalian:
                if rec.tanggal_pengembalian > rec.today:
                    selisih_hari = (rec.tanggal_pengembalian - rec.today).days
                    tarif_denda = rec.buku_id.denda
                    rec.denda = selisih_hari * tarif_denda
                else:
                    rec.denda = 0.0

    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if '@' not in rec.email or '.' not in rec.email:
                raise UserError('Alamat email tidak valid. Mohon pastikan alamat email memiliki karakter "@" dan "."')

    def action_confirm(self):
        self.write({'state': 'confirm'})
        
    def action_approved(self):
        stok = self.env['gaez.buku'].sudo().search([('name', '=', self.buku_id.name)], limit=1)
        if stok:
            self.stock_buku -= 1
            stok.stock -= 1
        self.write({'state': 'approved'})
    
    def action_pinalty(self):
        self.write({'state': 'pinalty'})

    def set_to_draft(self):
        self.write({'state': 'draft'})
    
    def action_closed(self):
        stok = self.env['gaez.buku'].sudo().search([('name', '=', self.buku_id.name)], limit=1)
        if stok:
            self.stock_buku += 1
            stok.stock += 1
        self.write({'state': 'closed'})
        
    def _cron_compute_penalty(self):
        telat_records = self.search([('state', '=', 'approved'), ('tanggal_pengembalian', '>', fields.Date.today())])
        telat_records.write({'state': 'pinalty'})
        for rec in telat_records:
            rec.action_send_overdue_email()

    def action_send_overdue_email(self):
        template = self.env.ref('gaez_buku.pinalty_buku_reminder')
        for rec in self:
            if rec.email:
                template.send_mail(rec.id, force_send=True, email_values={'email_to': rec.email})


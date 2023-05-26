from odoo import tools
from odoo import fields, models
import odoo.addons.decimal_precision as dp
import time
import logging
from odoo.tools.translate import _
from odoo import api
from odoo.exceptions import UserError, Warning


_logger = logging.getLogger(__name__)
SPP_STATES =[('draft','Draft'),('open','Verifikasi'), ('reject','Ditolak'),
                 ('done','Disetujui')]

class spp(models.Model):
    _name       = 'anggaran.spp'

    def _spm_exists(self):
        for spp in self:
            spp.spm_exists = False
            if spp.spm_ids:
                spp.spm_exists = True


    name                = fields.Char('Nomor', required=True, readonly=True, default='/')
    tanggal             = fields.Date('Tanggal', required=True, default=lambda self: time.strftime("%Y-%m-%d"))
    period_id           = fields.Many2one(comodel_name='account.period', string='Perioda', compute='_fperiode', store=True,)
    tahun_id            = fields.Many2one(comodel_name='account.fiscal.year', string='Tahun')
    kepada              = fields.Char('Kepada', required=True)
    unit_id             = fields.Many2one(comodel_name='vit.unit_kerja', string='SUBSATKER', required=True)
    rka_id              = fields.Many2one(comodel_name='anggaran.rka', string='Dasar Anggaran', required=True)
    # 'dasar_rkat'      : fields.Char('Dasar RKAT Nomor/Tanggal', required=True),
    jumlah              = fields.Float('Jumlah Pembayaran', required=True)
    keperluan           = fields.Char('Untuk Keperluan', required=True)
    cara_bayar          = fields.Selection([('tup','UUDP'),('ls','Pembayaran LS')],
                            'Cara Bayar',required=True)
    # 'cara_bayar'        : fields.selection([('tup','TUP'),('gup','GUP'),('ls','Pembayaran LS')],
    #                       'Cara Bayar',required=True),
    alamat              = fields.Text('Alamat')
    nomor_rek           = fields.Char('Nomor Rekening')
    nama_bank           = fields.Char('Nama Bank')
    spp_line_ids        = fields.One2many(comodel_name='anggaran.spp_line',inverse_name='spp_id',string='Penjelasan', ondelete="cascade")
    pumkc_id            = fields.Many2one(comodel_name='hr.employee', string='PUMKC')
    nip_pumkc           = fields.Char(comodel_name='hr.employee', related='pumkc_id.nip', string='NIP PUMKC', store=True, readonly=True)
    atasan_pumkc_id     = fields.Many2one(comodel_name='hr.employee', string='Atasan Langsung PUMKC')
    nip_atasan_pumkc    = fields.Char(comodel_name='hr.employee', related='atasan_pumkc_id.nip', string='NIP Atasan PUMKC', store=True, readonly=True)
    user_id             = fields.Many2one(comodel_name='res.users', string='Created', required=True, readonly=True, default=lambda self: self.env.uid)
    state               = fields.Selection(selection=SPP_STATES, string='Status', readonly=True, required=True, default=SPP_STATES[0][0])
    sptb_id             = fields.Many2one(comodel_name='anggaran.sptb', string='SPTB')
    spm_ids             = fields.One2many(comodel_name='anggaran.spm',inverse_name='spp_id',string='SPM')
    spm_exists          = fields.Boolean(compute='_spm_exists', string='SPM Sudah Tercatat', type='boolean', help="Apakah SPP ini sudah dicatatkan SPM-nya.")       

    @api.depends('tahun_id')
    def _fperiode(self):
        periode = ''
        for spp in self:
            periode = int(spp.tahun_id.name) + 1
            acc_periode = spp.env['account.period'].search([('name','=',str(periode))])
            # import pdb; pdb.set_trace()
            if acc_periode:
                spp.period_id = acc_periode.id

    @api.multi
    def action_draft(self):
        #set to "draft" state
        return self.write({'state':SPP_STATES[0][0]})

    @api.multi
    def action_confirm(self):
        #set to "confirmed" state
        return self.write({'state':SPP_STATES[1][0]})

    @api.multi
    def action_reject(self):
        #set to "done" state
        return self.write({'state':SPP_STATES[2][0]})

    @api.multi
    def action_done(self):
        #set to "done" state

        #update realisasi di rka_detail.realisasi
        #dari spp -> spp_line -> spp_line_mak.rka_coa_id dengan nilai spp_ini
        for spp in self:            
            for spp_line in spp.spp_line_ids:               
                for spp_line_mak in spp_line.spp_line_mak_ids:
                    sql = "UPDATE anggaran_rka_coa SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE id = '%s' AND rka_kegiatan_id = '%s'" % (spp_line_mak.spp_ini, spp_line_mak.spp_ini, spp_line_mak.rka_coa_id.id, spp_line.rka_kegiatan_id.id)
                    self.env.cr.execute(sql)
                sql1 = "UPDATE anggaran_rka_kegiatan SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE id = '%s' AND rka_id = '%s'" % (spp_line.spp_ini, spp_line.spp_ini, spp_line.rka_kegiatan_id.id, spp.rka_id.id)
                self.env.cr.execute(sql1)
            sql2 = "UPDATE anggaran_rka SET realisasi = coalesce(realisasi,0) + '%s', sisa = coalesce(sisa,0) - '%s' WHERE unit_id = '%s' AND id = '%s'" % (spp.jumlah, spp.jumlah, spp.unit_id.id, spp.rka_id.id)
            self.env.cr.execute(sql2)

        return self.write({'state':SPP_STATES[3][0]})

    @api.model
    def create(self, vals):
        vals['name']    = self.env['ir.sequence'].next_by_code('anggaran.spp')
        return super(spp, self).create(vals)

    @api.multi
    def action_create_spm(self):
        for spp in self:
        #############################################################
        # cari rka utk unit_id
        #############################################################
            cr = self.env.cr
            sql = """SELECT kg.indikator, sum(sl.pagu), sum(sl.spp_lalu), sum(sl.spp_ini), sum(sl.jumlah_spp), sum(sl.sisa_dana)
                    FROM anggaran_spp_line sl
                    LEFT JOIN anggaran_rka_kegiatan kg ON sl.rka_kegiatan_id = kg.id
                    WHERE sl.spp_id = %s
                    GROUP BY kg.indikator
                    """
            cr.execute(sql, (spp.id,))
            result = cr.fetchall()
            spm_line_ids = []
            for res in result:
                spm_line_ids.append((0,0,{
                        'kegiatan'      : res[0],
                        'pagu'          : res[1],
                        'up_sd_lalu'    : res[2],
                        'up_ini'        : res[3],
                        'jumlah_up'     : res[4],
                        'sisa_dana'     : res[5],
                    }))

            spm_obj = self.env["anggaran.spm"]
            data = {
                'name'          : '/',
                'tanggal'       : time.strftime("%Y-%m-%d") ,
                'cara_bayar'    : 'gup',
                'unit_id'       : spp.unit_id.id,
                'tahun_id'      : spp.tahun_id.id,
                'jumlah'        : spp.jumlah,
                'sisa'          : sum(map(lambda x: x.sisa_dana, spp.spp_line_ids)),
                'user_id'       : self.env.uid, 
                'state'         : 'draft',
                'spp_id'        : spp.id,
                'spm_line_ids'  : spm_line_ids
            }
            spm_id = spm_obj.create(data)
            return spm_id

    @api.multi
    def action_view_spm(self):
        spms = self.mapped('spm_ids')
        action = self.env.ref('anggaran.action_spm_list').read()[0]
        # if len(spms) > 1:
        #   action['domain'] = [('id', 'in', ["+','.join(map(str, spms))+"])]
        if len(spms) == 1:
            form_view = [(self.env.ref('anggaran.view_spm_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = spms.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.onchange('spp_line_ids') 
    def on_change_spp_line_ids(self):
        jumlah = 0.0
        for line in self.spp_line_ids:
            jumlah += line.spp_ini 
        self.jumlah = jumlah 


    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != SPP_STATES[0][0]:
                raise UserError("Tidak bisa dihapus selain dalam status Rancangan!")
        return super(spp, self).unlink()

class spp_line(models.Model):
    _name       = "anggaran.spp_line"
    _rec_name   = "rka_kegiatan_id"

    spp_id              = fields.Many2one(comodel_name='anggaran.spp', string='SPP')
    rka_kegiatan_id     = fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan Bersangkutan')
    pagu                = fields.Float('PAGU')
    spp_lalu            = fields.Float("SPP sd yg Lalu")
    spp_ini             = fields.Float("SPP ini")
    jumlah_spp          = fields.Float("Jumlah SPP")
    sisa_dana           = fields.Float("Sisa Dana")
    spp_line_mak_ids    = fields.One2many(comodel_name='anggaran.spp_line_mak',inverse_name='spp_line_id',string='MAKs', ondelete="cascade")


    @api.onchange('rka_kegiatan_id','spp_ini') 
    def on_change_rka_kegiatan_id(self):
        self.pagu       = self.rka_kegiatan_id.anggaran
        self.spp_lalu   = self.rka_kegiatan_id.realisasi
        self.jumlah_spp = self.spp_lalu + self.spp_ini 
        self.sisa_dana  = self.pagu - self.jumlah_spp

    @api.onchange('spp_line_mak_ids') 
    def on_change_spp_line_mak_ids(self):
        total_spp_ini = 0.0
        for line in self.spp_line_mak_ids:
            total_spp_ini = total_spp_ini + line.spp_ini

        self.spp_ini = total_spp_ini


class spp_line_mak(models.Model):
    _name       = "anggaran.spp_line_mak"

    spp_line_id     = fields.Many2one(comodel_name='anggaran.spp_line', string='SPP Line')
    rka_coa_id      = fields.Many2one(comodel_name='anggaran.rka_coa', string='MAK')
    pagu            = fields.Float('PAGU')
    spp_lalu        = fields.Float("SPP sd yg Lalu")
    spp_ini         = fields.Float("SPP ini", required=True)
    jumlah_spp      = fields.Float("Jumlah SPP")
    sisa_dana       = fields.Float("Sisa Dana")
    rka_kegiatan_id = fields.Many2one(comodel_name='anggaran.rka_kegiatan', string='Kegiatan Bersangkutan', related='spp_line_id.rka_kegiatan_id')


    @api.onchange('rka_coa_id','spp_ini')
    def on_change_rka_coa_id(self):
        self.pagu       = self.rka_coa_id.total
        self.spp_lalu   = self.rka_coa_id.realisasi
        self.jumlah_spp = self.spp_lalu + self.spp_ini
        self.sisa_dana  = self.pagu - self.jumlah_spp


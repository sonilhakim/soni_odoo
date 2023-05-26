

#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
import time
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
STATES=[('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel'), ('partial', 'Partial Done'), ('done', 'Done')]

class KasirStore(models.Model):

    _name = "vit.kasir_store"
    _description = "vit.kasir_store"
    _order = 'date desc, id desc'
    _inherit = ['mail.thread']

    @api.model
    def _get_default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'kasir_store')],
            limit=1).id

    @api.depends('summary_lines', 'store_lines.lot_id_sumber','store_lines.lot_id_target')
    def _get_count(self):
        count = self.store_lines.filtered(lambda line:line.lot_id_sumber and line.lot_id_target)
        self.count = len(count)

    name                = fields.Char( readonly=True, required=True, default='New', string="Name",  help="")
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="State",track_visibility='onchange',  help="")
    date                = fields.Date( string="Date", default=lambda self: time.strftime("%Y-%m-%d"), readonly=True, states={"draft" : [("readonly",False)]},track_visibility='onchange', help="")
    project             = fields.Char( string="Project", help="", readonly=True, states={"draft" : [("readonly",False)]},track_visibility='onchange' )
    notes               = fields.Text( string="Notes",  help="", readonly=True, states={"draft" : [("readonly",False)]},track_visibility='onchange' )    
    
    po_id               = fields.Many2one(comodel_name="vit.purchase_order_garmen", string="No. OR", readonly=True, states={"draft" : [("readonly",False)]},track_visibility='onchange')
    partner_id          = fields.Many2one( comodel_name="res.partner",  string="Customer", readonly=True, states={"draft" : [("readonly",False)]},track_visibility='onchange',  help="")
    user_id             = fields.Many2one("res.users", "User", default=lambda self: self.env.uid, track_visibility='onchange')
    store_lines         = fields.One2many(comodel_name="vit.kasir_store_line",  inverse_name="store_id",  string="Lines",  help="", readonly=True, states={"draft" : [("readonly",False)]},)
    summary_lines       = fields.One2many(comodel_name="vit.summary_polybag_store",  inverse_name="store_id",  string="Summary",  help="")
    barcode             = fields.Char('Barcode', help="Jika scan otomatis bermasalah, maka letakan kursor disini")
    barcode_repair      = fields.Char('Barcode Repair', help="Jika scan otomatis bermasalah, maka letakan kursor disini")
    warning             = fields.Text('Warning', help="warning message")
    warning_repair      = fields.Text('Warning Repair', help="warning message")
    count               = fields.Integer('Count', compute="_get_count", help="Jumlah data yang lengkap sudah di scan")
    repair_ids          = fields.One2many('vit.kasir_repair_line', 'store_id', readonly=True, states={"partial" : [("readonly",False)]})
    unvalidate_ids      = fields.One2many('vit.kasir_store_line', 'store_id', domain=[('unvalidate','=',True)], readonly=True, states={"partial" : [("readonly",False)]})
    show_unvalidate     = fields.Boolean('Show Unvalidate')

    picking_type_id     = fields.Many2one('stock.picking.type', 'Operation Type', default=_get_default_picking_type, required=True)
    
    @api.model
    def create(self, vals):
        if not vals.get('name', False) or vals['name'] == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('vit.kasir_store') or 'Error Number!!!'
        return super(KasirStore, self).create(vals)

    @api.onchange('po_id')
    def onchange_or(self):
        if self.po_id:
            self.partner_id = self.po_id.partner_id
            self.project = self.po_id.sph_id.proposal_id.inquery_id.name

    @api.multi 
    def action_draft(self):
        self.state = STATES[0][0]

    @api.multi 
    def action_confirm(self):
        for rec in self.store_lines:
            # if not rec.lot_id_target:
            #     raise UserError(_("Polybag belum lengkap!"))
            # else:
            #     self.state = STATES[1][0]
            self.state = STATES[1][0]

    @api.multi 
    def action_cancel(self):
        # for rec in self.store_lines:
        #     if rec.is_swap:
        #         rec.reverse_swap()
        self.state = STATES[2][0]

    @api.multi 
    def action_done(self):
        self.ensure_one()
        # cek unvalidate
        if self.unvalidate_ids:
            raise UserError(_("Ada data yang belum repair!"))
        # cek lines
        if self.store_lines.filtered(lambda line:not line.lot_id_target or not line.lot_id_sumber):
            raise UserError(_("Baris polybag ada yang belum lengkap/terisi !"))
        has_line_swap = []
        for swap_lot in self.store_lines.filtered(lambda sl: sl.is_not_same == True and sl.is_swap == False):
            if swap_lot:
                if (swap_lot.lot_id_sumber.id not in has_line_swap) and (swap_lot.lot_id_target.id not in has_line_swap):
                    swap_lot.swap_barcode()
                    has_line_swap.append(swap_lot.lot_id_sumber.id)
                    has_line_swap.append(swap_lot.lot_id_target.id)

        for rec in self.store_lines:
            done_time = datetime.now()
            if rec.is_not_same == True:
                if rec.is_swap == True:
                    sql = """
                        update stock_production_lot set store = true, date_done_store = %s
                        where id = %s
                        """
                    self.env.cr.execute(sql, (done_time,rec.lot_id_target.id,))
                else:
                    pass
            else:
                sql = """
                    update stock_production_lot set store = true, date_done_store = %s
                    where id = %s
                    """
                self.env.cr.execute(sql, (done_time,rec.lot_id_target.id,))

        fail_lines = self.store_lines.search([('lot_id_target.store','=',False),('store_id','=',self.id)])
        if fail_lines:
            for fl in fail_lines:
                fl.unvalidate = True
            self.show_unvalidate = True
            self.state = STATES[3][0]
        else:
            self.state = STATES[4][0]

    @api.multi 
    def action_complete(self):
        self.ensure_one()
        # cek lines
        if self.repair_ids:
            if self.repair_ids.filtered(lambda line:not line.lot_id_target or not line.lot_id_sumber):
                raise UserError(_("Ada data yang belum repair!"))
        else:
            raise UserError(_("Ada data yang belum repair!"))
        has_line_swap = []
        for swap_lot in self.repair_ids.filtered(lambda sl: sl.is_not_same == True and sl.is_swap == False):
            if swap_lot:
                if (swap_lot.lot_id_sumber.id not in has_line_swap) and (swap_lot.lot_id_target.id not in has_line_swap):
                    swap_lot.swap_barcode()
                    has_line_swap.append(swap_lot.lot_id_sumber.id)
                    has_line_swap.append(swap_lot.lot_id_target.id)

        for rec in self.repair_ids:
            if rec.is_not_same == True:
                if rec.is_swap == True:
                    sql = """
                        update stock_production_lot set store = true
                        where id = %s
                        """
                    self.env.cr.execute(sql, (rec.lot_id_target.id,))
                else:
                    pass
            else:
                sql = """
                    update stock_production_lot set store = true
                    where id = %s
                    """
                self.env.cr.execute(sql, (rec.lot_id_target.id,))

        fail_lines = self.repair_ids.search([('lot_id_target.store','=',False),('store_id','=',self.id)])
        if fail_lines:
            self.state = STATES[3][0]
        else:
            self.state = STATES[4][0]


    @api.onchange('barcode')
    def add_product_lot(self):
        if self.barcode:
            # if self.state in ["done"]:
            #     selections = self.fields_get()["state"]["selection"]
            #     value = next((v[1] for v in selections if v[0] == self.state), self.state)
            #     self.warning = "Tidak bisa scan item dalam status " + value
            #     self.barcode = False
            #     return

            if self:
                polybags = self.env['stock.production.lot'].search([('polybag', '=', self.barcode)])                
                lots = self.env['stock.production.lot'].search([('name', '=', self.barcode)])

                if not polybags and not lots:
                    self.warning = "Barcode " + self.barcode + " tidak ditemukan!"
                    self.barcode = False
                    return
           
                elif polybags and not lots:
                    if self.state != 'draft':
                        self.warning = "Polybag hanya bisa discan dalam status Draft!"
                        self.barcode = False
                        return
                    else :
                        polybag = self.env['stock.production.lot'].search([('polybag', '=', self.barcode)], limit=1)
                        if self.po_id:
                            if polybag.po_id != self.po_id:
                                self.warning = "Polybag tidak sesuai dengan No. OR yang dipilih!"
                                self.barcode = False
                                return
                        else:
                            self.po_id = polybag.po_id.id

                        search_stores_polybags = self.env['vit.summary_polybag_store'].search([('polybag_name', '=', self.barcode),('store_id', '!=', False)])
                        if search_stores_polybags:
                            for ssp in search_stores_polybags:
                                self.warning = "Polybag sudah terdaftar di " + ssp.store_id.name + ". Harap pindai barcode yang berbeda.!"
                                self.barcode = False
                                return
                        
                        search_polybag_store = self.summary_lines.filtered(lambda sl: sl.polybag_name == self.barcode)
                      
                        if search_polybag_store:
                            self.warning = "Polybag " + self.barcode + " sudah terdaftar. Harap pindai barcode yang berbeda.!"
                            self.barcode = False
                            return                          
                        else:
                            for pb in polybags:
                                # insert store line
                                store_lines_val = {
                                    'lot_id_sumber'  : pb.id,
                                    'karyawan_sumber': pb.karyawan,
                                    'nik_sumber'     : pb.nik,
                                    'size_id_sumber' : pb.size_id.id,
                                    'bordir_sumber'  : pb.nama_bordir,
                                    'style_id_sumber': pb.style_id.id,
                                    'pengukuran_karyawan_sumber' : pb.pengukuran_karyawan.id,
                                    'data_pengukuran_id_sumber' : pb.data_pengukuran_id.id,
                                    'polybag_sumber' : pb.polybag,
                                    'divisi_sumber'  : pb.divisi_id.id,
                                    'lokasi_sumber'  : pb.lokasi_id.id,
                                    'jabatan_sumber' : pb.jabatan_id.id,
                                    'location_id_sumber' : pb.location_id.id,
                                    'lot_sumber'     : pb.lot,
                                }
                                new_store_line = self.store_lines.new(store_lines_val)
                                self.store_lines += new_store_line

                            # insert summary
                            summary_val = {
                                'polybag_name'  : self.barcode,
                                'date'          : datetime.now(),
                                'qty_polybag'   : len(polybags.ids),
                            }
                            new_summary_line = self.summary_lines.new(summary_val)
                            self.summary_lines += new_summary_line

                elif lots and not polybags:
                    if self.po_id:
                        if lots.po_id != self.po_id:
                            self.warning = "Item tidak sesuai dengan No. OR yang dipilih!"
                            self.barcode = False
                            return
                    else:
                        self.po_id = lots.po_id.id
                        
                    if not self.state or self.state == 'draft':
                        self.insert_lot_sumber(lots[0])
                    else:
                        if not self.state or self.state == 'draft':
                            self.insert_lot_sumber(lots[0])
                        else :
                            search_stores_lots = self.env['vit.kasir_store_line'].search([('lot_id_target', '=', lots.id),('lot_id_target.store','=', True),('store_id','!=', False)])
                            search_barcode_store = self.store_lines.filtered(lambda sl: sl.lot_id_target == lots)
                            search_same_lot = self.store_lines.filtered(lambda sl: sl.lot_id_sumber == lots and sl.lot_id_target.id == False)
                            # search_same_style = self.store_lines.search([('lot_id_target', '!=', lots.id), ('lot_id_sumber', '=', False), ('style_id_target', '=', lots.style_id.id), ('size_id_target', '=', lots.size_id.id)], limit=1)
                            search_same_style = self.store_lines.filtered(lambda sl: sl.lot_id_sumber != lots and sl.lot_id_target.id == False and sl.style_id_sumber.id == lots.style_id.id and sl.size_id_sumber.id == lots.size_id.id)
                            # import pdb;pdb.set_trace()
                            if search_stores_lots:
                                for sslts in search_stores_lots:
                                    self.warning = "QRcode " + self.barcode + " sudah terdaftar di " + sslts.store_id.name + ". Harap pindai barcode yang berbeda"
                                    self.barcode = False
                                    return

                            elif search_barcode_store:
                                self.warning = "QRcode " + self.barcode + " sudah terdaftar. Harap pindai barcode yang berbeda!"
                                self.barcode = False
                                return

                            elif search_same_lot:
                                search_same_lot.update({
                                    'lot_id_target'  : lots.id,
                                    'karyawan_target': lots.karyawan,
                                    'nik_target'     : lots.nik,
                                    'size_id_target' : lots.size_id.id,
                                    'bordir_target'  : lots.nama_bordir,
                                    'style_id_target': lots.style_id.id,
                                    'pengukuran_karyawan_target' : lots.pengukuran_karyawan.id,
                                    'data_pengukuran_id_target' : lots.data_pengukuran_id.id,
                                    'polybag_target' : lots.polybag,
                                    'divisi_target'  : lots.divisi_id.id,
                                    'lokasi_target'  : lots.lokasi_id.id,
                                    'jabatan_target' : lots.jabatan_id.id,
                                    'location_id_target' : lots.location_id.id,
                                    'lot_target'     : lots.lot,
                                })

                            elif search_same_style:
                                search_same_style[0].update({
                                    'lot_id_target'  : lots.id,
                                    'karyawan_target': lots.karyawan,
                                    'nik_target'     : lots.nik,
                                    'size_id_target' : lots.size_id.id,
                                    'bordir_target'  : lots.nama_bordir,
                                    'style_id_target': lots.style_id.id,
                                    'pengukuran_karyawan_target' : lots.pengukuran_karyawan.id,
                                    'data_pengukuran_id_target' : lots.data_pengukuran_id.id,
                                    'polybag_target' : lots.polybag,
                                    'divisi_target'  : lots.divisi_id.id,
                                    'lokasi_target'  : lots.lokasi_id.id,
                                    'jabatan_target' : lots.jabatan_id.id,
                                    'location_id_target' : lots.location_id.id,
                                    'lot_target'     : lots.lot,
                                    'is_not_same' : True,
                                })

                            elif not search_same_style:
                                self.warning = "Style dan Size barang " + self.barcode + " tidak sesuai dengan Style dan Size pada daftar barang di polybag!"
                                self.barcode = False
                                return

            self.barcode = False
            self.warning = False

    def insert_lot_sumber(self,barcode) :
        search_barcode_store = self.store_lines.filtered(lambda sl: sl.lot_id_sumber == barcode)
        # import pdb;pdb.set_trace()
        if search_barcode_store:
            self.warning = "QRcode " + barcode.name + " sudah terdaftar di lot sumber. Harap pindai barcode yang berbeda."
            self.barcode = False
            return

        lot_line={'lot_id_sumber'  : barcode.id,
                'karyawan_sumber': barcode.karyawan,
                'nik_sumber'     : barcode.nik,
                'size_id_sumber' : barcode.size_id.id,
                'bordir_sumber'  : barcode.nama_bordir,
                'style_id_sumber': barcode.style_id.id,
                'pengukuran_karyawan_sumber' : barcode.pengukuran_karyawan.id,
                'data_pengukuran_id_sumber' : barcode.data_pengukuran_id.id,
                'polybag_sumber' : barcode.polybag,
                'divisi_sumber'  : barcode.divisi_id.id,
                'lokasi_sumber'  : barcode.lokasi_id.id,
                'jabatan_sumber' : barcode.jabatan_id.id,
                'location_id_sumber' : barcode.location_id.id,
                'lot_sumber'     : pb.lot,
            }
        new_store_line = self.store_lines.new(lot_line)
        self.store_lines += new_store_line

        # insert polybag
        if not self.summary_lines :
            summary_polybag = {
                        'polybag_name'  : barcode.polybag,
                        'date'          : datetime.now(),
                        'qty_polybag'   : 1,
                    }
            new_summary_line = self.summary_lines.new(summary_polybag)
            self.summary_lines += new_summary_line
        else :
            sum_line = self.summary_lines.filtered(lambda x:x.polybag_name == barcode.polybag)
            if sum_line :
                sum_line.update({'qty_polybag':sum_line.qty_polybag+1})
            else : 
                summary_polybag = {
                        'polybag_name'  : barcode.polybag,
                        'date'          : datetime.now(),
                        'qty_polybag'   : 1,
                    }
                new_summary_line = self.summary_lines.new(summary_polybag)
                self.summary_lines += new_summary_line
   

    @api.onchange('barcode_repair')
    def add_product_repair(self):
        if self.barcode_repair:
            if self.state == 'partial':
                polybags = self.env['stock.production.lot'].search([('polybag', '=', self.barcode_repair)])                
                lots = self.env['stock.production.lot'].search([('name', '=', self.barcode_repair)])

                if not polybags and not lots:
                    self.warning_repair = "Barcode " + self.barcode_repair + " tidak ditemukan!"
                    self.barcode_repair = False
                    return
           
                elif polybags and not lots:
                    search_polybag_rp = self.repair_ids.filtered(lambda rp: rp.polybag_sumber == self.barcode_repair)                  
                    if search_polybag_rp:
                        self.warning_repair = "Polybag " + self.barcode_repair + " sudah terdaftar. Harap pindai barcode yang berbeda.!"
                        self.barcode_repair = False
                        return                          
                    else:
                        # store_ids = self.unvalidate_ids
                        # for st in store_ids:
                        lot_ids = self.env['stock.production.lot'].search([('polybag', '=', self.barcode_repair),('store','=',False)])
                        # insert repair line
                        for pb in lot_ids:
                            repair_lines_val = {
                                'lot_id_sumber'  : pb.id,
                                'karyawan_sumber': pb.karyawan,
                                'nik_sumber'     : pb.nik,
                                'size_id_sumber' : pb.size_id.id,
                                'bordir_sumber'  : pb.nama_bordir,
                                'style_id_sumber': pb.style_id.id,
                                'pengukuran_karyawan_sumber' : pb.pengukuran_karyawan.id,
                                'data_pengukuran_id_sumber' : pb.data_pengukuran_id.id,
                                'polybag_sumber' : pb.polybag,
                                'divisi_sumber'  : pb.divisi_id.id,
                                'lokasi_sumber'  : pb.lokasi_id.id,
                                'jabatan_sumber' : pb.jabatan_id.id,
                                'location_id_sumber' : pb.location_id.id,
                                'lot_sumber'     : pb.lot,
                            }
                            new_repair_line = self.repair_ids.new(repair_lines_val)
                            self.repair_ids += new_repair_line

                elif lots and not polybags:
                    search_stores_lots = self.env['vit.kasir_store_line'].search([('lot_id_target', '=', lots.id),('store_id','!=', self.id)])
                    search_repair_lots = self.env['vit.kasir_repair_line'].search([('lot_id_target', '=', lots.id),('store_id','!=', self.id)])
                    search_barcode_store = self.repair_ids.filtered(lambda sl: sl.lot_id_target == lots)
                    search_same_lot = self.repair_ids.filtered(lambda sl: sl.lot_id_sumber == lots and sl.lot_id_target.id == False)
                    search_same_style = self.repair_ids.filtered(lambda sl: sl.lot_id_sumber != lots and sl.lot_id_target.id == False and sl.style_id_sumber.id == lots.style_id.id and sl.size_id_sumber.id == lots.size_id.id)
                    if search_stores_lots:
                        for sslts in search_stores_lots:
                            self.warning_repair = "QRcode " + self.barcode_repair + " sudah terdaftar di " + sslts.store_id.name + ". Harap pindai barcode yang berbeda"
                            self.barcode_repair = False
                            return
                    if search_repair_lots:
                        for sslts in search_stores_lots:
                            self.warning_repair = "QRcode " + self.barcode_repair + " sudah terdaftar di " + sslts.store_id.name + ". Harap pindai barcode yang berbeda"
                            self.barcode_repair = False
                            return

                    elif search_barcode_store:
                        self.warning_repair = "QRcode " + self.barcode_repair + " sudah terdaftar. Harap pindai barcode yang berbeda!"
                        self.barcode_repair = False
                        return

                    elif search_same_lot:
                        search_same_lot.update({
                            'lot_id_target'  : lots.id,
                            'karyawan_target': lots.karyawan,
                            'nik_target'     : lots.nik,
                            'size_id_target' : lots.size_id.id,
                            'bordir_target'  : lots.nama_bordir,
                            'style_id_target': lots.style_id.id,
                            'pengukuran_karyawan_target' : lots.pengukuran_karyawan.id,
                            'data_pengukuran_id_target' : lots.data_pengukuran_id.id,
                            'polybag_target' : lots.polybag,
                            'divisi_target'  : lots.divisi_id.id,
                            'lokasi_target'  : lots.lokasi_id.id,
                            'jabatan_target' : lots.jabatan_id.id,
                            'location_id_target' : lots.location_id.id,
                            'lot_target'     : lots.lot,
                        })

                    elif search_same_style:
                        search_same_style[0].update({
                            'lot_id_target'  : lots.id,
                            'karyawan_target': lots.karyawan,
                            'nik_target'     : lots.nik,
                            'size_id_target' : lots.size_id.id,
                            'bordir_target'  : lots.nama_bordir,
                            'style_id_target': lots.style_id.id,
                            'pengukuran_karyawan_target' : lots.pengukuran_karyawan.id,
                            'data_pengukuran_id_target' : lots.data_pengukuran_id.id,
                            'polybag_target' : lots.polybag,
                            'divisi_target'  : lots.divisi_id.id,
                            'lokasi_target'  : lots.lokasi_id.id,
                            'jabatan_target' : lots.jabatan_id.id,
                            'location_id_target' : lots.location_id.id,
                            'lot_target'     : lots.lot,
                            'is_not_same' : True,
                        })

                    elif not search_same_style:
                        self.warning_repair = "Style dan Size barang " + self.barcode_repair + " tidak sesuai dengan Style dan Size pada daftar barang di polybag!"
                        self.barcode_repair = False
                        return

            self.barcode_repair = False
            self.warning_repair = False

    @api.multi
    def unlink(self):
        for ks in self:
            if ks.state != 'draft':
                raise UserError(_('Data yang bisa dihapus hanya yg berstatus draft'))
        return super(KasirStore, self).unlink()


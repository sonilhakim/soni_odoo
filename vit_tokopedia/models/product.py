from odoo import api, fields, models, _
import time
import datetime
import logging
from io import BytesIO
import xlsxwriter
import base64
from odoo.exceptions import Warning
_logger = logging.getLogger(__name__)

class product(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    berat           = fields.Float(string='Berat')
    pesan           = fields.Float(string='Pemesanan Minimum')
    status          = fields.Selection([('aktif', 'Aktif'), ('nonaktif', 'Nonaktif')], string='Status', default='aktif',)
    # jumlah      = fields.Char(string='Jumlah Stok')
    tokped_categ_id = fields.Many2one('product.category', 'Tokopedia Category', domain="[('is_tokopedia','=',True)]", help="Select tokopedia category for the current product")
    desk            = fields.Text(string="Deskripsi Produk")
    etalase         = fields.Char(string='Etalase')
    preorder        = fields.Selection([('ya', 'Ya'), ('tidak', 'Tidak')], string='Preorder',)
    waktu_preorder  = fields.Float(string='Waktu Proses Preorder')
    kondisi         = fields.Selection([('baru', 'Baru'), ('bekas', 'Bekas')], string='Kondisi', default='baru',)
    gambar_1        = fields.Char("Gambar 1", help="This field holds the image used as image for tokopedia, limited to 1024x1024px.")
    gambar_2        = fields.Char("Gambar 2", help="This field holds the image used as image for tokopedia, limited to 1024x1024px.")
    gambar_3        = fields.Char("Gambar 3", help="This field holds the image used as image for tokopedia, limited to 1024x1024px.")
    gambar_4        = fields.Char("Gambar 4", help="This field holds the image used as image for tokopedia, limited to 1024x1024px.")
    gambar_5        = fields.Char("Gambar 5", help="This field holds the image used as image for tokopedia, limited to 1024x1024px.")
    url_1           = fields.Char(string='URL Video Produk 1')
    url_2           = fields.Char(string='URL Video Produk 2')
    url_3           = fields.Char(string='URL Video Produk 3')
    is_exported     = fields.Boolean(string="Is Exported",  )
    date_exported   = fields.Datetime(string="Exported Date", required=False, )
    tokopedia_ok     = fields.Boolean('Can be in Tokopedia')


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = "product.category"

    code            = fields.Char(string="Code")
    is_tokopedia    = fields.Boolean(string="Is Tokopedia",  )
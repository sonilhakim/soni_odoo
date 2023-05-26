from odoo import api, models


class JadwalPersiapanMaterial(models.AbstractModel):
    _name = 'report.vit_report_rekap_inventory.jpm_tmpl'

    @api.model
    def _compute_jpm_tmpl(self, data):
        sql = """SELECT rp.name, pt.name, mr.product_qty, mr.date_planned_start, sp.scheduled_date, sp.date_done
                FROM stock_picking sp
                LEFT JOIN mrp_production mr ON sp.origin = mr.name
                LEFT JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                LEFT JOIN res_partner rp ON mr.partner_id = rp.id
                LEFT JOIN product_product pp ON mr.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                WHERE spt.name = %s
                """

        if data['date_from'] and data['date_to']:
            sql += " AND sp.scheduled_date >= '%s' AND sp.scheduled_date <= '%s' ORDER BY sp.scheduled_date" %(data['date_from'], data['date_to'])
        else:
            sql += "ORDER BY sp.scheduled_date"

        self.env.cr.execute(sql, ('Consume',))
        result = self.env.cr.fetchall()
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'stock.picking'
        wiz_rec = self.env[self._context.get('active_model', False)].browse(self._context.get('active_ids', False))
        result = self._compute_jpm_tmpl(data)
        docargs = {
            'doc_ids': wiz_rec.ids,
            'doc_model': 'jadwal.persiapan.material.wizard',
            'data': data,
            'docs': wiz_rec,
            'data_dict': result,
        }
        return docargs

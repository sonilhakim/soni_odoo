from odoo import api, models


class ReportRekapBTB(models.AbstractModel):
    _name = 'report.vit_report_rekap_inventory.rekap_btb_report_tmpl'

    @api.model
    def _compute_rekap_btb(self, data):
        sql = """SELECT sp.date_done, po.name, rp.name, rpq.name, pt.name, sm.quantity_done
                FROM stock_move sm
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                LEFT JOIN purchase_order po ON sp.origin = po.name
                LEFT JOIN res_partner rp ON sp.partner_id = rp.id
                LEFT JOIN product_product pp ON sm.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                LEFT JOIN vit_marketing_inquery_garmen iq ON sm.analytic_tag_id = iq.analytic_tag_id
                LEFT JOIN res_partner rpq ON iq.partner_id = rpq.id
                WHERE spt.name = %s AND sp.state = %s
                """

        if data['date_from'] and data['date_to']:
            sql += " AND sp.date_done >= '%s' AND sp.date_done <= '%s' ORDER BY sp.date_done " %(data['date_from'], data['date_to'])
        else:
            sql += "ORDER BY sp.date_done"
        
        self.env.cr.execute(sql, ('Receipts', 'done',))
        result = self.env.cr.fetchall()
        return result

    @api.model
    def _get_report_values(self, docids, data=None):
        self.model = 'stock.move'
        wiz_rec = self.env[self._context.get('active_model', False)].browse(self._context.get('active_ids', False))
        result = self._compute_rekap_btb(data)
        docargs = {
            'doc_ids': wiz_rec.ids,
            'doc_model': 'rekap.btb.wizard',
            'data': data,
            'docs': wiz_rec,
            'data_dict': result,
        }
        return docargs

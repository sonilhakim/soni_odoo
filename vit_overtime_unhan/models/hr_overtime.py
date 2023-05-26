from odoo import api, fields, models, _
import time
from datetime import datetime, timedelta
import dateutil.parser
from odoo.exceptions import UserError, ValidationError

SESSION_STATES =[('draft','Draft'),('confirm','Menunggu Persetujuan Manager'),('confirm_manager','Menunggu Persetujuan HRD'),("refuse","Ditolak"),("validate", "Valid"),("cancel", "Dibatalkan")]

class hr_overtime(models.Model):
    _name = "hr.overtime"
    _description = "Overtime"
    _order = "date_from asc"


    def _compute_number_of_hours(self, name, args):
        result = {}
        for hol in self:
            result[hol.id] = hol.number_of_hours_temp         
        return result


    name                = fields.Char("Deskripsi", required=True, readonly=True, states={"draft":[("readonly",False)]}, size=64)
    state               = fields.Selection(string="State", 
                                            selection=SESSION_STATES,
                                            required=True,
                                            readonly=True,
                                            default=SESSION_STATES[0][0])

    user_id             = fields.Many2one("res.users", "Pembuat", default=lambda self: self.env.user,readonly=True)
    date_from           = fields.Datetime("Tanggal Mulai", readonly=True, states={"draft":[("readonly",False)]})
    date_to             = fields.Datetime("Tanggal Akhir", readonly=True, states={"draft":[("readonly",False)]})
    manager_id          = fields.Many2one("hr.employee", "Manager Department", readonly=True)
    notes               = fields.Text("Notes", readonly=True, states={"draft":[("readonly",False)]})
    number_of_hours_temp= fields.Float("Jam Lembur", readonly=True, states={"draft":[("readonly",False)]})
    hari_libur          = fields.Boolean("Hari Libur?", readonly=True, states={"draft":[("readonly",False)]})
    number_of_days_temp = fields.Float("Hari Lembur", readonly=True, states={"draft":[("readonly",False)]})
    number_of_hours     = fields.Float(compute="_compute_number_of_hours", method=True, string="Jumlah Jam", store=True)
    department_id       = fields.Many2one("hr.department", "Departemen", readonly=True, states={"draft":[("readonly",False)]})
    type_id             = fields.Many2one("hr.overtime.hour", "Tipe Lembur", required=True, readonly=True, states={"draft":[("readonly",False)]})
    date                = fields.Date("Tanggal", default=lambda self: self._context.get("date", fields.Date.context_today(self)))
    break_hour          = fields.Float("Jam Istirahat", readonly=True, states={"draft":[("readonly",False)]})
    month               = fields.Char("Bulan", default=lambda *a: time.strftime("%Y-%m"))
    nominal             = fields.Integer("Nominal")
    employee_ids        = fields.One2many("hr.overtime.employee", "overtime_id", "Karyawan", readonly=True, states={"draft":[("readonly",False)]})
    manager_department_id  = fields.Integer(related="department_id.manager_id.user_id.id")
    tgl_lembur          = fields.Date(string="Tanggal lembur")
    lembur_istimewa     = fields.Boolean("Lembur Istimewa?",readonly=True, states={"draft":[("readonly",False)]})
    lembur_biasa        = fields.Boolean("Lembur biasa?", states={"draft":[("readonly",False)]})


    _sql_constraints = [
        ("date_check", "CHECK ( number_of_hours_temp > 0 )", "The number of hours must be greater than 0 !"),
        ("date_check2", "CHECK (date_from < date_to)", "The start date must be before the end date !")
    ]

    # @api.multi
    # @api.onchange('hari_libur')
    # @api.depends('hari_libur','lembur_istimewa')
    # def _total_years(self):
    #     # import pdb;pdb.set_trace()
    #     if self.hari_libur == True:
    #         self.lembur_istimewa = False

    @api.multi
    @api.onchange('type_id')
    @api.depends('hari_libur','lembur_istimewa','type_id','lembur_biasa')
    def _total_years(self):
        # import pdb;pdb.set_trace()
        if self.type_id.name == 'Lembur Biasa':
            self.lembur_biasa = True
            self.lembur_istimewa = False
            self.hari_libur = False
        elif self.type_id.name == 'Lembur Off In':
            self.hari_libur = True
            self.lembur_istimewa = False
            self.lembur_biasa = False
        elif self.type_id.name == 'Lembur Istimewa':
            self.lembur_istimewa = True
            self.lembur_biasa = False
            self.hari_libur = False

    @api.model
    def create(self, vals):
        if 'hari_libur' in vals and 'lembur_istimewa' in vals:
            if vals['hari_libur'] == True and vals['lembur_istimewa'] == True:
                raise UserError(_('Jenis Document tidak benar! pilih salah satu lembur Istimewa, lembur day off atau lembur biasa !'))
        return super(hr_overtime, self).create(vals)

    @api.multi
    def write(self, vals):
        #import pdb;pdb.set_trace()
        if 'hari_libur' in vals and 'lembur_istimewa' in vals:
            if vals['hari_libur'] == True and vals['lembur_istimewa'] == True:
                raise UserError(_('Jenis Document tidak benar! pilih salah satu lembur Istimewa, lembur day off atau lembur biasa !'))
        elif 'hari_libur' in vals and 'lembur_istimewa' not in vals:
            if vals['hari_libur'] == True and self.lembur_istimewa == True:
                raise UserError(_('Jenis Document tidak benar! pilih salah satu lembur Istimewa, lembur day off atau lembur biasa !'))
        elif 'hari_libur' not in vals and 'lembur_istimewa' in vals:
            if self.hari_libur == True and vals['lembur_istimewa'] == True:
                raise UserError(_('Jenis Document tidak benar! pilih salah satu lembur Istimewa, lembur day off atau lembur biasa !'))
        return super(hr_overtime, self).write(vals)



    # TODO: can be improved using resource calendar method
    def _get_number_of_hours(self, date_from, date_to, istirahat):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
        timedelta = to_dt - from_dt
        diff_day =(float(timedelta.seconds) / 3600) - istirahat
        return diff_day

    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""

        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
        timedelta = to_dt - from_dt
        diff_days = timedelta.days + float(timedelta.seconds) / 86400
        return diff_days

    # def unlink(self):
    #     for rec in self:
    #         if rec.state <> "draft":
    #             raise UserError(_("Warning!"),_("You cannot delete a overtime which is not in draft state !"))
    #     return super(hr_overtime, self).unlink(ids, context)

    @api.onchange('date_to','break_hour')
    def _get_number_of_hours(self):
        """Returns an overtime hours."""
        if self.date_to:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            from_dt = datetime.strptime(str(self.date_from), DATETIME_FORMAT)
            to_dt = datetime.strptime(str(self.date_to), DATETIME_FORMAT)
            timedelta = to_dt - from_dt
            diff_day =(float(timedelta.seconds) / 3600) - self.break_hour
            self.number_of_hours_temp = diff_day     


    @api.onchange('date_from')
    def _calc_date(self):
        # import pdb;pdb.set_trace()
        if self.date_from:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            date_field1 = datetime.strptime(str(self.date_from), DATETIME_FORMAT)
            date_new = date_field1 + timedelta(hours=-7)
            self.tgl_lembur = str(date_new)
        return {}

    # @api.depends('date_from')
    # def _calc_date(self):
    #     for date in self:
    #         DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    #         date_field1 = datetime.strptime(date.date_from, DATETIME_FORMAT)

    #         date.tgl_lembur = date_field1 + timedelta(hours=7)
    #     return {}


    #action for state / workflow
    @api.multi
    def action_draft(self):
        self.state = SESSION_STATES[0][0]
    @api.multi
    def action_confirm_admin(self):
        self.state = SESSION_STATES[1][0]
    @api.multi
    def action_confirm_manager(self):
        self.state = SESSION_STATES[2][0]    
    @api.multi
    def action_refuse(self):
        self.state = SESSION_STATES[3][0]   
    @api.multi
    def action_cancel(self):
        self.state = SESSION_STATES[5][0]    
    @api.multi
    def action_validate(self):
        self.state = SESSION_STATES[4][0]

hr_overtime()



class hr_overtime_employee(models.Model) :

    _name = "hr.overtime.employee"
    _description = " Detail Employee"


    @api.depends('employee_id','ovt_hour')
    def _hitung_lembur(self):
        for obj in self:
            jam = float(obj.ovt_hour)
            overtime_type = obj.overtime_id.type_id.hour_ids
            x = 0
            tot = 0
            # sisa = jam
            for over in overtime_type :
                if jam > 0:
                    sampai = float(over.to_hour)
                    dari = float(over.from_hour)
                    if sampai == 0.0 :
                        sampai = float(1000)
                    if dari != 0.0 :
                        if dari == 1 :
                            i = sampai
                        if dari > 1  :  
                            i = sampai - dari
                            if i == 0 :
                                i = 1

                        if jam >= i :
                            tot = i * over.calculation
                        elif jam < i :
                            tot = jam * over.calculation
                        jam = jam - i 
                        x = x + tot

            obj.total_jam = round(x,2)
            obj.write({"total_jam1":round(x,2)})



    overtime_id = fields.Many2one("hr.overtime", "overtime_id", ondelete="cascade")
    employee_id = fields.Many2one("hr.employee", "Karyawan", domain="[('department_id','=',parent.department_id)]")
    ovt_hour    = fields.Float("Jam Lembur riil")
    total_jam   = fields.Float(compute="_hitung_lembur",store=False, readonly=True,string="Total Jam Lembur (Calculated)")
    total_jam1  = fields.Float("Total Jam Lembur (Store DB)")


class overtime_hour(models.Model):
    _name = "hr.overtime.hour"
    _description = "Pengali jam lembur"


    name = fields.Char("Nama", required=True)
    hour_ids = fields.One2many("hr.overtime.hour.detail","hour_type", "Jam")  

overtime_hour()


class overtime_hour_detail(models.Model):
    _name = "hr.overtime.hour.detail"


    from_hour = fields.Selection([("1","Jam 1"),("2","Jam 2"),("3","Jam 3"),("4","Jam 4"),("5","Jam 5"),("6","Jam 6"),("7","Jam 7"),
            ("8","Jam 8"),("9","Jam 9"),("10","Jam 10"),("11","Jam 11"),("12","Jam 12"),("13","Jam 13"),("14","Jam 14"),("15","Jam 15"),
            ("16","Jam 16"),("17","Jam 17"),("18","Jam 18"),("19","Jam 19"),("20","Jam 20"),("21","Jam 21"),("22","Jam 22"),("23","Jam 23"),("24","Jam 24")], string="Hour Start", required=True)
    to_hour = fields.Selection([("1","Jam 1"),("2","Jam 2"),("3","Jam 3"),("4","Jam 4"),("5","Jam 5"),("6","Jam 6"),("7","Jam 7"),
            ("8","Jam 8"),("9","Jam 9"),("10","Jam 10"),("11","Jam 11"),("12","Jam 12"),("13","Jam 13"),("14","Jam 14"),("15","Jam 15"),
            ("16","Jam 16"),("17","Jam 17"),("18","Jam 18"),("19","Jam 19"),("20","Jam 20"),("21","Jam 21"),("22","Jam 22"),("23","Jam 23"),("24","Jam 24")], string="Hour End", required=True)
    calculation = fields.Float("Perhitungan" , required=True)
    hour_type = fields.Many2one("hr.overtime.hour","Tipe Lembur")

overtime_hour_detail()

# class Hr_employee(models.Model):
#     _name = 'hr.employee'
#     _inherit = 'hr.employee'


#     @api.multi
#     @api.depends('name', 'nik')
#     def name_get(self):
#         #import pdb;pdb.set_trace()
#         result = []
#         for account in self:
#             name = '['+ (account.nik or '') + '] ' + (account.name or '')
#             result.append((account.id, name))
#         return result
        
#     @api.model
#     def name_search(self, name, args=None, operator='ilike', limit=100):
#         args = args or []
#         recs = self.browse()
#         if not recs:
#             recs = self.search(['|', ('name', operator, name),('nik', operator, name)] + args, limit=limit)
#         return recs.name_get() 

# Hr_employee()
# -*- coding: utf-8 -*-
import odoo
import math
from odoo.tools.translate import _
import odoo.addons.web.controllers.main as main
import logging
import werkzeug
import json
from odoo import http, _
from urllib.parse import urlsplit
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)

# class Home(main.Home):

# 	# Public Home
# 	@http.route('/', type='http', auth="public", website=True)
# 	def home(self, **kw):
# 		res = super(Home, self).index()
# 		e_categories = request.env['e_learning.category'].sudo().search([('id', '!=', None)])
# 		e_learning_ids = request.env['e_learning.e_learning']

# 		return request.render("vit_elearning.elearning", {
# 			'e_categories'		: e_categories,
# 			'e_class_ids'			: e_learning_ids.sudo().search([('id', '!=', None), ('online_class', '=', True),('state', '=', 'publish')]),
# 			'e_seminar_ids'			: e_learning_ids.sudo().search([('id', '!=', None), ('online_seminar', '=', True),('state', '=', 'publish')]),
# 		})

class VitElearning(http.Controller):

	# Public Home
	@http.route("/elearning", auth='public')
	def elearning(self, **kw):
		e_categories 	= request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		e_learning_ids 	= request.env['e_learning.e_learning']
		artikel_ids 	= request.env['artikel.e_learning']
		# user_id 		= request.env.uid
		# user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		# if not user.groups_id:
		# 	return request.render("vit_elearning.admission", {})
		# else :
		return request.render("vit_elearning.elearning", {
			'e_categories'		: e_categories,
			'e_class_ids'		: e_learning_ids.sudo().search([('id', '!=', None), ('online_class', '=', True),('show_in_front','=',True), ('state', '=', 'publish')],limit=6),
			'e_seminar_ids'		: e_learning_ids.sudo().search([('id', '!=', None), ('online_seminar', '=', True),('state', '=', 'publish')],limit=3),
			'artikel_ids'		: artikel_ids.sudo().search([('id', '!=', None), ('state', '=', 'publish')]),
		})

	@http.route("/myaccount", auth='public')
	def myaccount(self, **kw):
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			return request.render("vit_elearning.myaccount", {
				'user_id' : user,
			})	

	@http.route("/kelasonline", auth='public')
	def kelasonline(self, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonline", {
			'pages'				: pages,
			'e_categories'		: e_categories,
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/kelasonlines/<int:e_category>", auth='public')
	def kelasonlines(self, e_category, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category']
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_category), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_category), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonlines", {
			'pages'				: pages,
			'e_categories'		: e_categories.sudo().search([('id', '!=', None)]),
			'e_category_id'		: e_categories.sudo().search([('id', '=', e_category)]),
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/kelasonline_free", auth='public')
	def kelasonline_free(self, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('total_price', '=', 0), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('total_price', '=', 0), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonline_free", {
			'pages'				: pages,
			'e_categories'		: e_categories,
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/kelasonlines_free/<int:e_category>", auth='public')
	def kelasonlines_free(self, e_category, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category']
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('total_price', '=', 0), ('e_learning_category_id', '=', e_category), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('total_price', '=', 0), ('e_learning_category_id', '=', e_category), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonlines_free", {
			'pages'				: pages,
			'e_categories'		: e_categories.sudo().search([('id', '!=', None)]),
			'e_category_id'		: e_categories.sudo().search([('id', '=', e_category)]),
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/kelasonline_mentor/<int:partner_id>", auth='public')
	def kelasonline_mentor(self, partner_id, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category']
		partner_ids 	= request.env['res.partner']
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('teachers_id', '=', partner_id), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('teachers_id', '=', partner_id), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonline_mentor", {
			'pages'				: pages,
			'e_categories'		: e_categories.sudo().search([('id', '!=', None)]),
			'partner_id'		: partner_ids.sudo().search([('id', '=', partner_id)]),
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/kelasonlines_mentor/<int:partner_id><int:e_category>", auth='public')
	def kelasonlines_mentor(self, partner_id, e_category, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_categories 	= request.env['e_learning.category']
		partner_ids 	= request.env['res.partner']
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_category), ('teachers_id', '=', partner_id), ('online_class', '=', True), ('state', '=', 'publish')],offset=offset, limit=9)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_category), ('teachers_id', '=', partner_id), ('online_class', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.kelasonlines_mentor", {
			'pages'				: pages,
			'e_categories'		: e_categories.sudo().search([('id', '!=', None)]),
			'e_category_id'		: e_categories.sudo().search([('id', '=', e_category)]),
			'partner_id'		: partner_ids.sudo().search([('id', '=', partner_id)]),
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})

	@http.route("/artikel", auth='public')
	def artikel(self, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		artikel_ids 	= request.env['artikel.e_learning'].sudo().search([('id', '!=', None), ('state', '=', 'publish')],offset=offset, limit=3)
		pages 			= request.env['artikel.e_learning'].sudo().search([('id', '!=', None), ('state', '=', 'publish')],)
		pages			= len(pages)/3
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.artikel", {
			'pages'				: pages,
			'artikel_ids'		: artikel_ids,
			'url' 				: current_url,
		})

	@http.route("/about", auth='public')
	def about(self, **kw):
		e_categories 	= request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		
		return request.render("vit_elearning.about", {
			'e_categories'		: e_categories,
		})

	@http.route("/seminaronline", auth='public')
	def seminaronline(self, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		e_learning_ids 	= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('online_seminar', '=', True),('state', '=', 'publish')],offset=offset, limit=3)
		pages 			= request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('online_seminar', '=', True), ('state', '=', 'publish')],)
		pages			= len(pages)/3
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.seminaronline", {
			'pages'				: pages,
			'e_learning_ids'	: e_learning_ids,
			'url' 				: current_url,
		})	

	@http.route("/single-courses/<int:e_learning_id>", auth='public')
	def single_courses(self, e_learning_id, **kw):
		e_learning_ids 	= request.env['e_learning.e_learning']
		video 			= e_learning_ids.sudo().search([('id', '=', e_learning_id)]).video_url
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
		# Update viewers
			# url_youtube = []
			if e_learning_id:
				# viewer = e_learning_ids.sudo().search([('id', '=', e_learning_id)]).viewer
				# viewer = e_learning_ids.sudo().search([('id', '=', e_learning_id)]).update({'viewer' : viewer + 1,})
				# if video != False:
				# 	url_youtube = video.split('/')[-1]

				return request.render("vit_elearning.single-courses", {
					'e_learning_id'	: e_learning_ids.sudo().search([('id', '=', e_learning_id)]),
					# 'url_youtube'	: "https://www.youtube.com/embed/{}?autoplay=1&mute=1".format(url_youtube),
					'url_video'		: video,
					'e_learning_ids': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_class', '=', True),('show_in_front','=',True),('state', '=', 'publish')],limit=6),
				})
			else:
				return request.render("vit_elearning.not_found", {})

	@http.route("/artikel-detail/<int:artikel_id>", auth='public')
	def artikel_detail(self, artikel_id, **kw):
		artikel_ids 	= request.env['artikel.e_learning']
		e_learning_ids 	= request.env['e_learning.e_learning']
		
		if artikel_id:
			return request.render("vit_elearning.artikel-detail", {
				'artikel_id'	: artikel_ids.sudo().search([('id', '=', artikel_id)]),
				'artikel_ids'	: artikel_ids.sudo().search([('id', '!=', None),('id', '!=', artikel_id), ('state', '=', 'publish')]),
				'e_learning_ids': e_learning_ids.sudo().search([('id', '!=', None),('online_class', '=', True),('state', '=', 'publish')], limit=9),
			})
		else:
			return request.render("vit_elearning.not_found", {})

	@http.route("/single-seminar/<int:e_learning_id>", auth='public', website=True)
	def single_seminar(self, e_learning_id, **kw):
		e_learning_ids = request.env['e_learning.e_learning']
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			if e_learning_id:
				return request.render("vit_elearning.single-seminar", {
					'e_learning_id'	: e_learning_ids.sudo().search([('id', '=', e_learning_id)]),
					'e_learning_ids': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_seminar', '=', True),('state', '=', 'publish')]),
				})
			else:
				return request.render("vit_elearning.not_found", {})

	@http.route("/our-mentor", auth='public')
	def mentor(self, **kw):
		offset			= kw.get('offset',0)
		offset			= int(offset)
		partner_ids 	= request.env['res.partner'].sudo().search([('is_mentor', '=', True)],offset=offset, limit=9)
		pages 			= request.env['res.partner'].sudo().search([('is_mentor', '=', True)])
		pages			= len(pages)/9
		pages			= math.ceil(pages)
		url 			= http.request.httprequest.full_path
		parse 			= str(url)
		c_url 			= parse.split('=')[-1]
		curl 			= urlsplit(c_url)
		current_url 	= int(curl[2])
		
		return request.render("vit_elearning.mentor", {
			'pages'				: pages,
			'partner_ids'		: partner_ids,
			'url' 				: current_url,
		})

	@http.route("/comment/<int:e_learning_id>", type='http', auth='public', website=True)
	def comment(self, e_learning_id, **kw):
		elearning_id 	= request.env['e_learning.e_learning'].sudo().search([('id', '=', e_learning_id)])		
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			for el in elearning_id:	
				kw.update({
					'res_id' 	: el.id,
					'model'		: el._name,
					'author_id'	: user.partner_id.id,
					})
				el.message_ids.sudo().create(kw)
			
			
	@http.route("/rating/<int:e_learning_id>", type='http', auth='public', website=True)
	def rating(self, e_learning_id, **kw):
		# import pdb; pdb.set_trace()
		elearning_id 	= request.env['e_learning.e_learning'].sudo().search([('id', '=', e_learning_id)])
		e_learning_ids 	= request.env['e_learning.e_learning']
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])
		kw.update({
				'rating' : elearning_id.rating + float(kw["rating"]),
				})

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			elearning_id.sudo().write(kw)
	
	@http.route("/viewer/<int:e_learning_id>", type='http', auth='public', website=True)
	def viewer(self, e_learning_id, **kw):
		# import pdb; pdb.set_trace()
		elearning_id 	= request.env['e_learning.e_learning'].sudo().search([('id', '=', e_learning_id)])
		e_learning_ids 	= request.env['e_learning.e_learning']
		if e_learning_id:
				viewer = e_learning_ids.sudo().search([('id', '=', e_learning_id)]).viewer
				viewer = e_learning_ids.sudo().search([('id', '=', e_learning_id)]).update({'viewer' : viewer + 1,})

	@http.route("/single-courses-lock/<int:e_learning_id>", auth='public')
	def single_courses_lock(self, e_learning_id, **kw):
		e_learning_ids = request.env['e_learning.e_learning']
		e_learning     = request.env['e_learning.e_learning'].sudo().search([('id', '=', e_learning_id)])
		e_learning_crs = request.env['e_learning.e_learning']
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			if e_learning_id:
				return request.render("vit_elearning.single-courses-lock", {
					'e_learning' : e_learning,
					'e_learning_cl': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_class', '=', True), ('state', '=', 'publish')],limit=3),
					'e_learning_crs': e_learning_ids.sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_learning.e_learning_category_id.id),('id', '!=', e_learning_id), ('online_class', '=', True),('state', '=', 'publish')],limit=3),
					'e_learning_sem': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_seminar', '=', True),('state', '=', 'publish')],limit=3),
				})
			else:
				return request.render("vit_elearning.not_found", {
				})

	@http.route("/single-seminar-lock/<int:e_learning_id>", auth='public')
	def single_seminar_lock(self, e_learning_id, **kw):
		e_learning_ids = request.env['e_learning.e_learning']
		e_learning     = request.env['e_learning.e_learning'].sudo().search([('id', '=', e_learning_id)])
		e_learning_crs = request.env['e_learning.e_learning']
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])

		if not user.groups_id:
			return request.render("vit_elearning.admission", {})
		else :
			if e_learning_id:
				return request.render("vit_elearning.single-seminar-lock", {
					'e_learning' : e_learning,
					'e_learning_sem': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_seminar', '=', True), ('state', '=', 'publish')],limit=3),
					'e_learning_crs': e_learning_ids.sudo().search([('id', '!=', None), ('e_learning_category_id', '=', e_learning.e_learning_category_id.id),('id', '!=', e_learning_id), ('online_seminar', '=', True),('state', '=', 'publish')],limit=3),
					'e_learning_cl': e_learning_ids.sudo().search([('id', '!=', None),('id', '!=', e_learning_id), ('online_class', '=', True),('state', '=', 'publish')],limit=3),
				})
			else:
				return request.render("vit_elearning.not_found", {
				})

	@http.route('/web/dbredirect', type='http', auth="none")
	def el_redirect(self, redirect='/elearning', **kw):
		ensure_db()
		return werkzeug.utils.redirect(redirect, 303)

	def _login_redirect(self, uid, redirect=None):
		return redirect if redirect else '/elearning'

	@http.route('/admission', type='http', auth="public", sitemap=False)
	def admission(self, redirect=None, **kw):
		ensure_db()
		request.params['login_success'] = False
		if request.httprequest.method == 'GET' and redirect and request.session.uid:
			return http.redirect_with_hash(redirect)

		if not request.uid:
			request.uid = odoo.SUPERUSER_ID

		values = request.params.copy()
		try:
			values['databases'] = http.db_list()
		except odoo.exceptions.AccessDenied:
			values['databases'] = None

		if request.httprequest.method == 'POST':
			old_uid = request.uid
			try:
				# uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
				# request.params['login_success'] = True
				login = values.get('login')
				request.env['res.users'].sudo().confirm_email_login(login)
				values['message'] = _("An email has been sent with credentials to reset your password")
				# return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
			except odoo.exceptions.AccessDenied as e:
				request.uid = old_uid
				if e.args == odoo.exceptions.AccessDenied().args:
					values['error'] = _("Wrong login/password")
				else:
					values['error'] = e.args[0]
		else:
			if 'error' in request.params and request.params.get('error') == 'access':
				values['error'] = _('Only employee can access this database. Please contact the administrator.')

		if 'login' not in values and request.session.get('auth_login'):
			values['login'] = request.session.get('auth_login')

		if not odoo.tools.config['list_db']:
			values['disable_database_manager'] = True

		if 'debug' in values:
			values['debug'] = True

		response = request.render('vit_elearning.admission', values)
		response.headers['X-Frame-Options'] = 'ALLOW'
		return response

	def web_login(self, *args, **kw):
		ensure_db()
		response = self.admission(*args, **kw)
		response.qcontext.update(self.get_auth_signup_config())
		if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
			# Redirect if already logged in and redirect param is present
			return http.redirect_with_hash(request.params.get('redirect'))
		return response

	@http.route('/admission2', type='http', auth="public", sitemap=False)
	def admission2(self, redirect=None, **kw):
		ensure_db()
		request.params['login_success'] = False
		if request.httprequest.method == 'GET' and redirect and request.session.uid:
			return http.redirect_with_hash(redirect)

		if not request.uid:
			request.uid = odoo.SUPERUSER_ID

		values = request.params.copy()
		try:
			values['databases'] = http.db_list()
		except odoo.exceptions.AccessDenied:
			values['databases'] = None

		if request.httprequest.method == 'POST':
			old_uid = request.uid
			try:
				uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
				request.params['login_success'] = True
				
				return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
			except odoo.exceptions.AccessDenied as e:
				request.uid = old_uid
				if e.args == odoo.exceptions.AccessDenied().args:
					values['error'] = _("Wrong login/password")
				else:
					values['error'] = e.args[0]
		else:
			if 'error' in request.params and request.params.get('error') == 'access':
				values['error'] = _('Only employee can access this database. Please contact the administrator.')

		if 'login' not in values and request.session.get('auth_login'):
			values['login'] = request.session.get('auth_login')

		if not odoo.tools.config['list_db']:
			values['disable_database_manager'] = True

		if 'debug' in values:
			values['debug'] = True

		response = request.render('vit_elearning.admission', values)
		response.headers['X-Frame-Options'] = 'ALLOW'
		return response

	def web_login(self, *args, **kw):
		ensure_db()
		response = self.admission(*args, **kw)
		response.qcontext.update(self.get_auth_signup_config())
		if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
			# Redirect if already logged in and redirect param is present
			return http.redirect_with_hash(request.params.get('redirect'))
		return response


	@http.route('/register', type='http', auth='public', website=True, sitemap=False)
	def register(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()

		if not qcontext.get('token') and not qcontext.get('signup_enabled'):
			raise werkzeug.exceptions.NotFound()

		if 'error' not in qcontext and request.httprequest.method == 'POST':
			try:
				self.do_signup(qcontext)
				# Send an account creation confirmation email
				if qcontext.get('token'):
					user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
					template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
					if user_sudo and template:
						template.sudo().with_context(
							lang=user_sudo.lang,
							auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
						).send_mail(user_sudo.id, force_send=True)
				return self.web_login(*args, **kw)
			except UserError as e:
				qcontext['error'] = e.name or e.value
			except (SignupError, AssertionError) as e:
				if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
					qcontext["error"] = _("Another user is already registered using this email address.")
				else:
					_logger.error("%s", e)
					qcontext['error'] = _("Could not create a new account.")

		response = request.render('vit_elearning.register', qcontext)
		response.headers['X-Frame-Options'] = 'ALLOW'
		return response

	@http.route('/reset_password', type='http', auth='public', website=True, sitemap=False)
	def el_reset_password(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()

		if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
			raise werkzeug.exceptions.NotFound()

		if 'error' not in qcontext and request.httprequest.method == 'POST':
			try:
				if qcontext.get('token'):
					self.do_signup(qcontext)
					return self.web_login(*args, **kw)
				else:
					login = qcontext.get('login')
					assert login, _("No login provided.")
					_logger.info(
						"Password reset attempt for <%s> by user <%s> from %s",
						login, request.env.user.login, request.httprequest.remote_addr)
					request.env['res.users'].sudo().reset_el_password(login)
					qcontext['message'] = _("An email has been sent with credentials to reset your password")
			except UserError as e:
				qcontext['error'] = e.name or e.value
			except SignupError:
				qcontext['error'] = _("Could not reset your password")
				_logger.exception('error when resetting password')
			except Exception as e:
				qcontext['error'] = str(e)

		response = request.render('vit_elearning.reset_password', qcontext)
		response.headers['X-Frame-Options'] = 'ALLOW'
		return response

	def get_auth_signup_config(self):
		"""retrieve the module config (which features are enabled) for the login page"""

		get_param = request.env['ir.config_parameter'].sudo().get_param
		return {
			'signup_enabled': request.env['res.users']._get_signup_invitation_scope() == 'b2c',
			'reset_password_enabled': get_param('auth_signup.reset_password') == 'True',
		}

	def get_auth_signup_qcontext(self):
		""" Shared helper returning the rendering context for signup and reset password """
		qcontext = request.params.copy()
		qcontext.update(self.get_auth_signup_config())
		if not qcontext.get('token') and request.session.get('auth_signup_token'):
			qcontext['token'] = request.session.get('auth_signup_token')
		if qcontext.get('token'):
			try:
				# retrieve the user info (name, login or email) corresponding to a signup token
				token_infos = request.env['res.partner'].sudo().signup_retrieve_info(qcontext.get('token'))
				for k, v in token_infos.items():
					qcontext.setdefault(k, v)
			except:
				qcontext['error'] = _("Invalid signup token")
				qcontext['invalid_token'] = True
		return qcontext

	def do_signup(self, qcontext):
		""" Shared helper that creates a res.partner out of a token """
		values = { key: qcontext.get(key) for key in ('login', 'name', 'password', 'mobile') }
		if not values:
			raise UserError(_("The form was not properly filled in."))
		if values.get('password') != qcontext.get('confirm_password'):
			raise UserError(_("Passwords do not match; please retype them."))
		supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
		if request.lang in supported_langs:
			values['lang'] = request.lang

		# Tambah tags res.partner yang daftar dari e-Learning =======================
		elearning_categ = request.env.ref('e_learning.res_partner_category_elearning')
		values['category_id'] = [(4, elearning_categ.id)]
		self._signup_with_values(qcontext.get('token'), values)
		request.env.cr.commit()

	def _signup_with_values(self, token, values):
		db, login, password = request.env['res.users'].sudo().signup(values, token)
		request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
		uid = request.session.authenticate(db, login, password)
		if not uid:
			raise SignupError(_('Authentication Failed.'))



	@http.route("/search_page", auth='public')
	def searchpage(self, **kw):
		name=kw.get('name')
		offset=kw.get('offset',0)
		offset=int(offset)
		e_categories = request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		e_learning_ids = request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('name', 'ilike', name), ('state', '=', 'publish')],offset=offset, limit=9)
		pages = request.env['e_learning.e_learning'].sudo().search([('id', '!=', None), ('name', 'ilike', name), ('state', '=', 'publish')],)
		pages= len(pages)/9
		pages= math.ceil(pages)
		
		return request.render("vit_elearning.search_page", {
			'pages'				: pages,
			'e_categories'		: e_categories,
			'e_learning_ids'	: e_learning_ids,
		})

	@http.route("/subscribe", auth='public')
	def subscribe(self, **kw):
		e_categories = request.env['e_learning.category'].sudo().search([('id', '!=', None)])
		e_learning_ids = request.env['e_learning.e_learning']
		user_id 		= request.env.uid
		user 			= request.env['res.users'].sudo().search([('id','=',user_id)])
		if user:
			for u in user:
				kw.update({
					'id' 			: u.id,
					'partner_id'	: u.partner_id.id,
					})
				u.sudo().write(kw)
				return request.render("vit_elearning.elearning", {
					'e_categories'		: e_categories,
					'e_class_ids'		: e_learning_ids.sudo().search([('id', '!=', None), ('online_class', '=', True),('state', '=', 'publish')],limit=6),
					'e_seminar_ids'		: e_learning_ids.sudo().search([('id', '!=', None), ('online_seminar', '=', True),('state', '=', 'publish')],limit=3),
				})
		else :			
			return request.render("vit_elearning.admission", {})
# encoding=utf-8
import json

from flask import render_template, request, current_app, jsonify, session, url_for, redirect, Response, make_response
from app.models import App, Platform, Comment, Admin, Theta, User, KeyWord
from . import main


@main.route('/api/login_status')
def login_status():
	if 'user' not in session.keys():
		return jsonify(None)

	else:
		user_id = session['user']
		user = User.query.get_or_404(user_id)
		return jsonify({'id': user.id, 'name': user.name})


@main.route('/api/show_type')
def show_type():
	if 'user' not in session.keys():
		admin = Admin.query.first_or_404()
		show_type = admin.setting
	else:
		user_id = session['user']
		user = User.query.get_or_404(user_id)
		show_type = user.show_type
	result = jsonify({'show_type': show_type})
	rsp = make_response(result)
	rsp.headers['Access-Control-Allow-Origin'] = '*'
	return rsp


@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
	# 登录
	if request.method == 'GET':
		return render_template('admin_login.html')
	else:
		data = request.form
		name = data['name']
		password = data['password']
		admin = Admin.query.filter(Admin.name == name).first()
		if (admin == None):
			return {'login': False, 'message': '用户名或密码有误,请重试'}  # 用户名或密码有误
		elif admin.vertify_password(password):
			return {'login': False, 'message': '用户名或密码有误,请重试'}  # 用户名或密码有误
		else:
			session["admin"] = admin.id
			return jsonify({'login':True})


@main.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "GET":
		return render_template('login.html')  # return login
	else:
		data = request.form
		email = data["email"]
		password = data["password"]
		if email==None or password==None:
			return jsonify({'login':False,'message':'邮箱和密码都不能为空，请重试'})
		user = User.query.filter(User.email == email).first()
		if (user == None):
			return jsonify({'login': False, 'message': '邮箱或密码有误,请重试'})  # 用户名或密码有误
		elif not user.vertify_password(password):
			return jsonify({'login': False, 'message': '邮箱或密码有误,请重试'})  # 用户名或密码有误
		else:
			session['user'] = user.id
			return jsonify({'login': True})  # return usercenter


@main.route('/')
def index():
	'''
	主页
	:return:主页
	'''
	return render_template('index.html', endpoint='.index')


@main.route('/app-list')
def app_list():
	'''
	app列表
	:return:app列表，分页后的
	'''
	if 'user' not in session.keys():
		redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int)
	pagination = App.query.paginate(page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
	apps = pagination.items
	return render_template('app_list.html', apps=apps, pagination=pagination, endpoint='.app_list')


@main.route('/app-detail/<int:id>')
def app_detail(id):
	'''
	APP详情
	:param id:APP id
	:return: app内容，根据app平台返回评论
	'''
	if 'user' not in session.keys():
		redirect(url_for('main.index'))
	app = App.query.get_or_404(id)
	platforms = app.platforms.all()
	if 'user' not in session:
		admin = Admin.query.first()
		show_type = admin.setting
	else:
		user_id = session['user']
		user = User.query.get_or_404(user_id)
		show_type = user.show_type
	return render_template('app_detail.html', time_type=show_type, app=app, platforms=platforms)


@main.route('/api/chart/<int:app_id>/<int:show_type>')
def chart_data(app_id, show_type):
	import app.date_util as date
	today = date.today()
	if show_type == 1:
		datetime = date.get_day_of_day(-7)
	elif show_type == 2:
		datetime = date.get_today_month(-1)
	elif show_type == 3:
		datetime = date.get_today_month(-3)
	elif show_type == 4:
		datetime = date.get_today_month(-12)
	else:
		return 404
	data_list = Comment.query.order_by(Comment.post_time.desc()).filter(Comment.app_id == app_id).filter(Comment.post_time >= datetime).filter(
		Comment.post_time <= today).all()
	result = {}
	for d in data_list:
		if not d.post_time.isoformat() in result.keys():
			result[d.post_time.isoformat()] = {'like': 0, 'normal': 0, 'dislike': 0}
		like = d.rate * 0.3 + d.like_rate * 0.5
		if like <= 0.33:
			result[d.post_time.isoformat()]['dislike'] += 1
		elif like > 0.33 and like <= 0.66:
			result[d.post_time.isoformat()]['normal'] += 1
		else:
			result[d.post_time.isoformat()]['like'] += 1
	return jsonify(result)


@main.route('/api/comment/<int:app_id>/<int:pid>/<int:page>', methods=["GET"])
def app_platform_comments(app_id, pid, page):
	'''
	获得评论
	:param app_id: APP id
	:param pid: Platform id
	:param page: page num
	:return: comment list
	'''
	from exts import db
	pagination = Comment.query.order_by(Comment.post_time.desc()).filter(Comment.app_id == app_id).filter(
		Comment.platform_id == pid).paginate(page, per_page=current_app.config['COMMENT_PER_PAGE'], error_out=False)
	result = pagination.items
	list = []
	for r in result:
		comments = {}
		comments['text'] = r.comment_text
		comments['rate'] = r.rate
		comments['post_time'] = r.post_time.isoformat()
		# print(type(r.post_time))
		comments['like_rate'] = r.like_rate
		list.append(comments)

	pages = pagination.pages
	theta1 = 0.3  # Theta.query.filter(Theta.position == 1).first()
	theta2 = 0.5  # Theta.query.filter(Theta.position == 2).first()
	js = jsonify({'pages': pages, 'comments': list, 'theta_1': theta1, 'theta_2': theta2})
	return js  # 返回


@main.route('/api/keyword/<int:appid>')
def keyword(appid):
	from exts import db
	keyword = KeyWord.query.order_by(db.desc(KeyWord.count)).filter(KeyWord.app_id == appid).limit(50)
	list = []
	for k in keyword:
		word = {}
		word['text'] = k.word
		word['weight'] = k.count
		list.append(word)
	result = jsonify(list)
	rsp = make_response(result)
	rsp.headers['Access-Control-Allow-Origin'] = '*'
	return rsp


@main.route('/platform-list')
def platform_list():
	'''
	获得平台列表，由于数量少，不做分页
	:return: 返回平台列表
	'''
	platform_list = Platform.query.all()
	return render_template('platform_list.html', platform_list=platform_list)


@main.route('/charts')
def chartsByTime():
	'''
	获得图表分析需要的值。
	:param appid:APP id
	:param time_type:时间类型，show type: 1 for week 2 for month 3 for season 4 for year
	:return:
	'''
	app_id = request.args.get('app_id', -1, type=int)
	if app_id < 0:
		return jsonify({'status': False, 'message': 'app_id有误'})
	time_type = request.args.get('time_type', default=-1, type=int)
	if time_type <= 0 or time_type > 4:
		return jsonify({'status': False, 'message': 'time_type有误'})
	app = App.query.get_or_404(app_id)
	comments = app.comments
	total = comments.count
	good = comments.filter(Comment.like_rate >= 0.66)
	bad = comments.filter(Comment.like_rate < 0.33)
	return json.dump({'status': True})

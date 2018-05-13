# encoding: utf-8
from flask import render_template, request, session, redirect, url_for, current_app, jsonify

from app.models import User
from . import user


@user.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('main.index'))


@user.route('/center')
def userCenter():
	current_user = get_current_user()
	follow_list = []
	for app in current_user.apps:
		follow_list.append({'name': app.name, 'id': app.id})
	return render_template('user/usercenter.html', user=current_user, list=follow_list)  # return UserCenter Imfo


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user_infomation():
	user = get_current_user()
	pass  # 修改用户信息


@user.route('/follow')
def follow(page):
	user = get_current_user()
	app = user.apps
	page = request.args.get('page', 1, type=int)
	pagination = app.paginate(page, per_page=current_app.config['APP_PER_PAGE'], error_out=False)
	result = pagination.items
	return None  # unfinished


@user.before_request
def before_request():
	user_key = "user"
	if not user_key in session.keys():
		return redirect(url_for('main.login'))  # return login


def get_current_user():
	user_id = session['user']
	user = User.query.get_or_404(user_id)
	return user

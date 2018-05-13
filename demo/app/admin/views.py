# encoding: utf-8
from flask import render_template, session, redirect, url_for, request, jsonify

from app.models import Admin, Comment, Theta, App, Platform
from . import admin


@admin.route('/center')
def adminCenter():
	# 返回管理员中心
	admin = get_current_admin()
	return render_template('admin/admincenter.html', admin=admin)


@admin.route('/app-update', methods=['POST'])
def appCommentUpdate():
	# API_更新APP的评论
	app_id = request.form.get('app_id', type=int)
	platform_id = request.form.get('platform_id', type=int)
	comments = request.form.getlist('comments')
	for comment in comments:
		Comment.add_comment(comment['text'], comment['rate'], comment['time'], app_id, platform_id)
	return jsonify({'status': True})


@admin.route('/logout')
def logout():
	# 注销
	session.clear()
	return redirect(url_for('main.admin_login'))  # return login


@admin.route('/appmgmt', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appManager():
	if request.method == 'GET':  # GET
		apps=App.query.all()
		return render_template('admin/app_mgmt.html',apps=apps)
	elif request.method == 'POST':  # POST
		pass
	elif request.method == 'PUT':  # PUT
		pass
	else:  # DELETE
		pass


@admin.route('/storemgmt', methods=['GET', 'POST', 'PUT', 'DELETE'])
def storeManager():
	if request.method == 'GET':  # GET
		platforms=Platform.query.all()
		return render_template('admin/store_mgmt.html',platforms=platforms)
	elif request.method == 'POST':  # POST
		pass
	elif request.method == 'PUT':  # PUT
		pass
	else:  # DELETE
		pass


@admin.route('/parammgmt', methods=['GET', 'PUT'])
def paramManager():
	if request.method == 'GET':
		theta=Theta.query.all()
		return render_template('admin/param_mgmt.html',theta=theta)
	else:
		pass


@admin.before_request
def before_request():
	key = 'admin'
	if key not in session.keys():
		return redirect(url_for('main.admin_login'))  # return login


def get_current_admin():
	id = session['admin']
	admin = Admin.query.get_or_404(id)
	return admin

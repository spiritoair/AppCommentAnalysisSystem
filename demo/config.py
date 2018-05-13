# coding=utf-8
import os

class Config():
	# DEBUG = True
	# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:jich0526@localhost:3306/AppComment?charset=utf8'
	APP_PER_PAGE=48
	COMMENT_PER_PAGE=20
	PAIR_NUMBER=30
	G=2.745
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY=os.urandom(24)

	@staticmethod
	def init_app(app):
		pass
# coding=utf-8
'''
This module is for the database model.
'''
from datetime import datetime

from app.util import word_segment, get_sentence_sentiment
from exts import db

follow = db.Table("follow",
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                  db.Column('app_id', db.Integer, db.ForeignKey('app.id'), primary_key=True))
app_platform_table = db.Table("app_platform_table",
                              db.Column('app_id', db.Integer, db.ForeignKey('app.id'), primary_key=True),
                              db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64), nullable=False)
    apps = db.relationship('App', secondary=follow, backref=db.backref('apps', lazy='dynamic'))
    show_type = db.Column(db.SmallInteger)  # 1 for week 2 for month 3 for season 4 for year

    def __init__(self, **kwargs):
        admin = Admin.query.first()
        self.show_type = admin.setting

    def vertify_password(self, password):
        return self.password == password

    def change_password(self, password):
        try:
            self.password = password
            db.session.commit()
        except:
            db.session.rollback()

    def add_app(self, app_id):
        list = self.apps
        app = App.query.get(app_id)
        list.append(app)
        self.apps = list
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def add_user(name, email, password):
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()


class App(db.Model):
    __tablename__ = 'app'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    last_update_time = db.Column(db.DateTime)
    # platforms = db.relationship('Platform', secondary=app_platform_table, backref=db.backref('apps', lazy='dynamic'))
    comments = db.relationship('Comment', backref='app', lazy='dynamic')

    # users = db.relationship('User', secondary=follow, backref=db.backref('users', lazy='dynamic'))

    @staticmethod
    def add_app(name, platform_ids):
        app = App(name=name, last_update_time=datetime.min)
        list = []
        for id in platform_ids:
            p = Platform.query.get(id)
            list.append(p)
        app.platforms = list
        db.session.add(app)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def delete_app(app_id):
        app = App.query.get(int(app_id))
        comments = app.comments
        for c in comments:
            db.session.delete(c)

        try:
            db.session.commit()
        except:
            db.session.rollback()


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_text = db.Column(db.Text)
    rate = db.Column(db.Float)  # 用户打分
    post_time = db.Column(db.Date)
    like_rate = db.Column(db.Float)  # 喜欢率
    junk = db.Column(db.Boolean, nullable=True)
    app_id = db.Column(db.Integer, db.ForeignKey('app.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))

    @staticmethod
    def add_comment(comment_text, rate, post_time, app_id, platform_id):
        comment = Comment(comment_text=comment_text, rate=rate, post_time=post_time, app_id=app_id,
                          platform_id=platform_id)
        segmentations = word_segment(comment_text)
        word_dict = {}
        for seg in segmentations:  # 分词
            word_dict[seg] = word_dict.get(seg, 0) + 1
        for word in word_dict.keys():
            KeyWord.add_word(app_id, word, word_dict[word])
        like = get_sentence_sentiment(segmentations)
        comment.like_rate = like
        db.session.add(comment)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def like_rate_setter(self, rate):
        self.like_rate = rate
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def junk_setter(self, junk):
        self.junk = junk
        try:
            db.session.commit()
        except:
            db.session.rollback()


class KeyWord(db.Model):
    __tablename__ = 'keyword'
    app_id = db.Column(db.Integer, db.ForeignKey('app.id'), nullable=False, primary_key=True)
    word = db.Column(db.String(64), nullable=False, index=True, primary_key=True)
    count = db.Column(db.Integer)

    @staticmethod
    def add_word(app_id, word, count):
        result = KeyWord.query.filter(app_id=app_id, word=word).first()
        if result == None:
            # 无此词语，创建新纪录
            keyword = KeyWord(app_id=app_id, word=word, count=count)
            db.session.add(keyword)
        else:
            # 有此词语，计数更新
            result.count = result.count + count
        try:
            db.session.commit()
        except:
            db.session.rollback()


class Platform(db.Model):
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True, index=True)
    comments = db.relationship('Comment', backref='platform', lazy='dynamic')

    apps = db.relationship('App', secondary=app_platform_table, backref=db.backref('platforms', lazy='dynamic'),
                           lazy='dynamic')

    @staticmethod
    def add_platform(name):
        platform = Platform(name=name)
        db.session.add(platform)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def name_setter(self, name):
        self.name = name
        try:
            db.session.commit()
        except:
            db.session.rollback()


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    setting = db.Column(db.SmallInteger, nullable=False,
                        default=1)  # default show type: 1 for week 2 for month 3 for season 4 for year

    def vertify_password(self, password):
        return self.password != password


class Theta(db.Model):
    __tablename__ = 'theta'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True)
    num = db.Column(db.Float, nullable=False)

    @staticmethod
    def add_theta(position, num):
        theta = Theta(position=position, num=num)
        db.session.add(theta)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    @staticmethod
    def vertify_theta(position, num):
        theta = Theta.query().filter(Theta.position == position).first()
        if theta is None:
            return False
        theta.num = num
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return True

# encoding=utf-8
from flask import Flask

import config
from exts import db

app = Flask(__name__, static_folder='app/static')
db.init_app(app)
app.config.from_object(config.Config)


from app.user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix="/user")

from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")



if __name__ == '__main__':
	app.run(debug=True)

import os
from flask import (
    Flask,
    g,
    session,
    request,
    )
from flask_assets import Environment
from flask_compress import Compress
from flask_login import (
    LoginManager,
    current_user,
)
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from flask_babel import Babel
from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config
from flask_debugtoolbar import DebugToolbarExtension

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
cache = Cache(config={'CACHE_TYPE': 'redis'})
ma = Marshmallow()
babel = Babel()
# for debugging
# toolbar = DebugToolbarExtension()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    # toolbar.init_app(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .modules.contacts import contacts as modules_contacts_blueprint
    app.register_blueprint(modules_contacts_blueprint, url_prefix='/account/contacts')

    from .modules.search import search as modules_search_blueprint
    app.register_blueprint(modules_search_blueprint, url_prefix='/')

    from .modules.messages import messages as modules_messages_blueprint
    app.register_blueprint(modules_messages_blueprint, url_prefix='/account/messages')

    from .modules.tasks import tasks as modules_task_blueprint
    app.register_blueprint(modules_task_blueprint, url_prefix='/account/tasks')

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .modules.api import api as modules_api_blueprint
    app.register_blueprint(modules_api_blueprint, url_prefix='/api/v1')

    from .modules.statistics import statistics as modules_statistics_blueprint
    app.register_blueprint(modules_statistics_blueprint)

    from .modules.emails import emails as modules_emails_blueprint
    app.register_blueprint(modules_emails_blueprint, url_prefix='/account/emails')

    # External Modules

    from .modules.offers import offers as modules_offers_blueprint
    app.register_blueprint(modules_offers_blueprint, url_prefix='/')

    @babel.localeselector
    def get_locale():
        if request.args.get('lang'):
            session['lang'] = request.args.get('lang')

        if current_user.is_authenticated:
            session["lang"] = current_user.default_language

        return session.get('lang', 'en')

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, "user", None)
        if user is not None:
            return user.timezone

    return app

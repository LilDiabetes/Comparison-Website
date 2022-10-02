from flask import Flask
from src.config import ConfigMain
from src.extensions import db, login_manager, admin, migrate
from flask_admin.menu import MenuLink
from src.admin import UserView, RoleView, UserRoleView
from src.models.user_models import User, Role, UserRoles

def create_app():
    application = Flask(__name__)
    application.config.from_object(ConfigMain)
    register_extension(application)
    register_blueprints(application)
    return application


def register_extension(application):
    db.init_app(application)
    migrate.init_app(application, db)
    login_manager.init_app(application)
    admin.init_app(application)
    admin.add_view(UserView(User, db.session, category='User Management'))
    admin.add_view(RoleView(Role, db.session, category='User Management'))
    admin.add_view(UserRoleView(UserRoles, db.session, category='User Management'))
    admin.add_link(MenuLink(name='Dashboard', url='/'))
    admin.add_link(MenuLink(name='Logout', url='/auth.logout'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(application):
    from webpages.views import auth_blueprint

    application.register_blueprint(auth_blueprint)


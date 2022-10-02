from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, request

class AuthMixin(object):

    def is_accessible(self):
        return current_user.has_roles('Admin')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("auth.login"))



class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_roles('Admin')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("auth.login"))


class UserView(ModelView, AuthMixin):

    can_create = True
    can_delete = True
    can_edit = True
    column_exclude_list = ['password', ]
    column_searchable_list = ['username', 'email']
    column_filters = ['roles']
    column_editable_list = ['username', 'email', 'roles']
    can_export = True


class RoleView(ModelView,AuthMixin):


    can_create = False
    can_delete = False
    can_edit = True
    column_searchable_list = ['name']
    column_filters = ['name']
    column_editable_list = ['name']
    can_export = True


class UserRoleView(ModelView,AuthMixin):


    can_create = True
    can_delete = True
    can_edit = True
    column_searchable_list = ['id', 'user_id', 'role_id']
    column_filters = ['id', 'user_id', 'role_id']
    column_list = ('id', 'user_id', 'role_id')
    can_export = True


from saleapp.models import Category, Product, User, UserRole
from saleapp import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

admin = Admin(app=app, name='Quản Trị Bán Hàng', template_mode='bootstrap4')


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductView(ModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_exclude_list = ['image']
    column_labels = {
        'name': 'Tên Sản Phẩm',
        'description': 'Mô Tả',
        'price': 'Giá',
    }

    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

    def is_accessible(self):
        return current_user.is_authenticated



    # def auth_admin(self):
    #     Kq = User.query.filter(User.user_role)
    #     if Kq == UserRole.ADMIN:
    #         admin = Admin(app=app, name='Quản Trị Bán Hàng', template_mode='bootstrap4')
    #         admin.add_view(ModelView(Category, db.session, name='Danh Mục'))
    #         admin.add_view(ProductView(Product, db.session, name='Sản Phẩm'))
    #         admin.add_view(StatsView(name='Thống Kê'))
    #     return Kq


class StatsView(BaseView):
    @expose('/')
    def __index__(self):
        return self.render('admin/stats.html')

Kq=current_user.user_role
admin.add_view(ModelView(Category, db.session, name='Danh Mục'))
admin.add_view(ProductView(Product, db.session, name='Sản Phẩm'))
admin.add_view(StatsView(name='Thống Kê'))

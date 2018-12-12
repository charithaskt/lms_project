from collections import OrderedDict

from django.utils.html import format_html
#from django.contrib.auth.models import User
from accounts.models import User, Profile
from django_jinja_knockout.tpl import format_local_date, Str
from django_jinja_knockout.views import KoGridView

from ils_app.models import Biblio, Items, CollectionDepartments, Reserves, Borrowers, Categories, Departments, Designations, CorporateAuthor, Genre
from .models import Action


class UserFkWidgetGrid(KoGridView):

    model = User
    grid_fields = [
        # Compound columns:
        [
            'email',
            'fullname',
        ],
        [
            'is_superuser',
            'staff',
            'admin',
            'active',
        ],
        [
            'last_login',
            'email_confirmed',
        ]
    ]
    search_fields = [
        ('fullname', 'icontains'),
        ('email', 'icontains'),
    ]
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('is_superuser', None),
        ('staff', None),
        ('active', None),
        ('last_login', None),
        ('email_confirmed', None),
    ])

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        str_fields = {
            'last_login': '' if obj.last_login is None else format_local_date(obj.last_login),
        }
        return str_fields


class ActionGrid(KoGridView):

    client_routes = {
        'user_fk_widget_grid'
    }
    model = Action
    grid_fields = [
        # Compound columns:
        [
            'performer',
            'date',
            'action_type',
        ],
        'content_type',
        'content_object'
    ]
    # Autodetection of related_models is impossible because Action model has generic relationships.
    related_models = [Biblio, Items, CollectionDepartments, Reserves, Borrowers]
    allowed_sort_orders = [
        'performer',
        'date',
        'action_type',
    ]
    mark_safe_fields = [
        'content_type'
    ]
    enable_deletion = True
    grid_options = {
        'selectMultipleRows': True,
        'highlightMode': 'linearRows',
        # Use fkGridOptions to setup allowed_filter_fields['performer'].
        'fkGridOptions': {
            'performer': {
                'pageRoute': 'user_fk_widget_grid',
                # Optional setting for BootstrapDialog:
                'dialogOptions': {'size': 'size-wide'},
            }
        }
    }

    def get_allowed_filter_fields(self):
        allowed_filter_fields = OrderedDict([
            ('performer', None),
            # Autodetect foreign key grid fkGridOptions, instead of explicitly specifying them in grid_options.
            # ('performer', {
            #    'pageRoute': 'user_fk_widget_grid',
            #    # Optional setting for BootstrapDialog:
            #    'dialogOptions': {'size': 'size-wide'},
            # }),
            ('date', None),
            ('action_type', None),
            ('content_type', self.get_contenttype_filter(
                ('ils_app', 'biblio'),
                ('ils_app', 'items'),
                ('ils_app', 'reserves'),
            ))
        ])
        return allowed_filter_fields

    def get_field_verbose_name(self, field_name):
        if field_name == 'content_object':
            return 'Object description'
        else:
            return super().get_field_verbose_name(field_name)

    def get_related_fields(self, query_fields=None):
        query_fields = super().get_related_fields(query_fields)
        # Remove virtual field from queryset values().
        query_fields.remove('content_object')
        return query_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        content_object = obj.content_object
        row['content_object'] = content_object.get_str_fields() \
            if hasattr(content_object, 'get_str_fields') \
            else str(content_object)
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        if hasattr(obj.content_object, 'get_absolute_url'):
            link = obj.content_object.get_absolute_url()
            str_fields['content_type'] = format_html(
                '<a href="{}" target="_blank">{}</a>',
                link,
                str_fields['content_type']
            )
        return str_fields

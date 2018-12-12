from django_jinja_knockout.views import ListSortingView, ContextDataMixin

from .models import Action


class ActionList(ContextDataMixin, ListSortingView):
    # Enabled always visible paginator links because there could be many pages of actions, potentially.
    always_visible_links = True
    model = Action
    grid_fields = [
        [
            'performer',
            'performer__is_superuser',
            'date',
        ],
        'action_type',
        'content_object'
    ]
    allowed_sort_orders = [
        'performer',
        'date',
        'action_type',
    ]

    def get_allowed_filter_fields(self):
        allowed_filter_fields = {
            'action_type': None,
            'content_type': self.get_contenttype_filter(
                ('ils_app', 'biblio'),
                ('ils_app', 'items'),
                ('ils_app', 'reserves'),
            )
        }
        return allowed_filter_fields

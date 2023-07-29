"""Utils"""
from django.db.models import Count

from .models import Category

menu = [
    # {'title': "Сервисы", 'url_name': 'services_main'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


class DataMixin:
    """Миксин"""

    paginate_by = 20

    def get_user_context(self, **kwargs):
        """get"""
        context = kwargs
        cats = Category.objects.annotate(Count('post'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

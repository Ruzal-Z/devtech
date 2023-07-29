from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import AddPostForm, RegisterUserForm
from .models import Category, Post
from .utils import DataMixin, menu


class PostHome(DataMixin, ListView):
    """
    Класс, отображающий список всех опубликованных статей на домашней странице.
    """

    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет дополнительный контекст к контексту страницы."""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Dev Technology")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        """Возвращает queryset из всех опубликованных статей."""
        return Post.objects.filter(is_published=True).select_related('cat')


def about(request):
    """Отображает страницу "О сайте"."""
    return render(
        request, 'posts/about.html', {'menu': menu, 'title': 'О сайте'}
    )


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """
    Класс, позволяющий зарегистрированным пользователям
    добавлять статьи на сайт.
    """

    form_class = AddPostForm
    template_name = 'posts/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет дополнительный контекст к контексту страницы."""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    """Отображает страницу контактов."""
    return render(request, 'posts/contact.html', {'contact': contact})


def pageNotFound(request, exception):
    """Обработчик страницы 404 ошибки."""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    """Класс, отображающий конкретную статью."""

    model = Post
    template_name = 'posts/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет дополнительный контекст к контексту страницы."""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class PostCategory(DataMixin, ListView):
    """Класс, отображающий список статей в заданной категории."""

    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post'
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(
            cat__slug=self.kwargs['cat_slug'], is_published=True
        ).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория - ' + str(c.name), cat_selected=c.pk
        )
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    """Регистрация пользователей.При успешной регистрации происходит
    автоматический вход в систему и перенаправление на главную страницу.
    """

    form_class = RegisterUserForm
    template_name = 'posts/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет дополнительный контекст к контексту страницы."""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        """Метод, вызываемый при успешной проверке формы регистрации."""
        user = form.save()
        login(self.request, user)
        return redirect('home')

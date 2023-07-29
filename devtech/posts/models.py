from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    Посты с заголовком, текстом, изображением,
    временем создания и изменения, статусом публикации и привязкой к категории.
    """

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото"
    )
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания"
    )
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения"
    )
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name="Категории"
    )

    def __str__(self):
        """
        Возвращает заголовок статьи в качестве ее строкового представления.
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для данной статьи.
        """
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        """Определяет метаданные модели статьи."""

        verbose_name = 'IT-статьи'
        verbose_name_plural = 'IT-статьи'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    """Категорий, к которым можно привязывать статьи."""

    name = models.CharField(
        max_length=100, db_index=True, verbose_name="Категория"
    )
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self):
        """Возвращает имя категории в качестве ее строкового представления."""
        return self.name

    def get_absolute_url(self):
        """Возвращает URL-адрес для данной категории."""
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        """Определяет метаданные модели категории."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


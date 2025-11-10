from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    color = models.CharField(max_length=7, default="#2D5016", verbose_name="Цвет")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Headline(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Краткое описание")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True, verbose_name="Изображение")
    pdf_file = models.FileField(upload_to='news_pdfs/', blank=True, null=True, verbose_name="PDF файл")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']
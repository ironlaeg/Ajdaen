from django.contrib import admin
from .models import Headline, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at', 'published_at']
    list_filter = ['status', 'tags', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['status']
    readonly_fields = ['created_at']
    date_hierarchy = 'published_at'
    filter_horizontal = ['tags']

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description', 'content', 'image', 'pdf_file', 'author')
        }),
        ('Категоризация', {
            'fields': ('tags',)
        }),
        ('Даты и статус', {
            'fields': ('status', 'published_at', 'created_at')
        }),
    )
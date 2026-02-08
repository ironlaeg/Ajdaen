from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Count
from datetime import datetime
from collections import defaultdict

from news.models import Headline, Tag
from news.forms import HeadlineForm


class MonthlyLinksMixin:
    
    def get_russian_month_name(self, year, month):
        months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        return f"{months[month-1]} {year}"
    
    def get_monthly_links(self):
        from django.db.models import Count

        months = Headline.objects.filter(
            status='published',
            published_at__isnull=False
        ).extra(
            select={
                'year': 'strftime("%%Y", published_at)',
                'month': 'strftime("%%m", published_at)',
            }
        ).values('year', 'month').annotate(count=Count('id')).order_by('-year', '-month').distinct()
        
        monthly_links = []
        for month_data in months:
            if month_data['year'] and month_data['month']:
                year = int(month_data['year'])
                month = int(month_data['month'])
                monthly_links.append({
                    'year': year,
                    'month': month,
                    'month_name': self.get_russian_month_name(year, month),
                    'count': month_data['count']
                })
        
        return monthly_links
    
    def get_popular_tags(self):
        return Tag.objects.annotate(
            news_count=Count(
                'headline',
                filter=Q(headline__status='published') & Q(headline__published_at__isnull=False)
            )
        ).filter(news_count__gt=0).order_by('-news_count')[:10]


class HeadlineListView(MonthlyLinksMixin, ListView):
    model = Headline
    template_name = 'headline_list.html'
    context_object_name = 'headlines'
    paginate_by = 10
    ordering = ['-published_at']

    def get_queryset(self):
        queryset = Headline.objects.filter(
            status='published',
            published_at__isnull=False
        ).select_related('author').prefetch_related('tags').distinct()

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(short_description__icontains=search_query)
            )

        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug).distinct()

        return queryset.order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')

        context['monthly_links'] = self.get_monthly_links()

        context['popular_tags'] = self.get_popular_tags()

        context['current_tag'] = self.request.GET.get('tag')
        
        return context


class HeadlineDetailView(MonthlyLinksMixin, DetailView):
    model = Headline
    template_name = 'headline_detail.html'
    context_object_name = 'headline'

    def get_queryset(self):
        return Headline.objects.select_related('author').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_headlines'] = Headline.objects.filter(
            status='published',
            published_at__isnull=False
        ).exclude(
            pk=self.object.pk
        )[:5]

        context['monthly_links'] = self.get_monthly_links()

        context['popular_tags'] = self.get_popular_tags()
        
        return context


class HeadlineCreateView(LoginRequiredMixin, CreateView):
    model = Headline
    form_class = HeadlineForm
    template_name = 'headline_form.html'
    success_url = reverse_lazy('news:headline_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published' and not form.instance.published_at:
            from django.utils import timezone
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Новость успешно создана!')
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if self.request.POST:
            messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return kwargs


class HeadlineUpdateView(LoginRequiredMixin, UpdateView):
    model = Headline
    form_class = HeadlineForm
    template_name = 'headline_form.html'

    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_at:
            from django.utils import timezone
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Новость успешно обновлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.POST:
            messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('news:headline_detail', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user
        return kwargs


class HeadlineDeleteView(LoginRequiredMixin, DeleteView):
    model = Headline
    template_name = 'headline_confirm_delete.html'
    success_url = reverse_lazy('news:headline_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Новость успешно удалена!')
        return super().delete(request, *args, **kwargs)


class HeadlineDraftListView(LoginRequiredMixin, ListView):
    model = Headline
    template_name = 'headline_draft_list.html'
    context_object_name = 'headlines'
    paginate_by = 10

    def get_queryset(self):
        return Headline.objects.filter(
            status='draft',
            author=self.request.user
        ).select_related('author').prefetch_related('tags').order_by('-created_at')


class HeadlineMonthArchiveView(MonthlyLinksMixin, ListView):
    model = Headline
    template_name = 'headline_month.html'
    context_object_name = 'headlines'
    paginate_by = 10

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']
        return Headline.objects.filter(
            status='published',
            published_at__year=year,
            published_at__month=month
        ).select_related('author').prefetch_related('tags').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']

        from django.utils import timezone
        context['archive_year'] = year
        context['archive_month'] = month
        context['archive_month_name'] = self.get_russian_month_name(year, month)

        context['monthly_links'] = self.get_monthly_links()

        context['popular_tags'] = self.get_popular_tags()
        
        return context


class HeadlineArchiveView(MonthlyLinksMixin, ListView):
    model = Headline
    template_name = 'headline_archive.html'
    context_object_name = 'headlines'

    def get_queryset(self):
        return Headline.objects.filter(status='published', published_at__isnull=False).select_related('author').prefetch_related('tags').order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        headlines = self.get_queryset()
        archive_data = defaultdict(lambda: defaultdict(list))
        
        for headline in headlines:
            year = headline.published_at.year
            month = headline.published_at.month
            archive_data[year][month].append(headline)

        archive_list = []
        for year in sorted(archive_data.keys(), reverse=True):
            year_data = {'year': year, 'months': []}
            for month in sorted(archive_data[year].keys(), reverse=True):
                month_data = {
                    'month': month,
                    'month_name': self.get_russian_month_name(year, month).split()[0],  # Only month name
                    'headlines': archive_data[year][month]
                }
                year_data['months'].append(month_data)
            archive_list.append(year_data)
        
        context['archive_data'] = archive_list

        context['monthly_links'] = self.get_monthly_links()

        context['popular_tags'] = self.get_popular_tags()
        
        return context


class TagListView(MonthlyLinksMixin, ListView):
    model = Headline
    template_name = 'headline_list.html'
    context_object_name = 'headlines'
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Headline.objects.filter(
            status='published',
            published_at__isnull=False,
            tags=self.tag
        ).select_related('author').prefetch_related('tags').order_by('-published_at').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['page_title'] = f'Новости с тегом: {self.tag.name}'
        context['monthly_links'] = self.get_monthly_links()
        context['popular_tags'] = self.get_popular_tags()
        context['current_tag'] = self.tag.slug
        
        return context
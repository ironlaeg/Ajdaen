from builtins import super

from django import forms
from .models import Headline, Tag


class HeadlineForm(forms.ModelForm):
    class Meta:
        model = Headline
        fields = ['title', 'short_description', 'content', 'image', 'pdf_file', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf,.pdf'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Устанавливаем queryset для тегов
        self.fields['tags'].queryset = Tag.objects.all()

        # Ограничиваем выбор статуса для обычных пользователей
        if user and not user.is_staff:
            self.fields['status'].choices = [
                ('draft', 'Черновик'),
                ('published', 'Опубликовано'),
            ]
        else:
            # Для staff показываем все варианты статуса
            self.fields['status'].choices = Headline.STATUS_CHOICES
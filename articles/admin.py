from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass

class TagsInlineFormset(BaseInlineFormSet):

    def clean(self):
        super(TagsInlineFormset, self).clean()
        error_checked = 0
        for form in self.forms:
            if not form.is_valid():
                return
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['is_main']:
                    error_checked += 1

        if error_checked != 1:
            raise ValidationError('Пожалуйста, выберите одну основную тему')

        return super().clean()


class TableInline(admin.TabularInline):
      model = Tag
      formset = TagsInlineFormset


class ArticleAdmin(admin.ModelAdmin):

    inlines = [
        TableInline
    ]

admin.site.register(Article, ArticleAdmin)

from django.contrib import admin
from .models import Article
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
     list_display = ['name', 'title', 'description']


admin.site.register(Article, ArticleAdmin)

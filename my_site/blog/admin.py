"""
這個模塊用於將模型註冊到 Django 的管理後台，並對某些模型進行自定義管理介面的配置。
"""

from django.contrib import admin
from .models import Author, Post, Tag, Comment, Cash, Stock

# 註冊你的模型到 Django 管理後台

class PostAdmin(admin.ModelAdmin):
    """
    自定義 Post 模型的管理後台顯示，包括過濾條件、顯示欄位和自動生成 slug 的功能。
    """
    list_filter = ("title", "author", "date",)
    list_display = ("title", "date", "author",)
    prepopulated_fields = {"slug": ("title",)}  # 自動根據 title 生成 slug
    ordering = ["date"]  # 在後台顯示時按日期升序排列
class CommentAdmin(admin.ModelAdmin):
    """
    自定義 Comment 模型的管理後台顯示，包括顯示的欄位。
    """
    list_display = ("user_name", "post")

# 註冊模型和自定義的管理類到 Django 後台
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cash)
admin.site.register(Stock)

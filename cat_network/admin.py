from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from cat_network.models import CatUser, Post, Comment, Like


@admin.register(CatUser)
class CatUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Additional Info:", {"fields": ("breed", "age", "bio",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional Info:", {"fields": ("breed", "age", "username",)}),)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ("author",)
    ordering = ("-created_at",)
    search_fields = ("title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ("author", "post",)
    ordering = ("-created_at",)
    search_fields = ("text",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ("user", "post",)
    ordering = ("user",)


admin.site.unregister(Group)
from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Category, NewsPost, TagedNewsPost, Item
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publish']
    search_fields = ['title', 'category', 'content']
    list_filter = ['publish']

    class Media:
        js = ('js/tiny.js',)


class ItemAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(TagedNewsPost)


# admin.site.site_title = "Happen in Minya"
admin.site.site_header = "يحدث في المنيا"
admin.site.index_title = "يحدث في المنيا"


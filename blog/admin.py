from django.contrib import admin
from .models import Post,Tag,Course,Appeal
class TagInline(admin.TabularInline):
    model = Tag
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_date')
    search_fields = ('title',)
    inlines = [TagInline]  
    fieldsets = (
        ['Main',{
            'fields':('title','text'),
        }],
        ['Advance',{
            'classes': ('collapse',),
            'fields': ('created_date',),
        }]
 
    )

admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Course)
admin.site.register(Appeal)
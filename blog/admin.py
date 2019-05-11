from django.contrib import admin
from .models import Post,Tag,Course,Appeal,gamee,User
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
class gameAdmin(admin.ModelAdmin):
    list_display=('id','cTitle','cAuthor','cContent','cLink')

class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','password','email','sex','ctime')
    
admin.site.register(User,UserAdmin)
admin.site.register(gamee,gameAdmin)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)
admin.site.register(Course)
admin.site.register(Appeal)
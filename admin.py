from django.contrib import admin
from .models import create_events,profile,Post
class PostAdmin(admin.ModelAdmin):
    pass
admin.site.register(create_events)
admin.site.register(profile)
admin.site.register(Post)

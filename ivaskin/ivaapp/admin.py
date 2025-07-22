from django.contrib import admin
from .models import App, Forclient, Tag, TagForClient, Reviews

# Register your models here.
admin.site.register(App)
admin.site.register(Forclient)
admin.site.register(Tag)
admin.site.register(TagForClient)
admin.site.register(Reviews)
from django.contrib import admin
from feedback.models import Customer, Answer, Note

# We register our models here
admin.site.register(Customer)
admin.site.register(Answer)
admin.site.register(Note)

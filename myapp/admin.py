from django.contrib import admin
from myapp import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Question_Classify)
admin.site.register(models.Question_Catalogue)
admin.site.register(models.Question)
admin.site.register(models.Solve_Question)
admin.site.register(models.Solve_Catalogue)
admin.site.register(models.Solve_Classify)


from django.contrib import admin
from .models import *

admin.site.register(SubjectModel)
admin.site.register(ContributionTypeModel)
admin.site.register(TradeModel)
admin.site.register(ManuscriptModel)
admin.site.register(CheckManuscriptModel)
admin.site.register(ReviewManuscriptModel)


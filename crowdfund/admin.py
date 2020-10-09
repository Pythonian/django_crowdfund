from django.contrib import admin
from .models import Reward, Order, Perk

class PerkInlineAdmin(admin.StackedInline):
    model = Perk


class RewardAdmin(admin.ModelAdmin):
    inlines = [PerkInlineAdmin]


admin.site.register(Reward, RewardAdmin)
admin.site.register(Order)

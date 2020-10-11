from django.contrib import admin
from .models import Reward, Order, Perk

class PerkInlineAdmin(admin.StackedInline):
    model = Perk


class RewardAdmin(admin.ModelAdmin):
    inlines = [PerkInlineAdmin]
    list_display = ['name', 'amount']


admin.site.register(Reward, RewardAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'reward', 'paid']

admin.site.register(Order, OrderAdmin)

from django.contrib import admin
from .models import Reward, Order, Perk, FrequentlyAskedQuestion, FrequentlyAskedQuestionDescription, Gallery, Section


class PerkInlineAdmin(admin.StackedInline):
    model = Perk


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    inlines = [PerkInlineAdmin]
    list_display = ['name', 'amount']


class FrequentlyAskedQuestionDescriptionInline(admin.StackedInline):
    model = FrequentlyAskedQuestionDescription
    extra = 1


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestion(admin.ModelAdmin):
    inlines = [FrequentlyAskedQuestionDescriptionInline]
    list_display = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'reward', 'paid']

admin.site.register(Gallery)
admin.site.register(Section)

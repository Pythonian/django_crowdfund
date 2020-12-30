from django.contrib import admin

from .models import (FrequentlyAskedQuestion, Post,
                     FrequentlyAskedQuestionDescription, Gallery, Order, Perk,
                     Reward, Section)


class PerkInlineAdmin(admin.StackedInline):
    model = Perk


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    inlines = [PerkInlineAdmin]
    list_display = ['name', 'amount']
    prepopulated_fields = {'slug': ('name',)}


class FrequentlyAskedQuestionDescriptionInline(admin.StackedInline):
    model = FrequentlyAskedQuestionDescription
    extra = 1


@admin.register(FrequentlyAskedQuestion)
class FrequentlyAskedQuestion(admin.ModelAdmin):
    inlines = [FrequentlyAskedQuestionDescriptionInline]
    list_display = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'reward', 'paid', 'created']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Gallery)
admin.site.register(Section)
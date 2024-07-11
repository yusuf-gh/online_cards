from django.contrib import admin
from .models import Cards
from django.utils import timezone

class CardAdmin(admin.ModelAdmin):
    
    list_display = ('card_number', 'series', 'card_type', 'expiry_month', 'expiry_year', 'status', 'user')
    readonly_fields = ('card_number', 'card_type', 'expiry_month', 'expiry_year', 'status')
    fields = ('series', 'card_number', 'card_type', 'status', 'user')
    list_filter = ('status', 'card_type', 'expiry_year', 'expiry_month', 'user')
    search_fields = ('card_number', 'series', 'user__username')
    
    def save_model(self, request, obj, form, change):
        # Устанавливаем значения expiry_year и expiry_month, если они не заданы
        if not obj.expiry_year:
            now = timezone.now()
            obj.expiry_year = now.year + 5  # Устанавливаем срок действия карты на 5 лет вперед
        if not obj.expiry_month:
            now = timezone.now()
            obj.expiry_month = now.month

        # Генерация уникального номера карты
        if not obj.card_number:
            obj.card_number = obj.generate_unique_card_number()
        
        # Определяем тип карты на основе серии
        obj.series = obj.card_number[:4]
        if obj.series in obj.VALID_SERIES:
            obj.card_type = obj.VALID_SERIES[obj.series]
        else:
            raise ValueError('Invalid card series')

        obj.check_expiry()
        super().save_model(request, obj, form, change)

admin.site.register(Cards, CardAdmin)
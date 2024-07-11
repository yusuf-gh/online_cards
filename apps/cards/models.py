from django.db import models
from django.utils import timezone
import random
from django.contrib.auth import get_user_model


class Cards(models.Model):
    
    balance = models.IntegerField(
        null=False,
        default=0
    )
    
    CARD_TYPES = (               # названия типов карт
        ('uzcard', 'Uzcard'),
        ('humo', 'Humo'),
    )
    
    VALID_SERIES = {          # серии на номерах карт и их типы под названия
        '8600': 'uzcard',
        '9860': 'humo'
    }
    
    STATUS_CHOICES = (        # статус карты (активна, не активна, просрочена)
        ('active', 'Active'), 
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    )
    
    card_number = models.CharField(       # 16 значный номер карты
        null=False, 
        editable=False,
        max_length=16,
        unique=True
        )
    
    series = models.CharField(
        max_length=4,
        choices=[(key, key) for key in VALID_SERIES.keys()]  # ориентируясь по названию серии выводит саму серию карты 
        )
    
    card_type = models.CharField(          # типы карт (CARD_TYPES) 
        max_length=6,
        choices=CARD_TYPES,
        editable=False
    )
    
    status = models.CharField(         # статус карты при создании  по умолчанию активна 
        max_length=8,
        choices=STATUS_CHOICES,
        default="active",
    )
    
    user = models.ForeignKey(      # принадлежность карты к пользователю
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='cards'
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    expiry_year = models.PositiveIntegerField(editable=False)
    
    expiry_month = models.PositiveIntegerField(editable=False)
    
    
    def save(self, *args, **kwargs): # функция для сохранения/добавления новых карт
        
        if not self.expiry_year:
            now = timezone.now()
            self.expiry_year = now.year + 5 # установка срока годности банковской карты на 5 лет вперет
        if not self.expiry_month:
            now = timezone.now()
            self.expiry_month = now.month  # установка месяца срока годности текущего месяца (ровно 5 лет)

        self.series = self.card_number[:4]  # первые 4 цыфры всех карт идентичны и сохраняются как тип/серия
        
        if self.series in self.VALID_SERIES:                 # проверка и сравнение наличия выбраннй серии в доступных типах карт (VALID_SERIES)
            self.card_type = self.VALID_SERIES[self.series] 
        else:
            raise ValueError("Invalid card series")
        
        self.check_expiry()                 # перезод на следующую функцию по проверку срока годности 
        
        super().save(*args, **kwargs)
    
    
    
    
    
    
    def check_expiry(self):                                          # проверка срока годности 
        if self.expiry_year is None or self.expiry_month is None:     # проверка на то что определены ли сроки годности карты
            raise ValueError("Expiry year and month must not be None")

        expiry_date = timezone.datetime(self.expiry_year, self.expiry_month, 1, tzinfo=None)
        expiry_date = timezone.make_aware(expiry_date)    # проверка осведомленности обьекта о временной зоне 

        now = timezone.now()
        
        if now > expiry_date:      #  проверка и сравнение текущей даты с сроком годности карты 
            self.status = 'expired'
    
    
    
    
    def generate_unique_card_number(self):      # функция создает уникальный номер карты 
                                                #     включая первые 4 цыфры как серия карты и остальные 12 случайным образом
        
        while True:
            
            number = self.series + ''.join(random.choices('0123456789', k=12)) 
            
            if not self.__class__.objects.filter(card_number=number).exists():
                
                return number
    
    
    
    
    def __str__(self):
        return (
            f"Card {self.card_number} (Series: {self.series}, Type: {self.get_card_type_display()}, "        # get_card_type_display() выводит человекочитаемое значение аттрибута card_type
            f"Created at: {self.created_at}, Expires: {self.expiry_month}/{self.expiry_year}, Status: {self.get_status_display()})"
            )
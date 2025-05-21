from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

class Character(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='characters/', blank=True, null=True)

    RARITY_CHOICES = [
        ("нормис", "нормис"),
        ("с особенностями развития", "с особенностями развития"),
        ("смешной", "смешной"),
        ("педик", "педик"),
        ("никита", "никита"),
        ("мега редкий", "мега редкий"),
        ("тупой", "тупой"),
        ("беспримерный", "беспримерный"),
        ("дебильнутый", "дебильнутый"),
        ("позитивный", "позитивный"),
        ("прикольный", "прикольный"),
        ("авторитетный", "авторитетный"),
        ("ебырь", "ебырь"),
        ("армагидон", "армагидон"),
    ]

    # если хочешь использовать выбор (select), надо так:
    rarity = models.CharField(max_length=50, choices=RARITY_CHOICES)

    danger = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    power = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    health = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    speed = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    intelligence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    luck = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    @property
    def general_rate(self):
        return round((self.danger + self.power + self.health + self.speed + self.intelligence + self.luck) / 6)

    def __str__(self):
        return self.name

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='plans/', blank=True, null=True)

    def __str__(self):
        return self.name
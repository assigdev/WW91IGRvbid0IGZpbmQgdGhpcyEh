from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Graphic(models.Model):
    FORMULAS = (
        ('t', 't + 2/t'),
        ('s', 'sin(t)'),
    )

    formula = models.CharField('Функция', max_length=1, default='t', choices=FORMULAS)
    interval = models.PositiveSmallIntegerField(
        'Интервал t, дней',
        validators=[MinValueValidator(1), MaxValueValidator(355)],
        default=1
    )
    dt = models.PositiveSmallIntegerField(
        'Шаг t, часы',
        validators=[MinValueValidator(1), MaxValueValidator(24)],
        default=1
    )
    date = models.DateTimeField('Дата обработки', blank=True, null=True)
    image = models.ImageField(upload_to='graphics', blank=True)
    error = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'График'
        verbose_name_plural = 'Графики'


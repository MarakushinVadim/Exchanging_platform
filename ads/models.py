from django.contrib.auth.models import User
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Ad(models.Model):

    class ConditionChoices(models.TextChoices):
        NEW = 'N', 'Новый'
        USED = 'U', 'Б/У'


    id = models.AutoField(primary_key=True, verbose_name='id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание"
    )
    image_url =  models.ImageField(
        upload_to="media", **NULLABLE, verbose_name="Фото"
    )
    category = models.CharField(
        max_length=100,
        verbose_name= "Категория",
        help_text="Введите категорию"
    )
    condition = models.CharField(
        max_length=1,
        choices=ConditionChoices.choices,
        default=ConditionChoices.NEW,
        verbose_name='Состояние'
    )
    created_at = models.DateField(
        verbose_name='Дата создания записи', **NULLABLE
    )



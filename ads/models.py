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
        verbose_name='Пользователь',
        **NULLABLE
    )
    title = models.CharField(
        max_length=100, verbose_name="Название объявления",
        help_text="Введите название объявления"
    )
    description = models.TextField(
        verbose_name="Описание объявления",
        help_text="Введите описание объявления"
    )
    image_url = models.ImageField(
        upload_to="media", **NULLABLE, verbose_name="Фото"
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Категория",
        help_text="Введите категорию"
    )
    condition = models.CharField(
        max_length=1,
        choices=ConditionChoices.choices,
        default=ConditionChoices.NEW,
        verbose_name='Состояние'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания объявления',
        **NULLABLE
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ExchangeProposal(models.Model):

    class ExchangeChoices(models.TextChoices):
        AWAITS = 'A', 'ожидает'
        TAKEN = 'T', 'принята'
        REJECTED = 'R', 'отклонена'

    id = models.AutoField(primary_key=True, verbose_name='id')
    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE,
        verbose_name='объявление',
        help_text='Выберете свое обьявление для обмена',
        related_name='you_send'
    )
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE,
        verbose_name='объявление',
        help_text='Выберете объявление на которое хотите обменяться',
        related_name='you_receive'
    )
    comment = models.TextField(
        verbose_name='комментарий',
        help_text = 'Напишите комментарий к предложению обмена'
    )
    status = models.CharField(
        max_length=1,
        choices=ExchangeChoices.choices,
        default=ExchangeChoices.AWAITS,
        verbose_name='Статус сделки'
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата предложения',
        **NULLABLE
    )

    def __str__(self):
        return f'Предложение сделки номер - {self.id}'


    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'
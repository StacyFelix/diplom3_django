from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Type(models.Model):
    title_t = models.CharField(max_length=30, verbose_name='Название',)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.title_t


class Subtype(models.Model):
    title_subt = models.CharField(max_length=30, verbose_name='Название',)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип')

    class Meta:
        verbose_name = 'Подтип'
        verbose_name_plural = 'Подтипы'

    def __str__(self):
        return self.title_subt


class Product(models.Model):
    title_pr = models.CharField(max_length=30, verbose_name='Название',)
    description_pr = models.CharField(max_length=100, verbose_name='Описание',)
    amount_pr = models.PositiveIntegerField(verbose_name='Количество',)
    # image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )
    image = models.FileField(null=True, blank=True, upload_to='static/products/', verbose_name='Изображение',)
    subtype = models.ForeignKey(Subtype, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Подтип')
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title_pr


class Article(models.Model):
    title_a = models.CharField(max_length=60, verbose_name='Название',)
    description_a = models.CharField(max_length=100, default='', verbose_name='Описание', )
    published_at = models.DateTimeField(default=now, editable=True, verbose_name='Дата публикации')
    products = models.ManyToManyField(Product, related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title_a


class Order(models.Model):
    status = models.CharField(max_length=30, verbose_name='Статус заказа', )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.pk)


class DetailOrder(models.Model):
    amount_do = models.PositiveIntegerField(verbose_name='Количество', )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, db_index=False, null=True, blank=True, verbose_name='Товар')
    person = models.ForeignKey(User, on_delete=models.CASCADE, db_index=False, null=True, blank=True, verbose_name='Юзер')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, db_index=False, null=True, blank=True, verbose_name='Заказ')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        unique_together = ('person', 'product', 'order')
        constraints = [
            models.UniqueConstraint(fields=['person', 'product', 'order'], name='person_product_order'),
        ]


class Review(models.Model):
    mark = models.PositiveIntegerField(verbose_name='Оценка', )
    review = models.CharField(max_length=100, verbose_name='Отзыв', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Товар')
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Юзер')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.mark)



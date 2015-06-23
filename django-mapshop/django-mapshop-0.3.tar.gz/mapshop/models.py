# -*- coding: utf-8 -*-
from django.db import models
from image_cropping import ImageRatioField
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
import pytils
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save




class Kiosk(models.Model):
    u''' Класс Киоск содержит все данные о киоске (адрес, фото, мнемонику, широту, долготу) '''
    address = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='media')
    mnemonic = models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=200)
    scheduler = models.CharField(max_length=200, default='с 9 до 6 в будни')
    def __unicode__(self):
        return self.name

class Category(MPTTModel):
    ''' Класс категори товаров'''
    name = models.CharField(max_length=200)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    def get_absolute_url(self):
       return reverse("catalog_filter", kwargs={"slug": self.name_slug})
    def __unicode__(self):
        return self.name
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        return super(Category, self).save(**kwargs)


class Product(models.Model):
    u''' Класс Продукт содержит данные о товарах (имя, фото, цену, описание, наличие товара)'''
    __original_ammount = None

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.__original_ammount = self.ammount
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=u"Стоимость (руб)")
    description = models.CharField(max_length=200)
    ammount = models.PositiveSmallIntegerField(default=0) 
    rate = models.PositiveSmallIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    def get_absolute_url(self):
       return reverse("product_detail", kwargs={"slug": self.name_slug})
    @property
    def thumb(self):
        image = ProductImages.objects.get(is_main=True,product=self)
        thumbnail_url = get_thumbnailer(image.image).get_thumbnail({
            'size': (100, 100),
            'box': image.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)
    def __unicode__(self):
        return self.name
    def save(self, **kwargs):
        from mapshop.tasks import test_task
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        if self.ammount != self.__original_ammount and self.__original_ammount==0:
            test_task.delay(self)
            self.__original_ammount = self.ammount
        return super(Product, self).save(**kwargs)



class ProductImages(models.Model):
    from easy_thumbnails.files import get_thumbnailer
    u''' картинки товаров '''
    product = models.ForeignKey('Product')
    image  = models.ImageField(upload_to='product', verbose_name=u'Изображение')
    cropping = ImageRatioField('image', '430x360')
    is_main = models.BooleanField(default=False) 
    @property
    def thumb(self):
        #try:
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)
        #except:
        #    return 'no image'
    def save(self, **kwargs):
        if not self.id:
            if not ProductImages.objects.filter(product=self.product).exists():
                self.is_main = True
        return super(ProductImages, self).save(**kwargs)


   
class Client(models.Model):
    u''' Класс Клиент содержит данные о клиенте (емайл, телефон, параметр уведомления по емайлу, параметр уведомления по телефону)  '''
    surname = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Фамилия')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Имя')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'Телефон')
    add_phone = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'Дополнительный телефон')
    email = models.EmailField(verbose_name=u'Email')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'Дата рождения')
    notice_email = models.BooleanField(default=True, verbose_name=u'Email для уведомлений')
    notice_phone = models.BooleanField(default=True, verbose_name=u'Телефон для СМС уведомлений')
    created_at = models.DateTimeField(auto_now_add=True)
    is_organization = models.BooleanField(default='True', verbose_name=u'Организация?')
    name_org = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Наименование организации')
    address_org = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Юридический адрес организации')
    postal_index_org = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'Почтовый индекс')
    inn_org = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'ИНН')
    kpp_org = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'КПП')
    account_org = models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Р/с')
    bank_org = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'Банк')
    cor_account_org = models.CharField(max_length=16, null=True, blank=True, verbose_name=u'Корр. счет')
    bik_org = models.CharField(max_length=9, null=True, blank=True, verbose_name=u'БИК')
    user_id = models.IntegerField(default=0, null=True, blank=True, verbose_name=u'Пользователь')
    kiosk = models.ForeignKey('Kiosk', null=True, blank=True)
    def __unicode__(self):
        return self.name


class Order(models.Model):
    u''' заказы по клиенту '''
    STATUSES = (
        (u'Новый', u'Новый'),
        (u'Киоск выбран', u'Киоск выбран'),
        (u'Ожидает оплаты', u'Ожидает оплаты'),
        (u'Оплачен', u'Оплачен'),
        (u'Доставка', u'Доставка'),
        (u'Доставлен', u'Доставлен'),
        (u'Отказ', u'Отказ'),
    )
    status = models.CharField(verbose_name=u'Статус заказа',
                                    choices=STATUSES,
                                    default=u'Новый',
                                    max_length=20)
    client = models.ForeignKey('Client', null=True, blank=True) 
    kiosk = models.ForeignKey('Kiosk', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=250, null=True, blank=True)
    @property
    def total(self):
        t = 0
        for i in self.orderitem_set.all():
            t = t + (i.product.price*i.ammount)
        return t
    

class OrderItem(models.Model):
    u'''Элементы заказа'''
    order = models.ForeignKey('Order')
    product = models.ForeignKey('Product') 
    created_at = models.DateTimeField(auto_now_add=True)
    ammount = models.IntegerField(default=1)
    

class Preorder(models.Model):
    u'''Предзаказ содержит данные о предзаказах по клиентам'''
    TYPE = (
        ('phone', 'phone'),
        ('email', 'email'),
    )
    product = models.ForeignKey('Product')
    contact =  models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(verbose_name=u'Тип предзаказа',
                                    choices=TYPE,
                                    default='email',
                                    max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('product', 'contact', 'type')



def get_client_or_create(user):
    try:
        c = Client.objects.get(user_id=user.id)
    except:
        c = Client()
        c.name = user.username
        c.email = user.email
        c.user_id = user.id
        c.save()
    return c
    

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender = Order)
def manage_with_order(instance, **kwargs):
    print '---------------------------------------work with order %s' % instance.pk










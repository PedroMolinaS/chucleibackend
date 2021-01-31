from django.conf import settings
from django.contrib.auth.models import UserManager, AbstractUser, Group
from django.db import models


# from rest_framework.authtoken.models import Token


###############################################################
# Tablas de Usuarios:
class User(AbstractUser):
    username = models.CharField('Nombre de Usuario', max_length=30, unique=True)
    email = models.EmailField('E-Mail', max_length=200, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    photo = models.ImageField(upload_to='users/image', null=True, blank=True)
    cell = models.CharField(null=True, blank=True, max_length=15)
    city = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    name = models.CharField('Nombre', max_length=100, blank=True)
    is_active = models.BooleanField('Esta activo?', blank=True, default=True)
    is_staff = models.BooleanField('Es del Equipo?', blank=True, default=True)
    date_joined = models.DateTimeField('Fecha Registo', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.name or self.username

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(settings.MEDIA_URL, self.imagen)
        return '{}{}'.format(settings.STATIC_URL, 'img/sinimagen.png')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('date_joined',)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    age = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='usuarios/fotos', null=True, blank=True)

    def __str__(self):
        return str(self.user)


####################################################################
class CategoryMain(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    image = models.CharField(max_length=350, null=True, blank=True)
    # image = models.ImageField(upload_to='categorymain/img', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categoriesmain'
        ordering = ['pk']
        verbose_name_plural = 'CategoriesMain'


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            help_text='Unique value for product page URL, created from name.')
    image = models.CharField(max_length=350, blank=True, null=True)
    # image = models.ImageField(upload_to='category/img', blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField('Meta Description', max_length=255,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categoriesmain = models.ForeignKey(CategoryMain, on_delete=models.CASCADE, related_name='category')

    class Meta:
        db_table = 'categories'
        ordering = ['pk']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for Locales page URL, created from nombre.')
    address = models.CharField(max_length=255)
    shop_lat = models.DecimalField(max_digits=15, decimal_places=7, default=-12.5429900)
    shop_lon = models.DecimalField(max_digits=15, decimal_places=7, default=-74.6086300)
    description = models.TextField(blank=True, null=True)
    hour_sem = models.CharField(max_length=50, null=True, blank=True)
    hour_fsem = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'stores'
        ordering = ['pk']
        verbose_name_plural = 'Stores'


class Almacen(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for Almacen page URL, created from nombre.')
    # cantidadAlmacenamiento = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    almacen_lat = models.DecimalField(max_digits=15, decimal_places=7, default=-12.5429900)
    almacen_lon = models.DecimalField(max_digits=15, decimal_places=7, default=-74.6086300)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='almacenstore')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'almacenes'
        verbose_name_plural = 'Almacenes'


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            help_text='Unique value for product page URL, created from name.', null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    original_price = models.DecimalField(max_digits=9, decimal_places=2,
                                         blank=True, default=0.00, null=True)
    talla = models.CharField(max_length=50, blank=True, null=True)
    image = models.CharField(max_length=350, null=True, blank=True)
    # image = models.ImageField(upload_to='product/img', blank=True, null=True)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    recomendations = models.IntegerField(default=0)
    offer = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    meta_keywords = models.CharField(max_length=255,
                                     help_text='Comma-delimited set of SEO keywords for meta tag', blank=True,
                                     null=True)
    meta_description = models.CharField(max_length=255,
                                        help_text='Content for description meta tag', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='productstore', null=True, blank=True)

    # categoriesmain = models.ForeignKey(CategoryMain, on_delete=models.CASCADE, related_name='productcategorymain')

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Photos(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photosproduct')

    class Meta:
        db_table = 'photos'
        verbose_name_plural = 'Photos'
        ordering = ['pk']

    def __str__(self):
        return self.name


# class Customer(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     slug = models.SlugField(max_length=255, unique=True,
#                             help_text='Unique value for customer page URL, created from name.')
#     address = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True, help_text='True Moroso')
#     document = models.CharField(max_length=10, blank=True, null=True)
#     type_doc = models.CharField(max_length=5, blank=True, null=True)
#
#     class Meta:
#         db_table = 'customers'
#         ordering = ['pk']
#
#     def __str__(self):
#         return self.name


class Deliveryman(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,
                            help_text='Unique value for repartidor page URL, created from nombre.')
    cell = models.CharField(max_length=15, blank=True, null=True)
    is_activo = models.BooleanField(default=True)
    quantityday = models.IntegerField(default=0)

    class Meta:
        db_table = 'deliveryman'
        ordering = ['pk']

    def __str__(self):
        return self.name


class Zonapais(models.Model):
    departamento = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    distrito = models.CharField(max_length=50, blank=True, null=True)


    class Meta:
        db_table = 'zonapais'
        verbose_name_plural = 'Zonapais'
        ordering = ['departamento', 'provincia', 'distrito']

    def __str__(self):
        return self.departamento


class Order(models.Model):
    dateorder = models.DateField()
    state = models.CharField(max_length=20, default='pendiente')
    address = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, null=True, blank=True)
    delivery = models.BooleanField(default=False)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    order_lat = models.DecimalField(max_digits=15, decimal_places=7, default=-12.5429900)
    order_lon = models.DecimalField(max_digits=15, decimal_places=7, default=-74.6086300)
    datedelivery = models.DateField()

    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderuser')
    deliveryman = models.ForeignKey(Deliveryman, on_delete=models.CASCADE, related_name='orderdeliveryman')
    zonapais = models.ForeignKey(Zonapais, on_delete=models.CASCADE, related_name='orderzonapais')


    # store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orderstore')

    class Meta:
        db_table = 'order'
        # ordering = ['ordercod']
        ordering = ['pk']

    def __str__(self):
        # return self.ordercod
        return str(self.pk)


class Order_Detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='orderdetail')
    # ordercod = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='orderdetail')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True,
                                related_name='orderdetailproduct')
    quantity = models.IntegerField()
    image_product = models.CharField(max_length=255, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.CASCADE, related_name='orderdetailstore')

    class Meta:
        db_table = 'order_detail'
        ordering = ['pk']

    def __str__(self):
        return str(self.pk)

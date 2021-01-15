# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator, FileExtensionValidator

# Django REST Framework
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from .models import CategoryMain, Category, Product, Order, Order_Detail, Store, \
    Almacen, Deliveryman, Person, User, Photos


#################################################


# Datos para el Login:
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'pk']
        # fields = ['username', 'first_name', 'last_name', 'email']


# Valida login y obtiene/genera Token:
class UserLoginSerializer(serializers.Serializer):
    # campos a requerir:
    email = serializers.EmailField()
    password = serializers.CharField(min_length=3, max_length=64)

    # Primero validamos los datos:
    def validate(self, data):
        # recibe las credenciales:
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son validas')

        # Guardamos el usuario en el contexto para posteriormente recuperar el token
        self.context['user'] = user
        return data

    def create(self, data):
        # Genera o recupera token
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


# Alta de un usuario
class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    photo = serializers.ImageField(
        # validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        required=False, allow_null=True
    )
    city = serializers.CharField(max_length=100, required=False, allow_null=True)
    country = serializers.CharField(max_length=100, required=False, allow_null=True)

    cell_refex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Ejemplo: +999999999. El límite son de 15 dígitos'
    )
    cell = serializers.CharField(validators=[cell_refex], required=False, allow_null=True)
    # groups = serializers.IntegerField(allow_null=True)
    password = serializers.CharField(min_length=6, max_length=64)
    password_confirmation = serializers.CharField(min_length=6, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Las contraseñas no coinciden!!!')
        # password_validation.validate_password(passwd)

        image = None
        if 'photo' in data:
            image = data['photo']
        if image:
            if image.size > (512 * 1024):
                raise serializers.ValidationError(
                    f'Imagen demasiado grande, max 512KB, envió {round(image.size / 1024)}KB')
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        return user


###################################################

# Categoria Padre
class CategoryMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMain
        fields = ['pk', 'name', 'image', 'is_active']


# Categoria Hijo
class CategorySerializer(serializers.ModelSerializer):
    categories = serializers.IntegerField(source='pk')

    class Meta:
        model = Category
        fields = ['pk', 'name', 'categories']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'name', 'group']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['pk', 'name']


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PhotosBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):
    original = serializers.CharField(source='url')

    class Meta:
        model = Photos
        fields = ['pk', 'name', 'product', 'original']


class ProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name')
    store_hour_sem = serializers.CharField(source='store.hour_sem')
    store_hour_fsem = serializers.CharField(source='store.hour_fsem')
    store_address = serializers.CharField(source='store.address')
    photosproduct = PhotosSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['pk', 'name', 'slug', 'image', 'price', 'original_price', 'description', 'stock', 'is_active',
                  'recomendations', 'offer', 'store', 'store_name', 'store_hour_sem', 'store_hour_fsem',
                  'store_address', 'photosproduct']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# Detalle del pedido
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Detail
        fields = '__all__'


class OrderOrderDetailBaseSerializer(serializers.ModelSerializer):
    orderdetail = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['pk', 'dateorder', 'state', 'address', 'delivery', 'delivery_cost', 'total_cost', 'order_lat',
                  'order_lon', 'datedelivery', 'user', 'deliveryman', 'orderdetail']


# Detalle del pedido con valores agreados adicionales
class DetailOrderSerializer(serializers.ModelSerializer):
    name_product = serializers.CharField(source='product.name')
    image_product = serializers.CharField(source='product.image')
    description_prod = serializers.CharField(source='product.description')
    price_prod = serializers.DecimalField(source='product.price', max_digits=9, decimal_places=2)

    class Meta:
        model = Order_Detail
        fields = ['pk', 'product', 'name_product', 'image_product', 'quantity', 'discount', 'store', 'description_prod',
                  'price_prod']


# Orden y su detalle de pedido
class OrderOrderDetailSerializer(serializers.ModelSerializer):
    orderdetail = DetailOrderSerializer(many=True, read_only=True)
    name_user = serializers.CharField(source='user.name')
    email_user = serializers.CharField(source='user.email')
    name_deliveryman = serializers.CharField(source='deliveryman.name')

    # name_store = serializers.CharField(source='store.name')

    class Meta:
        model = Order
        fields = ['pk', 'email_user', 'dateorder', 'state', 'address', 'delivery', 'delivery_cost', 'total_cost',
                  'order_lat', 'order_lon', 'datedelivery', 'name_user', 'name_deliveryman',
                  'orderdetail']


class OrderDetailBasicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Detail
        fields = ['pk', 'order', 'product', 'quantity', 'discount', 'store']


class OrderDetailGraficosSerializer(serializers.ModelSerializer):
    product_price = serializers.DecimalField(source='product.price', max_digits=9, decimal_places=2)
    product_name = serializers.CharField(source='product.name')
    product_category = serializers.CharField(source='product.categories')

    class Meta:
        model = Order_Detail
        fields = ['pk', 'order', 'product', 'product_name', 'quantity', 'product_price', 'product_category']


class EmptySerializer(serializers.Serializer):
    pass


class CategoryProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['pk', 'name', 'slug', 'description', 'is_active', 'image', 'product']


class MainCategoryCategoryProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryMain
        fields = ['pk', 'name', 'slug', 'image', 'category']


class StoreProductosSerializer(serializers.ModelSerializer):
    productstore = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['pk', 'name', 'address', 'shop_lat', 'shop_lon', 'description', 'hour_sem', 'hour_fsem', 'is_active',
                  'productstore']

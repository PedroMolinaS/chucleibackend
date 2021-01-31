# Django REST Framework
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Max, Min, Sum, Count, Q
from django.forms.models import model_to_dict

import json

# Serializer
from .serializers import ProductSerializer, OrderOrderDetailSerializer, \
    CategoryProductSerializer, MainCategoryCategoryProductSerializer, UserLoginSerializer, UserModelSerializer, \
    UserSignUpSerializer, OrderDetailBasicoSerializer, OrderSerializer, OrderDetailSerializer, \
    EmptySerializer, OrderDetailGraficosSerializer, OrderOrderDetailBaseSerializer, StoreProductosSerializer, \
    DetailOrderSerializer, PhotosSerializer, CategorySerializer, StoreSerializer, ProductBaseSerializer, \
    PhotosBaseSerializer, ZonapaisSerializer

# Models
from .models import Category, Product, Order, Order_Detail, CategoryMain, Store, Deliveryman, User, Photos, Zonapais

from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render
from django.db.models import Q, Sum, Count
from django.db import connection
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout, authenticate, get_user_model

###############
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from . import serializers


# from .utils import get_and_authenticate_user


#############


def index(request):
    template_name = 'index.html'
    return render(request, template_name)


############################

# Servicios de login incluidos:

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    # Detail: define si es una petición de detalle o no, en nuestro caso solo permitiremos post
    @action(detail=False, methods=['post'])
    def login(self, request):
        # Usuario existente
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        # Usuario por darse de alta
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        request.user.auth_token.delete()
        # logout(request)
        data = {'success': 'Deslogueado exitosamente'}
        return Response(data=data, status=status.HTTP_200_OK)


#########################################################

# Metodo seguros
# ListApiView Se utiliza para puntos finales de solo lectura para representar
# una colección de instancias de modelo .Proporciona un get controlador de métodos.


class CategoryAllViewset(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class StoreAllViewset(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (AllowAny,)


# class CategoryCreateListViewset(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class ProductsAllViewset(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ProductsDetailPkViewset(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = (AllowAny,)


# class RegisterCustomer(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, format=None):
#         # Enviar por el Postman o por el front
#         post_name = request.data['name']
#         post_slug = request.data['slug']
#         post_address = request.data['address']
#         post_is_active = request.data['is_active']
#         post_document = request.data['document']
#         # ************************************************
#         # Orm de Django
#         customer = Customer()
#         customer.name = post_name
#         customer.slug = post_slug
#         customer.address = post_address
#         customer.is_active = post_is_active
#         customer.document = post_document
#
#         if len(customer.document) == 8 and customer.document[-1:] == '2':
#             data = {'detail': 'Customer save correct!!!!'}
#             customer.save()
#         else:
#             data = {'detail': 'Customer Invalid!!'}
#         reply = json.dumps(data)
#         return HttpResponse(reply, content_type='application/json')


# class CustomerAllViewset(generics.ListAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer
#     permission_classes = (AllowAny,)


class OrderOrderDetailViewset(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOrderDetailSerializer
    permission_classes = (AllowAny,)


# Servicios Incluidos:

@api_view(['GET'])
def productSearch(request, name):
    prod = Product.objects.filter(
        Q(name__icontains=name) | Q(price__icontains=name) | Q(stock__icontains=name)
    )
    serializer = ProductSerializer(prod, many=True)
    return Response(serializer.data)


class CategoryProductViewset(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    permission_classes = (AllowAny,)


class MainCategoryCategoryProductViewset(generics.ListAPIView):
    queryset = CategoryMain.objects.all()
    serializer_class = MainCategoryCategoryProductSerializer
    permission_classes = (AllowAny,)


class ZonapaisViewset(generics.ListAPIView):
    queryset = Zonapais.objects.all()
    serializer_class = ZonapaisSerializer
    permission_classes = (AllowAny,)


class ProductUpdatePkViewset(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


##########################################################
# CREAR PRODUCTOS Y DETALLES DE IMAGENES:
class ProductMultipleImageViewset(viewsets.ModelViewSet):
    serializer_class = PhotosSerializer
    queryset = Product.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        return PhotosSerializer

    def get_queryset(self):
        photos = Photos.objects.all()
        return photos

    def create(self, request, *args, **kwargs):
        product_data = request.data

        new_product = Product.objects.create(
            name=product_data['name'],
            slug=product_data['slug'],
            price=product_data['price'],
            original_price=product_data['original_price'],
            talla=product_data['talla'],
            image=product_data['image'],
            stock=product_data['stock'],
            brand=product_data['brand'],
            description=product_data['description'],
            is_active=product_data['is_active'],
            recomendations=product_data['recomendations'],
            offer=product_data['offer'],
            meta_keywords=product_data['meta_keywords'],
            meta_description=product_data['meta_description'],
            created_at=product_data['created_at'],
            updated_at=product_data['updated_at'],
            categories=Category.objects.get(pk=product_data['categories']),
            store=Store.objects.get(pk=product_data['store'])
        )
        new_product.save()

        new_productarreglo = product_data['photos']

        for detalle_obj in new_productarreglo:
            new_photos = Photos.objects.create(
                product=new_product,
                name=detalle_obj['name'],
                url=detalle_obj['url'])
            new_photos.save()

        serializer = PhotosSerializer(new_photos)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductCreateListViewset(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductBaseSerializer
    permission_classes = (AllowAny,)


class PhotosCreateListViewset(generics.ListCreateAPIView):
    queryset = Photos.objects.all()
    serializer_class = PhotosBaseSerializer
    permission_classes = (AllowAny,)


# Para crear pedidos (cabecera):
class OrderCreateListViewset(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)


# Para crear detalles de pedido:
class OrderDetailListViewset(generics.ListCreateAPIView):
    queryset = Order_Detail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (AllowAny,)


# Crear multiples detalles de un pedido creado:
class MultipleOrderDetailViewset(viewsets.ModelViewSet):
    serializer_class = OrderDetailBasicoSerializer

    def get_queryset(self):
        order_detail = Order_Detail.objects.all()
        return order_detail

    def create(self, request, *args, **kwargs):
        arreglodata = request.data

        for objdata in arreglodata:
            new_orderdetail = Order_Detail.objects.create(
                order=Order.objects.get(pk=objdata['order']),
                product=Product.objects.get(pk=objdata['product']),
                store=Store.objects.get(pk=objdata['store']),
                quantity=objdata['quantity'],
                discount=objdata['discount']
            )
            new_orderdetail.save()

        serializer = OrderDetailBasicoSerializer(new_orderdetail)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, *args, **kwargs):
    #     arreglodata = request.data
    #     arreglo_actualizado = []
    #     for objdata in arreglodata:
    #         if "pk" in objdata.keys():
    #             new_orderdetail = Order_Detail.objects.filter(pk=objdata["pk"]).exists()
    #             c = new_orderdetail.get(pk=objdata["pk"])
    #             c.quantity = objdata.get('quantity', c.quantity)
    #             c.discount = objdata.get('discount', c.discount)
    #             c.save()
    #             arreglo_actualizado.append(c.pk)
    #         else:
    #             # aqui puedo utilizar el codigo de CREATE
    #             c = Order_Detail.objects.create(**objdata, question=question)
    #             arreglo_actualizado.append(c.pk)


class OrderMultipleOrderDetailViewset(viewsets.ModelViewSet):
    serializer_class = OrderDetailBasicoSerializer
    queryset = Order.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        return OrderDetailBasicoSerializer

    def get_queryset(self):
        order_detail = Order_Detail.objects.all()
        return order_detail

    def create(self, request, *args, **kwargs):
        order_data = request.data

        # new_order = Order_Detail.objects.create(ordercod=Order.objects.get(pk=order_data["ordercod"]),
        #                                        product=Product.objects.get(pk=order_data["product"]),
        #                                        quantity=order_data["quantity"], discount=order_data["discount"])
        # new_order.save()
        # serializer = DetailOrderSerializer2(new_order)
        # return Response(serializer.data)

        new_order = Order.objects.create(
            dateorder=order_data['dateorder'],
            state=order_data['state'],
            address=order_data['address'],
            reference=order_data['reference'],
            delivery=order_data['delivery'],
            delivery_cost=order_data['delivery_cost'],
            total_cost=order_data['total_cost'],
            order_lat=order_data['order_lat'],
            order_lon=order_data['order_lon'],
            datedelivery=order_data['datedelivery'],
            user=User.objects.get(pk=order_data['user']),
            deliveryman=Deliveryman.objects.get(pk=order_data['deliveryman']),
            zonapais=Zonapais.objects.get(pk=order_data['zonapais'])
        )
        new_order.save()

        new_orderarreglo = order_data['orderdetail']
        # print(new_orderarreglo)

        for detalle_obj in new_orderarreglo:
            # print(detalle_obj)
            new_orderdetail = Order_Detail.objects.create(
                order=new_order,
                product=Product.objects.get(pk=detalle_obj['product']),
                store=Store.objects.get(pk=detalle_obj['store']),
                quantity=detalle_obj['quantity'],
                discount=detalle_obj['discount'])
            new_orderdetail.save()

        serializer = OrderDetailBasicoSerializer(new_orderdetail)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, instance, validated_data):
    #     orderdetail = validated_data.pop('orderdetail')
    #     instance.dateorder = validated_data.get("dateorder", instance.dateorder)
    #     instance.state = validated_data.get("state", instance.state)
    #     instance.delivery = validated_data.get("delivery", instance.delivery)
    #     instance.delivery_cost = validated_data.get("delivery_cost", instance.delivery_cost)
    #     instance.total_cost = validated_data.get("total_cost", instance.total_cost)
    #     instance.order_lat = validated_data.get("order_lat", instance.order_lat)
    #     instance.order_lon = validated_data.get("order_lon", instance.order_lon)
    #     instance.datedelivery = validated_data.get("datedelivery", instance.datedelivery)
    #     instance.user = validated_data.get("user", instance.user)
    #     instance.deliveryman = validated_data.get("deliveryman", instance.deliveryman)
    #     instance.store = validated_data.get("store", instance.store)
    #     instance.save()
    #
    #     keep_orderdetail = []
    #     existing_pk = [c.pk for c in instance.orderdetail]
    #     for orderd in orderdetail:
    #         if "id" in orderd.keys():
    #             if Order_Detail.objects.filter(pk=orderd["pk"]).exists():
    #                 c = Order_Detail.objects.get(id=orderd["pk"])
    #                 c.dateorder = orderd.get('dateorder', c.dateorder)
    #                 c.state = orderd.get('state', c.state)
    #                 c.delivery = orderd.get('delivery', c.delivery)
    #                 c.delivery_cost = orderd.get('delivery_cost', c.delivery_cost)
    #                 c.total_cost = orderd.get('total_cost', c.total_cost)
    #                 c.order_lat = orderd.get('order_lat', c.order_lat)
    #                 c.order_lon = orderd.get('order_lon', c.order_lon)
    #                 c.datedelivery = orderd.get('datedelivery', c.datedelivery)
    #                 c.user = orderd.get('user', c.user)
    #                 c.deliveryman = orderd.get('deliveryman', c.deliveryman)
    #                 c.store = orderd.get('store', c.store)
    #                 c.save()
    #                 keep_orderdetail.append(c.pk)
    #             else:
    #                 continue
    #         else:
    #             c = Order_Detail.objects.create(**orderd, question=instance)
    #             keep_orderdetail.append(c.pk)
    #
    #     for orderd in instance.orderdetail:
    #         if orderd.pk not in keep_orderdetail:
    #             orderd.delete()
    #
    #     return instance


# Para actualizar pedidos (cabecera):
class OrderUpdateViewset(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'
    permission_classes = (AllowAny,)


# Para actualizar detalles de pedido:
class OrderDetailUpdateViewset(generics.UpdateAPIView):
    queryset = Order_Detail.objects.all()
    serializer_class = OrderDetailSerializer
    lookup_field = 'pk'
    permission_classes = (AllowAny,)


class OrderOrderDetailBaseViewset(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderOrderDetailBaseSerializer
    lookup_field = 'user'
    permission_classes = (AllowAny,)


class StoreProductosViewset(generics.ListAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreProductosSerializer


@api_view(['GET'])
def pedidosproductSearch(request, user):
    usu = Order.objects.filter(user=user)
    serializer = OrderOrderDetailBaseSerializer(usu, many=True)
    return Response(serializer.data)


def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class ApiTotalProductosXCategoria(APIView):
    def get(self, request, format=None):
        restot = Category.objects.annotate(Count('product'))
        restot2 = restot.values_list('name', 'product__count')
        list_product = []
        for res in restot2:
            new_res = {
                'category_name': res[0],
                'cant_products': res[1]
            }
            print(res)
            print(json.dumps(res))
            list_product.append(new_res)
        dump = list_product
        reply = json.dumps(dump)
        return HttpResponse(reply, content_type='application/json')


class ApiTotalPedidosXProducto(APIView):
    def get(self, request, format=None):
        restot1 = Product.objects.annotate(Count('orderdetailproduct'))
        restot2 = restot1.values_list('pk', 'name', 'orderdetailproduct__count')

        list_product = []
        for pro in restot2:
            print(pro)
            print(json.dumps(pro))
            new_pro = {
                'producto_pk': pro[0],
                'producto_name': pro[1],
                'cant_ped': pro[2]
            }
            print(new_pro)
            list_product.append(new_pro)
        dump = list_product
        reply = json.dumps(dump)
        return HttpResponse(reply, content_type='application/json')


class ApiTotalPedidosXUsuario(APIView):
    def get(self, request, format=None):
        restot1 = User.objects.annotate(Count('orderuser'))
        restot2 = restot1.values_list('username', 'orderuser__count')

        list_product = []
        for usu in restot2:
            print(usu)
            print(json.dumps(usu))
            new_usu = {
                'usu_name': usu[0],
                'cant_ped': usu[1]
            }
            print(new_usu)
            list_product.append(new_usu)
        dump = list_product
        reply = json.dumps(dump)
        return HttpResponse(reply, content_type='application/json')


class ApiTotalPedidosXDelivery(APIView):
    def get(self, request, format=None):
        restot1 = Deliveryman.objects.annotate(Count('orderdeliveryman'))
        print(restot1)
        restot2 = restot1.values_list('name', 'orderdeliveryman__count')

        list_product = []
        for deliv in restot2:
            new_deliv = {
                'delivery_name': deliv[0],
                'cant_ped': deliv[1]
            }
            list_product.append(new_deliv)
        dump = list_product
        reply = json.dumps(dump)
        return HttpResponse(reply, content_type='application/json')


def pdf_view(request):
    try:
        return FileResponse(open('DocumentoFuncional.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

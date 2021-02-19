# Django
from django.urls import path, include

from . import views
from .views import index, UserViewSet, OrderMultipleOrderDetailViewset, MultipleOrderDetailViewset, Logout, AuthViewSet, \
    ProductMultipleImageViewset

# Para Crear un Api Restfull
##########################################################
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register('orders', OrderMultipleOrderDetailViewset, basename='orders')
router.register('products', ProductMultipleImageViewset, basename='products')
router.register('order_detail', MultipleOrderDetailViewset, basename='order_detail')
router.register('autentica', AuthViewSet, basename='autentica')

# router.register('full_products', views.ProductFullViewset)
# router.register('full_categories', views.CategoryFullViewset)
###########################################################

urlpatterns = [
    # path('', index, name='index'),
    # path('List_All_Categories/', views.CategoryAllViewset.as_view()),  # http://127.0.0.1:8000/List_All_Categories/
    # path('Create_List_Categories/', views.CategoryCreateListViewset.as_view()),
    # path('Delete_Categories/<pk>/', views.CategoryDeletePkViewset.as_view()),
    # path('Update_Categories/<pk>/', views.CategoryUpdatePkViewset.as_view()),
    # path('Detail_Categories/<slug>/', views.CategoryDetailPkViewset.as_view()),
    # path('Create_Customer/', views.RegisterCustomer.as_view()),
    # path('List_All_Customers/', views.CustomerAllViewset.as_view()),
    # path('Detail_Products/<slug>/', views.ProductsDetailPkViewset.as_view()),

    # SERVICIOS CREADOS YA UTILIZADOS EN EL FRONT::::::
    path('List_Category_Products/', views.CategoryProductViewset.as_view()),
    path('List_Category_Products/v2/', views.CategoryProductViewsetV2.as_view()),
    path('List_MainCategoryCategory_Products/', views.MainCategoryCategoryProductViewset.as_view()),
    path('List_MainCategoryCategory_Products/v2/', views.MainCategoryCategoryProductViewsetV2.as_view()),
    path('List_All_Products/', views.ProductsAllViewset.as_view()),
    path('List_All_Categories/', views.CategoryAllViewset.as_view()),
    path('List_All_Store/', views.StoreAllViewset.as_view()),
    path('List_All_Zonapais/', views.ZonapaisViewset.as_view()),
    path('List_Product_search/<name>/', views.productSearch, name='List_Product_search'),
    path('List_Order_OrderDetail/', views.OrderOrderDetailViewset.as_view()),
    path('Create_List_Product/', views.ProductCreateListViewset.as_view()),
    path('Create_List_Photos/', views.PhotosCreateListViewset.as_view()),
    path('Create_List_Order/', views.OrderCreateListViewset.as_view()),
    path('Create_List_OrderDetail/', views.OrderDetailListViewset.as_view()),
    path('Update_Order/<pk>/', views.OrderUpdateViewset.as_view()),
    path('Update_OrderDetail/<pk>/', views.OrderDetailUpdateViewset.as_view()),
    path('pedidos_cliente/<user>/', views.pedidosproductSearch, name='pedidos_cliente'),
    path('ApiTotalPedidosXProducto/', views.ApiTotalPedidosXProducto.as_view()),
    path('ApiTotalPedidosXUsuario/', views.ApiTotalPedidosXUsuario.as_view()),

    path('logout/', Logout.as_view()),
    path('tienda_productos/', views.StoreProductosViewset.as_view()),
    path('ApiTotalPedidosXCategoria/', views.ApiTotalProductosXCategoria.as_view()),
    path('ApiTotalPedidosXDelivery/', views.ApiTotalPedidosXDelivery.as_view()),

    path('api/', include(router.urls)),  # http://127.0.0.1:8000/api/users/signup/
    # http://127.0.0.1:8000/api/users/login/

    path('', views.pdf_view),

]

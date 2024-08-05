from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'productos', views.ProductoViewSet)
router.register(r'bodegas', views.BodegaViewSet)
router.register(r'inventarios', views.InventarioViewSet)
router.register(r'facturas', views.FacturaViewSet)
router.register(r'ventas', views.VentaViewSet)
router.register(r'detalleventa', views.DetalleventaViewset)




urlpatterns = [
    path('', include(router.urls))  
]

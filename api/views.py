from rest_framework import viewsets
from .models import Categoria, Producto, Bodega, Inventario, Venta, DetalleVenta, Factura
from .serializers import CategoriaSerializer, ProductoSerializer, BodegaSerializer, InventarioSerializer, VentaSerializer, FacturaSerializer, DetalleVentaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetalleventaViewset(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        venta_id = self.request.query_params.get('venta_id')
        if venta_id:
            queryset = queryset.filter(venta_id=venta_id)
        return queryset

class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


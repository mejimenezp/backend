from django.test import TestCase
from .models import Categoria, Producto, Bodega, Inventario, Venta, DetalleVenta, Factura

class ModelosTest(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.producto = Producto.objects.create(nombre="portatil", descripcion="portatil de alta gama", precio=1500, categoria=self.categoria)
        self.bodega = Bodega.objects.create(nombre="Bodega Central", ubicacion="calle 166")
        self.inventario = Inventario.objects.create(producto=self.producto, cantidad=10, bodega=self.bodega)
        self.venta = Venta.objects.create()
        self.detalle_venta = DetalleVenta.objects.create(venta=self.venta, producto=self.producto, cantidad=2)

    def test_categoria_creation(self):
        self.assertEqual(self.categoria.nombre, "Electrónica")

    def test_producto_creation(self):
        self.assertEqual(self.producto.nombre, "portatil")
        self.assertEqual(self.producto.descripcion, "portatil de alta gama")
        self.assertEqual(self.producto.precio, 1500)
        self.assertEqual(self.producto.categoria, self.categoria)

    def test_bodega_creation(self):
        self.assertEqual(self.bodega.nombre, "Bodega Central")
        self.assertEqual(self.bodega.ubicacion, "calle 166")

    def test_inventario_creation(self):
        self.assertEqual(self.inventario.producto, self.producto)
        self.assertEqual(self.inventario.cantidad, 10)
        self.assertEqual(self.inventario.bodega, self.bodega)

    def test_venta_creation(self):
        self.assertEqual(self.venta.total, 3000)

    def test_detalle_venta_creation(self):
        self.assertEqual(self.detalle_venta.producto, self.producto)
        self.assertEqual(self.detalle_venta.cantidad, 2)
        self.assertEqual(self.detalle_venta.precio_unitario, 1500)
        self.assertEqual(self.detalle_venta.subtotal, 3000)

    def test_venta_total_calculation(self):
        detalle_venta2 = DetalleVenta.objects.create(venta=self.venta, producto=self.producto, cantidad=1)
        self.venta.calcular_total()
        self.assertEqual(self.venta.total, 4500)

    def test_factura_creation(self):
        factura = Factura.objects.create(venta=self.venta)
        self.assertEqual(factura.total, self.venta.total)

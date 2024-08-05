from django.db import models
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        if not self.nombre:
            raise ValidationError('El nombre de la categoría no puede estar vacío.')

class Producto(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def clean(self):
        if not self.nombre:
            raise ValidationError('El nombre del producto no puede estar vacío.')
        if self.precio <= 0:
            raise ValidationError('El precio debe ser mayor que cero.')
        if not self.categoria:
            raise ValidationError('El producto debe tener una categoría asociada.')

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.TextField()

    def clean(self):
        if not self.nombre:
            raise ValidationError('El nombre de la bodega no puede estar vacío.')
        if not self.ubicacion:
            raise ValidationError('La ubicación de la bodega no puede estar vacía.')

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'bodega')

    def clean(self):
        if self.cantidad < 0:
            raise ValidationError('La cantidad en el inventario no puede ser negativa.')
        if not self.producto:
            raise ValidationError('El inventario debe estar asociado a un producto.')
        if not self.bodega:
            raise ValidationError('El inventario debe estar asociado a una bodega.')

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalleventa_set.all())
        self.total = total
        self.save()

    def clean(self):
        if self.total < 0:
            raise ValidationError('El total de la venta no puede ser negativo.')

    def __str__(self):
        return f'Venta {self.id}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalleventa_set', null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.precio_unitario = self.producto.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.calcular_total()

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor que cero.')
        if self.precio_unitario <= 0:
            raise ValidationError('El precio unitario debe ser mayor que cero.')
        if self.subtotal != self.cantidad * self.precio_unitario:
            raise ValidationError('El subtotal no es correcto.')

    def __str__(self):
        return f'Detalle de venta {self.id}'

class Factura(models.Model):
    venta = models.OneToOneField(Venta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.venta.total
        super().save(*args, **kwargs)

    def clean(self):
        if self.total < 0:
            raise ValidationError('El total de la factura no puede ser negativo.')

    def __str__(self):
        return f'Factura {self.id}'

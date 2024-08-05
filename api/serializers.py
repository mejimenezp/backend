from rest_framework import serializers
from .models import Categoria, Producto, Bodega, Inventario, Venta, DetalleVenta, Factura

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'categoria', 'categoria_nombre']

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    bodega_nombre = serializers.CharField(source='bodega.nombre', read_only=True)
    
    class Meta:
        model = Inventario
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'bodega', 'bodega_nombre']

        

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, source='producto.precio', read_only=True)
    
    
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal', 'venta_id']

class VentaSerializer(serializers.ModelSerializer):
    detalleventa_set = DetalleVentaSerializer(many=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'detalleventa_set', 'total']
    
    def get_total(self, obj):
        total = sum(detalle.subtotal for detalle in obj.detalleventa_set.all())
        return total
    
    def create(self, validated_data):
        detalle_venta_data = validated_data.pop('detalleventa_set')
        venta = Venta.objects.create(**validated_data)
        for detalle_data in detalle_venta_data:
            producto = detalle_data.get('producto')
            if not producto:
                raise serializers.ValidationError({'message': 'El producto es obligatorio en los detalles de venta.'})
            
            detalle_venta = DetalleVenta.objects.create(venta=venta, **detalle_data)
            
            try:
                inventario = Inventario.objects.get(producto=detalle_venta.producto)
            except Inventario.DoesNotExist:
                raise serializers.ValidationError({'message': f"No se encontró inventario para el producto {detalle_venta.producto.nombre}"})

            if inventario.cantidad >= detalle_venta.cantidad:
                inventario.cantidad -= detalle_venta.cantidad
                inventario.save()
            else:
                raise serializers.ValidationError({'message': f"No hay suficiente inventario para el producto {detalle_venta.producto.nombre}"})

        venta.calcular_total()
        
        
        Factura.objects.create(venta=venta, total=venta.total)
        
        return venta

class FacturaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer()
    
    class Meta:
        model = Factura
        fields = ['id', 'venta', 'fecha', 'total']

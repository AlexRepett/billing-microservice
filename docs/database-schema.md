# Esquema de Base de Datos - Sistema de Facturación

**Proyecto:** Microservicio de Facturación  
**Versión:** 1.0 - Fase 2  
**Última actualización:** Febrero 2026  
**Autor:** Alexis Repetto

---

## 📊 Diagrama Entidad-Relación

```
┌─────────────┐         ┌──────────────┐         ┌─────────────────┐
│   Cliente   │         │   Factura    │         │ FacturaDetalle  │
├─────────────┤         ├──────────────┤         ├─────────────────┤
│ id (PK)     │◄──────┐ │ id (PK)      │◄──────┐ │ id (PK)         │
│ rfc         │       │ │ folio        │       │ │ factura (FK)    │
│ razon_social│       └─│ cliente (FK) │       └─│ producto (FK)   │
│ email       │         │ fecha_emision│         │ cantidad        │
│ telefono    │         │ fecha_venci. │         │ precio_unitario │
│ direccion   │         │ subtotal     │         │ subtotal (calc) │
│ ...         │         │ iva          │         └─────────────────┘
└─────────────┘         │ total        │                   ▲
                        │ estatus      │                   │
                        │ notas        │                   │
                        └──────────────┘                   │
                                                           │
                        ┌──────────────┐                   │
                        │   Producto   │───────────────────┘
                        ├──────────────┤
                        │ id (PK)      │
                        │ codigo       │
                        │ nombre       │
                        │ descripcion  │
                        │ precio_unit. │
                        │ unidad_medida│
                        │ iva_aplica   │
                        └──────────────┘
```

---

## 🔗 Descripción de Relaciones

### Relaciones One-to-Many (1:N)

1. **Cliente → Factura**
   - **Tipo:** One-to-Many
   - **Descripción:** Un cliente puede tener múltiples facturas
   - **Implementación:** `ForeignKey` en modelo Factura hacia Cliente
   - **Cascada:** `on_delete=models.PROTECT` (no permitir borrar cliente con facturas)

2. **Factura → FacturaDetalle**
   - **Tipo:** One-to-Many
   - **Descripción:** Una factura puede tener múltiples líneas de detalle (productos/servicios)
   - **Implementación:** `ForeignKey` en modelo FacturaDetalle hacia Factura
   - **Cascada:** `on_delete=models.CASCADE` (si se borra factura, borrar detalles)

3. **Producto → FacturaDetalle**
   - **Tipo:** One-to-Many
   - **Descripción:** Un producto puede aparecer en múltiples facturas
   - **Implementación:** `ForeignKey` en modelo FacturaDetalle hacia Producto
   - **Cascada:** `on_delete=models.PROTECT` (no permitir borrar producto usado en facturas)

---

## 📋 Definición de Modelos

### 1. Cliente

**Propósito:** Almacenar información de los clientes/receptores de facturas. Representa a las personas físicas o morales que reciben facturación.

**Ubicación:** `src/billing/models.py` → `class Cliente(models.Model)`

| Campo | Tipo Django | Restricciones | Descripción |
|-------|-------------|---------------|-------------|
| `id` | AutoField | PK, auto_increment | Identificador único (generado automáticamente) |
| `rfc` | CharField | max_length=13, unique, db_index | RFC del cliente (12 o 13 caracteres) |
| `razon_social` | CharField | max_length=255 | Nombre legal del cliente o razón social |
| `email` | EmailField | max_length=255 | Correo electrónico de contacto |
| `telefono` | CharField | max_length=20, blank=True | Teléfono de contacto |
| `direccion` | TextField | blank=True | Dirección completa (calle, número, colonia) |
| `codigo_postal` | CharField | max_length=10, blank=True | Código postal |
| `ciudad` | CharField | max_length=100, blank=True | Ciudad |
| `estado` | CharField | max_length=100, blank=True | Estado/Provincia |
| `pais` | CharField | max_length=100, default='México' | País |
| `fecha_registro` | DateTimeField | auto_now_add | Fecha de alta en el sistema |
| `activo` | BooleanField | default=True | Indica si el cliente está activo |

**Índices adicionales:**
- `rfc` (unique index automático)
- `razon_social` (considerar index para búsquedas)

**Validaciones custom:**
- Validar formato de RFC mexicano (12 caracteres persona moral, 13 persona física)
- Validar que email sea válido

**Métodos:**
- `__str__()`: Retornar razón social
- `get_absolute_url()`: URL del detalle del cliente
- `get_facturas_activas()`: Retornar facturas no canceladas

---

### 2. Producto

**Propósito:** Catálogo de productos y servicios que se pueden facturar. Representa los conceptos que aparecen como líneas en las facturas.

**Ubicación:** `src/billing/models.py` → `class Producto(models.Model)`

| Campo | Tipo Django | Restricciones | Descripción |
|-------|-------------|---------------|-------------|
| `id` | AutoField | PK, auto_increment | Identificador único |
| `codigo` | CharField | max_length=50, unique, db_index | Código interno del producto/servicio |
| `nombre` | CharField | max_length=255 | Nombre del producto/servicio |
| `descripcion` | TextField | blank=True | Descripción detallada |
| `precio_unitario` | DecimalField | max_digits=10, decimal_places=2 | Precio por unidad (antes de IVA) |
| `unidad_medida` | CharField | max_length=20, choices=UNIDADES | Unidad de medida (pieza, servicio, hora, kg, etc.) |
| `iva_aplica` | BooleanField | default=True | Indica si aplica IVA (16% en México) |
| `activo` | BooleanField | default=True | Indica si el producto está activo para facturar |
| `fecha_creacion` | DateTimeField | auto_now_add | Fecha de creación |
| `fecha_actualizacion` | DateTimeField | auto_now | Última actualización |

**Choices de unidad_medida:**
```python
UNIDADES = [
    ('pieza', 'Pieza'),
    ('servicio', 'Servicio'),
    ('hora', 'Hora'),
    ('kg', 'Kilogramo'),
    ('litro', 'Litro'),
    ('metro', 'Metro'),
    ('paquete', 'Paquete'),
]
```

**Métodos:**
- `__str__()`: Retornar nombre del producto
- `get_precio_con_iva()`: Calcular precio con IVA si aplica
- `get_absolute_url()`: URL del detalle del producto

---

### 3. Factura

**Propósito:** Documento fiscal que representa la transacción. Cabecera de la factura con información general y totales.

**Ubicación:** `src/billing/models.py` → `class Factura(models.Model)`

| Campo | Tipo Django | Restricciones | Descripción |
|-------|-------------|---------------|-------------|
| `id` | AutoField | PK, auto_increment | Identificador único |
| `folio` | CharField | max_length=20, unique, db_index | Folio de la factura (auto-generado) |
| `cliente` | ForeignKey | to=Cliente, on_delete=PROTECT, related_name='facturas' | Cliente receptor de la factura |
| `fecha_emision` | DateTimeField | auto_now_add | Fecha de emisión |
| `fecha_vencimiento` | DateField | null=True, blank=True | Fecha de vencimiento (opcional) |
| `subtotal` | DecimalField | max_digits=10, decimal_places=2, default=0 | Subtotal (suma de líneas sin IVA) |
| `iva` | DecimalField | max_digits=10, decimal_places=2, default=0 | Total de IVA |
| `total` | DecimalField | max_digits=10, decimal_places=2, default=0 | Total a pagar (subtotal + iva) |
| `estatus` | CharField | max_length=20, choices=ESTATUS, default='BORRADOR' | Estado de la factura |
| `notas` | TextField | blank=True | Notas adicionales |
| `fecha_creacion` | DateTimeField | auto_now_add | Fecha de creación del registro |
| `fecha_actualizacion` | DateTimeField | auto_now | Última actualización |

**Choices de estatus:**
```python
ESTATUS = [
    ('BORRADOR', 'Borrador'),
    ('EMITIDA', 'Emitida'),
    ('PAGADA', 'Pagada'),
    ('CANCELADA', 'Cancelada'),
]
```

**Índices adicionales:**
- `folio` (unique index automático)
- `fecha_emision` (index para consultas por fecha)
- `estatus` (index para filtros)

**Métodos:**
- `__str__()`: Retornar folio
- `generar_folio()`: Generar folio único (ej: FAC-2026-00001)
- `calcular_totales()`: Recalcular subtotal, iva, total desde detalles
- `emitir()`: Cambiar estatus a EMITIDA
- `cancelar()`: Cambiar estatus a CANCELADA
- `get_absolute_url()`: URL del detalle de la factura
- `puede_editarse()`: Retornar True si está en BORRADOR

**Properties (campos calculados):**
- `dias_vencimiento`: Días transcurridos desde emisión hasta vencimiento

---

### 4. FacturaDetalle

**Propósito:** Líneas individuales de la factura. Representa cada producto/servicio facturado con su cantidad y precio.

**Ubicación:** `src/billing/models.py` → `class FacturaDetalle(models.Model)`

| Campo | Tipo Django | Restricciones | Descripción |
|-------|-------------|---------------|-------------|
| `id` | AutoField | PK, auto_increment | Identificador único |
| `factura` | ForeignKey | to=Factura, on_delete=CASCADE, related_name='detalles' | Factura a la que pertenece |
| `producto` | ForeignKey | to=Producto, on_delete=PROTECT, related_name='factura_detalles' | Producto facturado |
| `cantidad` | DecimalField | max_digits=10, decimal_places=2 | Cantidad de unidades |
| `precio_unitario` | DecimalField | max_digits=10, decimal_places=2 | Precio unitario al momento de facturar |
| `orden` | PositiveIntegerField | default=0 | Orden de aparición en la factura |

**Nota sobre precio_unitario:** Se guarda el precio al momento de la factura (no se usa el precio actual del producto), para mantener histórico correcto aunque el precio del producto cambie después.

**Métodos:**
- `__str__()`: Retornar "{cantidad} x {producto}"
- `get_subtotal()`: Calcular cantidad * precio_unitario

**Properties (campos calculados):**
- `subtotal`: Property que retorna cantidad * precio_unitario
- `iva_monto`: Calcular IVA si el producto lo aplica
- `total_linea`: Subtotal + IVA

**Meta options:**
```python
class Meta:
    ordering = ['orden', 'id']
    verbose_name = 'Detalle de Factura'
    verbose_name_plural = 'Detalles de Factura'
```

---

## 🔐 Consideraciones de Seguridad

1. **Protección de eliminación:**
   - Clientes con facturas NO pueden eliminarse (PROTECT)
   - Productos usados en facturas NO pueden eliminarse (PROTECT)
   - Si se elimina una factura, sus detalles se eliminan automáticamente (CASCADE)

2. **Auditoría:**
   - Todos los modelos tienen campos `fecha_creacion` / `fecha_actualizacion`
   - El campo `activo` permite "borrado suave" en lugar de eliminación física

3. **Validación:**
   - RFC único por cliente
   - Folios únicos por factura
   - Códigos únicos por producto

---

## 📊 Consideraciones de Performance

1. **Índices de búsqueda:**
   - `Cliente.rfc` (búsquedas frecuentes)
   - `Factura.folio` (búsquedas por folio)
   - `Factura.fecha_emision` (filtros por fecha)
   - `Producto.codigo` (búsquedas de productos)

2. **Queries optimizados:**
   - Usar `select_related('cliente')` al listar facturas
   - Usar `prefetch_related('detalles__producto')` al ver detalle de factura

3. **Campos calculados:**
   - `subtotal`, `iva`, `total` en Factura son **denormalizados** (se guardan calculados)
   - Esto evita calcular en cada consulta, pero requiere recalcular con signals

---

## 🧪 Datos de Prueba Sugeridos

Una vez creados los modelos, cargar:

1. **3-5 Clientes de prueba**
   - Cliente persona física
   - Cliente persona moral
   - Cliente extranjero

2. **10-15 Productos/Servicios**
   - Productos físicos (con IVA)
   - Servicios profesionales (con IVA)
   - Productos exentos de IVA

3. **5-10 Facturas de prueba**
   - Facturas en diferentes estatus
   - Facturas con múltiples líneas
   - Facturas de un solo producto

---

## 📝 Próximos Pasos

1. ✅ **Fase 1 (Hoy - Martes):** Implementar modelo Cliente
2. ✅ **Fase 2 (Miércoles):** Implementar modelo Producto
3. ✅ **Fase 3 (Jueves):** Implementar modelo Factura
4. ✅ **Fase 4 (Viernes):** Implementar modelo FacturaDetalle + migraciones

---

## 🔄 Control de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Feb 2026 | Diseño inicial - Fase 2 |

---

**Notas técnicas:**
- Base de datos: PostgreSQL 12+
- ORM: Django 4.2.28
- Encoding: UTF-8
- Timezone: America/Mexico_City

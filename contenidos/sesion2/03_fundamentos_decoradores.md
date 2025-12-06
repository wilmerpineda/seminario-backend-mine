# 2.3 Controlando el Flujo de Datos con Decoradores

En el mundo de la Inteligencia de Negocios, a menudo lidiamos con datos que necesitan ser calculados, validados o transformados antes de ser útiles. Python nos ofrece una herramienta poderosa llamada decoradores (esas etiquetas que empiezan con `@`) para añadir "superpoderes" a nuestros métodos.

En este capítulo, desmitificaremos los tres más importantes para un Ingeniero de Datos o Analista BI: `@property`, `@staticmethod` y `@classmethod`.

## 1. `@property`: Campos Calculados "En Vivo"

### ¿El Problema?

Imaginen que tienen una clase Venta. Si calculan la ganancia en el ``__init__``, ese valor se queda "congelado" en el tiempo. Si luego actualizan el costo o el precio, la ganancia **no** se actualiza automáticamente, generando inconsistencias graves en los reportes.

### La Solución

El decorador `@property` nos permite definir un método, pero acceder a él como si fuera un atributo (sin usar paréntesis ()). Es como tener una celda de Excel con una fórmula: siempre muestra el valor actualizado.

Ideal para: Márgenes, ROAS, Conversiones, KPIs derivados.

```
class ProductoAnalitico:
    def __init__(self, costo_unitario, precio_venta):
        self.costo = costo_unitario
        self.precio = precio_venta
        self._descuento = 0.0 # Variable "protegida" (convención interna)

    # CASO DE USO 1: CÁLCULO DINÁMICO
    # Al poner @property, convertimos la función en un atributo de solo lectura.
    @property
    def margen_ganancia(self):
        # Esta lógica se ejecuta CADA VEZ que alguien escribe 'objeto.margen_ganancia'
        precio_final = self.precio * (1 - self._descuento)
        return precio_final - self.costo

    # CASO DE USO 2: VALIDACIÓN DE DATOS (Governance)
    # Primero definimos la propiedad de lectura
    @property
    def descuento(self):
        return self._descuento

    # Luego definimos el "setter": Qué pasa cuando alguien intenta asignar un valor
    @descuento.setter
    def descuento(self, valor):
        # Aquí imponemos la REGLA DE NEGOCIO
        if valor > 0.5: 
            print("⚠️ ALERTA DE COMPLIANCE: Descuento > 50% rechazado por política.")
            return 
        if valor < 0:
            print("⚠️ ERROR: El descuento no puede ser negativo.")
            return
        
        # Si pasa las reglas, guardamos el dato
        self._descuento = valor

```

### ¿Cómo se usa en la práctica?

```
prod = ProductoAnalitico(costo=50, precio_venta=100)

# 1. Lectura como atributo (Sin paréntesis)
# Incorrecto: prod.margen_ganancia() -> Error
# Correcto:
print(f"Margen Inicial: {prod.margen_ganancia}") # 50

# 2. Protección de Reglas de Negocio
prod.descuento = 0.8  # El setter intercepta esto
# Salida: ⚠️ ALERTA DE COMPLIANCE: Descuento > 50% rechazado...

prod.descuento = 0.1  # Este sí pasa (10%)

# 3. Reactividad
# Note que NO tuvimos que recalcular el margen manualmente. 
# Al pedirlo de nuevo, @property volvió a ejecutar la fórmula con el nuevo descuento.
print(f"Nuevo Margen: {prod.margen_ganancia}") # 40
```

## 2. `@staticmethod`: Utilitarios de Limpieza

### ¿El Problema?

A veces tenemos funciones que son útiles para nuestros datos (como limpiar strings, convertir fechas, normalizar monedas) pero que **no necesitan saber nada de una fila o instancia específica**.

Si las ponemos fuera de la clase, ensuciamos nuestro código ("espagueti"). Si las ponemos dentro como métodos normales, Python nos obliga a poner self, aunque no lo usemos.

La Solución

`@staticmethod` nos deja poner una función dentro de una clase por orden y organización, pero esa función es independiente: no recibe `self` ni `cls`. Es una herramienta pura.

Ideal para: Data Cleaning, Conversiones de Unidades, Parsers de Texto.

```
class LimpiadorDatos:
    
    @staticmethod
    def normalizar_texto(texto):
        """
        Elimina espacios, tildes y estandariza a mayúsculas.
        No necesita 'self' porque la lógica es universal, no depende de un objeto.
        """
        if not texto or not isinstance(texto, str):
            return "N/A"
        
        texto_limpio = texto.strip().upper()
        reemplazos = (("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"))
        
        for a, b in reemplazos:
            texto_limpio = texto_limpio.replace(a, b)
            
        return texto_limpio

# Uso directo (Namespace)
# No necesitamos hacer: limpiador = LimpiadorDatos()
# Simplemente usamos la clase como una caja de herramientas:

ciudades_sucias = ["  Bogotá  ", "Medellín", None, "Chía"]
ciudades_limpias = [LimpiadorDatos.normalizar_texto(c) for c in ciudades_sucias]

print(ciudades_limpias)
# Salida: ['BOGOTA', 'MEDELLIN', 'N/A', 'CHIA']
```

## 3. `@classmethod`: Ingesta y Adaptadores

### ¿El Problema?

En BI, los datos vienen de todos lados: un CSV, una API JSON, una base de datos SQL.
El `__init__` estándar suele esperar los datos ya limpios y separados (`nombre`, `score`). ¿Cómo creamos objetos desde fuentes "sucias" o formatos diferentes sin llenar el código principal de lógica de transformación?

### La Solución

Los `@classmethod` actúan como Constructores Alternativos. Reciben `cls` (la clase misma) en lugar de `self` (el objeto), lo que les permite crear y devolver nuevas instancias de esa clase.

Ideal para: Patrones Factory, ETL, Parsing de formatos complejos.

```
class LeadCliente:
    def __init__(self, nombre, score):
        self.nombre = nombre
        self.score = score

    # CONSTRUCTOR ALTERNATIVO 1: Desde CSV
    @classmethod
    def desde_csv_string(cls, linea_csv):
        # Lógica de parsing encapsulada AQUÍ, no en el main
        try:
            nombre, score_str = linea_csv.split(',')
            # 'cls' es equivalente a llamar a LeadCliente(...)
            return cls(nombre, int(score_str))
        except ValueError:
            print("Error parseando CSV")
            return None

    # CONSTRUCTOR ALTERNATIVO 2: Desde JSON/Diccionario
    @classmethod
    def desde_json_api(cls, json_obj):
        # Mapeo de campos (ej: la API llama al campo 'lead_val' en vez de 'score')
        return cls(
            nombre=json_obj.get('name', 'Anónimo'), 
            score=json_obj.get('lead_val', 0)
        )

# Pipeline de Ingesta
# Note cómo la clase sabe "fabricarse a sí misma" desde distintos orígenes

# Fuente 1: Archivo plano
lead_csv = LeadCliente.desde_csv_string("Carlos R,70")

# Fuente 2: Respuesta de API
lead_api = LeadCliente.desde_json_api({'name': 'Maria L', 'lead_val': 95})

print(f"Lead CSV: {lead_csv.nombre} - {lead_csv.score}")
print(f"Lead API: {lead_api.nombre} - {lead_api.score}")
```

## Resumen Comparativo para BI

Esta tabla es su guía rápida para decidir qué herramienta usar en sus pipelines de datos.

| **Decorador**     | **Sintaxis de llamada**    | **¿Recibe `self`?** | **¿Recibe `cls`?** | **Propósito en Inteligencia de Negocios**                                   | **Ejemplo Típico**                                                                 |
|------------------|----------------------------|---------------------|--------------------|----------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| *(Método normal)* | `obj.metodo()`             | ✅ Sí               | ❌ No              | Acciones basadas en datos de una fila/registro específico.                 | `calcular_impuesto()` usando el monto de una transacción.                          |
| `@property`       | `obj.atributo` *(sin `()`)* | ✅ Sí               | ❌ No              | Campos calculados dinámicos o validación al asignar valores.               | `obj.margen` (cálculo en vivo), `obj.email` (valida regex en asignación).          |
| `@staticmethod`   | `Clase.metodo()`           | ❌ No               | ❌ No              | Funciones de utilidad pura: entra dato ➝ sale dato limpio.                 | `normalizar_fecha()`, `limpiar_texto()`, `convertir_usd_cop()`.                    |
| `@classmethod`    | `Clase.metodo()`           | ❌ No               | ✅ Sí              | Crear objetos desde fuentes o formatos externos (Factory methods).         | `desde_excel()`, `desde_parquet()`, `cargar_configuracion()`.                      |

### Regla de Oro

+ Si necesita acceder a `self.variable `, es un **Método Normal** o **Property**.
+ Si necesita crear una instancia nueva de la clase, es un **Classmethod**.
+ Si no toca nada de la clase y solo transforma un input, es un **Staticmethod**.
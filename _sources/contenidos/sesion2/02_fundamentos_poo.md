# 2.2 Fundamentos de POO - La "Célula" del Dato

En Inteligencia de Negocios, estamos acostumbrados a pensar en tablas gigantes (DataFrames). Sin embargo, cuando construimos pipelines de datos robustos, a veces necesitamos controlar la lógica fila por fila o entidad por entidad.

Aquí es donde la POO brilla: nos permite definir **qué es** un dato válido y qué puede hacer.

## 1. El `self`: Contexto de la Fila Actual

Imagine que está procesando un Excel con 10,000 transacciones.

+ **Enfoque Procedimental** : Usted tiene una lista de números y pasa listas a funciones. Es difícil rastrear qué dato pertenece a qué cliente.

+ **Enfoque Orientado a Objetos** : Cada fila se convierte en un objeto inteligente que sabe sus propios valores.

En este contexto, `self` es "**Esta fila específica que estoy procesando ahora mismo**".

### Ejemplo: Modelando un KPI (Indicador Clave de Desempeño)

No piense en una clase como una "plantilla", piénsela como una **Definición de Métrica**.

```
class KPIVentas:
    def __init__(self, region, venta_real, meta_mensual):
        # ESTADO: Los datos crudos de este registro
        self.region = region
        self.venta_real = venta_real
        self.meta = meta_mensual
        
    def calcular_cumplimiento(self):
        # COMPORTAMIENTO: Lógica de negocio encapsulada
        if self.meta == 0:
            return 0.0
        return (self.venta_real / self.meta) * 100

    def estado_alerta(self):
        # Regla de negocio: ¿Debemos preocuparnos?
        cumplimiento = self.calcular_cumplimiento()
        if cumplimiento < 70:
            return "ROJO: Riesgo Crítico"
        elif cumplimiento < 90:
            return "AMARILLO: Atención"
        else:
            return "VERDE: Saludable"

# Procesamiento de datos (Simulando un loop de ETL)
datos_brutos = [
    {"zona": "Norte", "real": 8500, "meta": 10000},
    {"zona": "Sur", "real": 4000, "meta": 10000}
]

for fila in datos_brutos:
    # 1. Instanciamos (Convertimos datos muertos en objetos vivos)
    kpi = KPIVentas(fila["zona"], fila["real"], fila["meta"])
    
    # 2. Le preguntamos al objeto (self sabe sus propios datos)
    print(f"Zona {kpi.region}: {kpi.calcular_cumplimiento()}% - {kpi.estado_alerta()}")

# Salida:
# Zona Norte: 85.0% - AMARILLO: Atención
# Zona Sur: 40.0% - ROJO: Riesgo Crítico
```
## 2. ``__init__``: Garantía de Calidad desde el Origen

El ``__init__`` es su primera línea de defensa en Calidad de Datos. Úselo para asegurar que un objeto no pueda existir si sus datos están sucios o incompletos.

```
class TransaccionFinanciera:
    def __init__(self, monto, moneda):
        # Validación de Calidad de Datos al instanciar
        if monto < 0:
            raise ValueError("Error de Calidad: No se permiten transacciones negativas en este flujo.")
        if moneda not in ['USD', 'COP', 'EUR']:
            raise ValueError(f"Error de Calidad: Moneda '{moneda}' no soportada.")
            
        self.monto = monto
        self.moneda = moneda

# Intento de crear dato sucio
try:
    tx = TransaccionFinanciera(-50, "PESOS")
except ValueError as e:
    print(f"Dato descartado: {e}")
    # Salida: Dato descartado: Error de Calidad: No se permiten transacciones negativas...
```
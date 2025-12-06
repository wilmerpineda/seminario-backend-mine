# 2.4 Python Moderno - Tipado Estricto y Configuraciones Robustas

En el mundo de la Inteligencia de Negocios, un error de "tipo de dato" puede costar horas de reprocesamiento. Si una función espera una lista de columnas y recibe un solo string, el script falla. Si espera un DataFrame y recibe un diccionario, falla.

Python moderno (3.9+) nos permite blindar nuestro código usando Type Hints (pistas de tipo) y **Dataclasses**. Ya no adivinamos qué entra a una función; lo declaramos explícitamente.

## 1. La "Tabla Periódica" del Tipado en Datos

Antes de escribir código, definamos cuándo usar cada estructura. Para un perfil de datos, esta es la guía de referencia:

| 🧩 **Tipo**   | 🔤 **Sintaxis escrita**                 | 🔎 **Cuándo usarlo en BI**                              | 💡 **Ejemplo aplicado al negocio**                       |
| ------------- | --------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------- |
| **DataFrame** | `pd.DataFrame`                          | Cuando usamos la tabla completa como base del análisis. | Input de un modelo, dashboards, simulaciones.            |
| **List**      | `List[tipo]` / `list[tipo]`             | Conjunto ordenado de elementos homogéneos.              | `['ventas', 'costos', 'margen']` para features objetivo. |
| **Dict**      | `Dict[key, value]` / `dict[key, value]` | Mapear claves ↔ valores, renombrar columnas.            | `{'ciu':'Ciudad','vta':'Ventas'}` limpieza de metadata.  |
| **Tuple**     | `Tuple[t1, t2]`                         | Datos inmutables: tamaños, coordenadas, pares clave.    | Tamaño gráfico `(10,6)` o ubicación `(lat,lon)`          |
| **Optional**  | `Optional[tipo]`                        | Cuando un argumento puede ser `None`.                   | `titulo: Optional[str]` para reportes opcionales.        |
| **Union**     | `Union[A, B]`                           | Parámetros multiformato (mejor evitar si se puede).     | `Union[int, str]` id de cliente como número o string.    |

A continuación se muestra un demo de una clase que utiliza las seis clases de tipado.

```
from typing import List, Dict, Tuple, Optional, Union
import pandas as pd

def analizar_metricas(
    data: pd.DataFrame,                # DataFrame principal
    columnas: List[str],               # Selección de variables
    mapeo: Optional[Dict[str, str]] = None,  # Renombres opcionales
    size: Tuple[int, int] = (10, 6),   # Tuple para dimensiones de salida
    id_cliente: Union[int, str] = "0000"  # Valor flexible (int ó str)
):
    """Ejemplo aplicable a BI — cálculo simple con anotaciones limpias."""

    if mapeo:
        data = data.rename(columns=mapeo)   # Dict
    df = data[columnas]                     # List
    
    resumen = df.describe()                 # Operación estadística
    print(f"Reporte para cliente {id_cliente}")
    print(f"Tamaño de visualización: {size}")
    
    return resumen
```

## 2. El Poder de las Dataclasses: Objetos de Configuración

En lugar de pasar 10 parámetros sueltos a una función (`color='red'`, `ancho=5`, `limite=0.8`...), es una mejor práctica agruparlos en un *Objeto de Configuración*.

Vamos a crear una **Dataclass** que controle las reglas de nuestro Análisis Exploratorio (EDA).

```
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class ConfiguracionEDA:
    """
    Define los parámetros globales para estandarizar los reportes.
    """
    dimensiones_figura: Tuple[int, int] = (10, 6)
    paleta_colores: str = "viridis"
    estilo_seaborn: str = "whitegrid"
    # Parámetro de Negocio: ¿A partir de qué valor consideramos una correlación 'fuerte'?
    umbral_correlacion: float = 0.75 
```

### ¿Por qué hacemos esto?

+ Centralización: Si queremos cambiar el tamaño de TODOS los gráficos del reporte, solo cambiamos este objeto.
+ Autocompletado: El editor de código nos mostrará qué configuraciones existen.

## 3. Caso Práctico: Refactorizando el ExploradorDatos

Vamos a tomar la siguiente clase base y la convertiremos en una herramienta profesional usando todo lo aprendido.

### Objetivo

Crear un analizador que:

+ Use *Tipado Estricto* en todos sus métodos.
+ Use la *Dataclass* para configurar gráficos y reglas.
+ Detecte automáticamente variables altamente correlacionadas (usando el umbral configurado).

<a href="../../extras/analisis_eda.py" download style="
   background:#4CAF50; padding:8px 14px; color:white; border-radius:6px;
   text-decoration:none; font-weight:bold;">
   📥 Descargar script .py
</a>

### Paso 1: Centralizar la Configuración (Dataclasses)

Abra el archivo `analisis_eda.py`. Note que en analisis_univariado, el tamaño de la figura es `(10, 6)` y el estilo es `seaborn-v0_8-whitegrid`.

Problema: Si queremos cambiar el estilo en los 50 gráficos del reporte, tenemos que buscar y reemplazar línea por línea.

Solución: Vamos a crear un objeto de configuración usando dataclasses.

📝 Tarea: Agregue esto al inicio de su script (recuerde importar dataclass y Tuple).

```
from dataclasses import dataclass
from typing import Tuple

@dataclass
class ConfiguracionEDA:
    """
    Control remoto para todos los parámetros visuales y reglas de negocio.
    """
    dimensiones: Tuple[int, int] = (10, 6)
    tema: str = "whitegrid"
    # Regla de Negocio: Umbral para alertas de correlación
    umbral_alerta: float = 0.8
```

### Paso 2: Blindando el Constructor (``__init__``)

Vamos a modificar la clase para que reciba nuestra nueva configuración.

🔴 Código Original (Legacy)

El código original solo verificaba si era un DataFrame, pero no nos decía nada más.

```
class ExploradorDatos:
    def __init__(self, dataframe):
        # ... validación básica ...
        self.datos = dataframe
```

🟢 Código Moderno (Refactorizado)

Vamos a inyectar la configuración y usar Type Hints para que el editor nos ayude.

```
# Asegúrese de importar: import pandas as pd
import seaborn as sns

class ExploradorDatosModerno:
    # 1. Type Hinting: Declaramos explícitamente qué entra
    def __init__(self, df: pd.DataFrame, config: ConfiguracionEDA):
        self.df = df
        self.config = config # Guardamos la configuración
        
        # 2. Aplicamos el tema globalmente una sola vez
        sns.set_theme(style=self.config.tema)
        print(f"--- Explorador inicializado con umbral {self.config.umbral_alerta} ---")
```

### Paso 3: Tipado en Métodos de Visualización

Miremos el método `analisis_univariado`. Originalmente recibe columna, pero no dice si es un string o una lista.

🔴 Código Original

```
def analisis_univariado(self, columna):
    # ... código con plt.figure(figsize=(10, 6)) quemado ...
    # ... código con sns.histplot ...
```

🟢 Código Moderno

Reemplazamos los valores fijos por `self.config` y añadimos tipado. Además, usaremos `Optional` para permitir títulos personalizados.

```
from typing import Optional
import matplotlib.pyplot as plt

    def plot_distribucion(self, columna: str, titulo: Optional[str] = None) -> None:
        if columna not in self.df.columns:
            print(f"Error: {columna} no existe.")
            return

        # USAMOS LA CONFIGURACIÓN (Adiós números mágicos)
        plt.figure(figsize=self.config.dimensiones)
        
        if pd.api.types.is_numeric_dtype(self.df[columna]):
            sns.histplot(data=self.df, x=columna, kde=True)
        else:
            sns.countplot(data=self.df, x=columna)
            
        # Lógica condicional limpia
        plt.title(titulo if titulo else f"Distribución de {columna}")
        plt.show()
```

### Paso 4: Agregando Inteligencia de Negocio

Ahora que tenemos una estructura robusta, agreguemos una funcionalidad nueva que use nuestro `umbral_alerta`.

Vamos a crear un método que devuelva una **Lista de Strings** (`List[str]`) con las advertencias de columnas que se parecen demasiado (colinealidad).

```
from typing import List

    def detectar_alertas(self) -> List[str]:
        """Devuelve advertencias si la correlación supera el umbral configurado."""
        
        # 1. Solo numéricas
        df_num = self.df.select_dtypes(include='number')
        matriz = df_num.corr().abs()
        
        alertas: List[str] = [] # Declaramos una lista vacía de textos
        
        cols = matriz.columns
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                valor = matriz.iloc[i, j]
                
                # 2. Usamos la regla de negocio de la Dataclass
                if valor > self.config.umbral_alerta:
                    alertas.append(f"⚠️ Alerta: {cols[i]} vs {cols[j]} ({valor:.2f})")
        
        return alertas
```

### Resultado Final: Cómo usar su nueva clase

```
# 1. Definimos las reglas del juego (Configuración)
mis_reglas = ConfiguracionEDA(
    dimensiones=(12, 5),
    tema="darkgrid",
    umbral_alerta=0.9
)

# 2. Instanciamos con seguridad
analista = ExploradorDatosModerno(df_ventas, mis_reglas)

# 3. Ejecutamos
analista.plot_distribucion("Monto_Venta")

# 4. Verificamos calidad de datos
reporte = analista.detectar_alertas()
for aviso in reporte:
    print(aviso)
```

#### ¿Qué hemos ganado?

+ Flexibilidad: Cambiando una sola línea en `ConfiguracionEDA`, todo el reporte cambia de estilo o sensibilidad.
+ Seguridad: Si intenta pasar un número donde va el dataframe, su editor le avisará antes de ejecutar.
+ Claridad: El código se explica solo. `-> List[str]` nos dice exactamente qué esperar de salida.

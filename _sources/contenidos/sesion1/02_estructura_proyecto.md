# 1.2 Anatomía de un Proyecto de Software

Como Analistas de Datos, tendemos a trabajar en una estructura plana: una carpeta con 5 archivos `.csv`, 3 notebooks llamados `analisis_v1.ipynb`, `analisis_final.ipynb`, `analisis_final_ahorasi.ipynb` y un script de Python.

Para construir **Sistemas de Analítica** (APIs, Pipelines), necesitamos una estructura jerárquica y modular.

## El Estándar "Src Layout"

La comunidad de Python ha adoptado una estructura conocida como `src-layout`. Veamos cómo se ve un proyecto profesional generado por Poetry y enriquecido manualmente:

```
analitica-pricing/
├── .gitignore           # Archivos que Git debe ignorar (ej. contraseñas, datos)
├── README.md            # La documentación principal (Portada del proyecto)
├── pyproject.toml       # Configuración del proyecto y dependencias
├── poetry.lock          # "Foto" exacta de las versiones instaladas
│
├── src/                 # CÓDIGO FUENTE
│   └── pricing_engine/  # Nombre de tu paquete (con guiones bajos)
│       ├── __init__.py  # Marca la carpeta como paquete importable
│       ├── main.py      # Punto de entrada de la aplicación
│       ├── models.py    # Definiciones de datos
│       └── utils.py     # Funciones auxiliares
│
├── tests/               # PRUEBAS AUTOMATIZADAS
│   ├── __init__.py
│   └── test_models.py   # Pruebas específicas para models.py
│
└── data/                # (Opcional) Datos locales
    ├── raw/             # Datos crudos (nunca se modifican)
    └── processed/       # Datos limpios
```

## Desglosando los Componentes Clave

1. `pyproject.toml` (El Cerebro)

Es el archivo de configuración moderno. Reemplaza a `setup.py`, `requirements.txt` y configuraciones de herramientas como `pytest.ini`. Aquí defines quién eres, qué versión es tu software y qué necesita para correr.

2. La carpeta `src/` (El Músculo)

¿Por qué meter el código en una subcarpeta `src`?

Evita errores de importación: Te obliga a instalar tu propio paquete para probarlo, simulando cómo lo usaría un usuario real.

Mantiene la raíz limpia: En la raíz solo deben ir archivos de configuración y documentación.

3. `__init__.py` (El Pegamento)

Este archivo (a menudo vacío) le dice a Python: "*Trata a esta carpeta como un paquete de software, no solo como un directorio de archivos*". Permite hacer importaciones como:
from `pricing_engine.utils import calcular_descuento`

4. `.gitignore` (El Filtro)

Fundamental en analítica. Aquí le decimos a Git qué **NO** subir. Regla de oro: Nunca subas datos (`.csv`, `.xlsx`), credenciales (`.env`), ni carpetas generadas automáticamente (`__pycache__`, `.venv`).

Un ejemplo de .gitignore para Python:

```
__pycache__/
*.py[cod]
.venv/
.env
.DS_Store
data/
```
# 1.5 Taller Práctico: El "Converter" Financiero

## Objetivo

Configurar un entorno de desarrollo profesional desde cero para crear una pequeña librería de conversión de monedas, aplicando el flujo de trabajo de Git y la gestión de dependencias con Poetry.

## Escenario de Negocio

El equipo de Finanzas de tu compañía tiene una lista de precios de productos internacionales en Dólares (USD), pero necesitan reportarlos a la DIAN en Pesos Colombianos (COP). Actualmente lo hacen manual en Excel y se equivocan frecuentemente.

Te han encargado crear una pequeña herramienta en Python que automatice este cálculo.

## Paso 1: Creación del Repositorio (GitHub)

El primer paso de todo proyecto profesional inicia en el control de versiones remoto.

1. Ve a tu cuenta de [GitHub](https://github.com/).

2. Crea un Nuevo Repositorio, nómbralo: taller-poetry-finance.

3. Importante:

    + Public/Private: A tu elección.
    + Add README file: No (lo crearemos localmente).
    + Add .gitignore: Selecciona Python.
    + License: Selecciona MIT License.

Clona el repositorio en tu computador:

```
git clone [https://github.com/TU_USUARIO/taller-poetry-finance.git](https://github.com/TU_USUARIO/taller-poetry-finance.git)
cd taller-poetry-finance
```

## Paso 2: Inicialización con Poetry

Vamos a convertir esta carpeta vacía en un proyecto de Python moderno.

1. Dentro de la carpeta, inicializa la estructura:

```
poetry new . --src
```

(*El punto . indica que use la carpeta actual. El flag --src fuerza la estructura profesional*).

2. Verifica que tu estructura se vea así:

```
taller-poetry-finance/
├── .gitignore
├── pyproject.toml  <-- ¡Nuevo!
├── README.md
├── src/
│   └── taller_poetry_finance/
│       └── __init__.py
└── tests/
```

3. Instala las dependencias. Aunque aún no usaremos librerías externas complejas, instalaremos requests para simular que consultamos una tasa de cambio en el futuro.

```
poetry add requests
```

## Paso 3: El Flujo de Trabajo (Git Branching)

⛔ ¡ALTO! No escribas código en la rama `main`.

Vamos a simular que estás desarrollando la funcionalidad de conversión.

1. Crea una nueva rama (feature branch):

```
git checkout -b feat/logica-conversion
```

2. Abre el proyecto en VS Code:

```
code .
```

## Paso 4: Desarrollo del Código

Vamos a crear la lógica.

1. Navega a src/taller_poetry_finance/.

2. Crea un archivo llamado conversion.py.

3. Copia y pega el siguiente código, incluso mejóralo:

```
def convertir_usd_a_cop(lista_precios_usd, tasa_cambio=4100):
    """
    Convierte una lista de precios de dólares a pesos colombianos.
    
    Args:
        lista_precios_usd (list): Lista de precios en USD.
        tasa_cambio (float): Tasa de cambio fija (default 4100).
        
    Returns:
        list: Lista de precios convertidos a COP.
    """
    precios_cop = []
    for precio in lista_precios_usd:
        # Lógica simple de conversión
        nuevo_precio = precio * tasa_cambio
        precios_cop.append(nuevo_precio)
    
    return precios_cop
```

4. Modifica el archivo `src/taller_poetry_finance/__init__.py` para exponer tu función:

```
from .conversion import convertir_usd_a_cop

```

## Paso 5: Probando en el Entorno Virtual

Para verificar que funciona, crearemos un script temporal de prueba (simulando un "Main").

1. Crea un archivo `run.py` en la raíz del proyecto (al nivel de `pyproject.toml`).

2. Agrega este contenido:

```
from taller_poetry_finance import convertir_usd_a_cop

precios_internacionales = [100, 50, 25.5, 10]
precios_locales = convertir_usd_a_cop(precios_internacionales)

print(f"Precios en USD: {precios_internacionales}")
print(f"Precios en COP: {precios_locales}")
```

3. El momento de la verdad: Ejecuta el script usando el entorno de Poetry:

```
poetry run python run.py
```

Si ves la lista convertida en tu terminal, ¡felicidades! Has creado y ejecutado un paquete correctamente aislado.

## Paso 6: Guardar y Publicar

Ahora vamos a subir tu trabajo para revisión.

1. Añade los cambios a Git (nota cómo `poetry.lock` se añade automáticamente):

```
git add .
```

2. Realiza el commit:

```
git commit -m "feat: implementa función básica de conversión usd-cop"
```

3. Sube la rama a GitHub:

```
git push origin feat/logica-conversion
```

4. **Entregable**: Ve a tu repositorio en GitHub. Verás un botón verde que dice "**Compare & pull request**".

    + Presiónalo.
    + Ponle un título descriptivo.
    + Dale a "Create Pull Request".
    + Copia el link del Pull Request y ese será tu entregable de la sesión.
# 1.1 Del Caos al Orden: Gestión de Dependencias con Poetry

## El Problema del "En mi máquina funciona"

Imagina este escenario: Acabas de terminar un modelo de predicción de churn para el banco. Usaste `pandas`, `scikit-learn` y una librería específica para conectar con Oracle. Todo funciona perfecto en tu laptop. Le envías el código al ingeniero de DevOps para que lo ponga en producción, y a los 5 minutos recibes un correo: "**El build falló. No encuentra la librería X**" o peor aún, "**Los resultados son diferentes a los que reportaste**".

Esto sucede por el "Infierno de las Dependencias" (*Dependency Hell*).

### ¿Por qué fallan `pip` y `conda`?

Históricamente, hemos usado dos herramientas:

1. Pip + requirements.txt:

    + El problema: `pip freeze > requirements.txt` guarda todo lo que hay en tu entorno, incluyendo librerías basura que no usas. Además, no siempre resuelve conflictos de versiones entre sub-dependencias (ej: Librería A pide numpy 1.20, Librería B pide numpy 1.24).

2. Conda:

    + El problema: Es excelente para Ciencia de Datos exploratoria, pero es pesado y lento para entornos de producción en la nube (Docker). A veces mezcla canales (`conda-forge` vs `defaults`) rompiendo binarios.

## La Solución: Poetry

**Poetry** es la herramienta estándar moderna para el packaging y gestión de dependencias en Python. Nos ofrece:

1. **Determinismo**: Garantiza que, si funciona en tu máquina, funcionará exactamente igual en el servidor, bit a bit.

2. **Separación de Intereses**: Diferencia entre librerías que necesitas para correr la app (pandas, fastapi) y librerías para desarrollar (pytest, black, jupyter).

3. **Resolución de Conflictos**: Si intentas instalar dos librerías incompatibles, Poetry te avisará antes de romper tu entorno.

### Instalación y Configuración

Aunque tengas Anaconda, instalaremos Poetry a nivel de sistema operativo (PowerShell o Terminal):

```
# Windows (PowerShell)
(Invoke-WebRequest -Uri [https://install.python-poetry.org](https://install.python-poetry.org) -UseBasicParsing).Content | python -

# macOS / Linux
curl -sSL [https://install.python-poetry.org](https://install.python-poetry.org) | python3 -
```

Para verificar que quedó instalado:

```
poetry --version
```

### Tu Primer Proyecto Profesional

Olvídate de crear una carpeta y tirar archivos adentro. Vamos a inicializar un proyecto con estructura estándar.

```
poetry new analitica-pricing
cd analitica-pricing
```

### Comandos Esenciales

| **Comando**                       | **Descripción**                                                 | **Equivalente antiguo**                 |
|----------------------------------|-----------------------------------------------------------------|----------------------------------------|
| `poetry add pandas`              | Instala una librería y la añade al proyecto                     | `pip install pandas`                   |
| `poetry add --group dev black`   | Instala una herramienta solo para desarrollo                    | N/A                                    |
| `poetry remove requests`         | Desinstala una librería limpiamente                             | `pip uninstall requests`               |
| `poetry shell`                   | Activa el entorno virtual aislado                               | `conda activate ...`                   |
| `poetry install`                 | Instala todo lo necesario (ideal para clonar repos)             | `pip install -r req.txt`               |


:::{note}
El archivo `poetry.lock` es **sagrado**. Poetry genera un archivo llamado `poetry.lock`. Este archivo registra las versiones exactas (con hash criptográfico) de todas las librerías instaladas. Siempre debes subir este archivo a Git. Es la garantía de que tus compañeros instalarán exactamente lo mismo que tú.
:::
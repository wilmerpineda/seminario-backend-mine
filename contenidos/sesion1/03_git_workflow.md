# 1.3 Flujo de Trabajo con Git en Equipos de Datos

Git no es solo "Guardar versiones". Es una herramienta de comunicación asíncrona. En un equipo de analítica, Git permite que una persona trabaje en la limpieza de datos mientras otra ajusta los hiperparámetros del modelo, sin borrarse el trabajo mutuamente.

![Flujo de Git](../../images/git_flow.jpg)

## Malas Prácticas Comunes

1. **Committear Notebooks**: Los archivos `.ipynb` son JSONs gigantes. Un cambio pequeño en una gráfica genera miles de líneas de diferencia, haciendo imposible la revisión.

2. **Trabajar solo en `main`**: Si rompes `main` (la rama principal), detienes el trabajo de todos.

3. **Mensajes de commit vagos**: "Update", "Fix", "Cambios".

## El Flujo de Trabajo Recomendado (Feature Branch Workflow)

Seguiremos este ciclo para cada tarea que realicemos en el seminario:

### 1. Clonar y Actualizar

Antes de empezar, asegúrate de tener la última versión.

```
git checkout main
git pull origin main
```

### 2. Crear una Rama (Branch)

Nunca trabajes directo en `main`. Crea una rama con un nombre descriptivo de lo que vas a hacer.

```
# Estructura: tipo/descripcion-corta
git checkout -b feat/crear-endpoint-usuarios
# O para arreglar errores
git checkout -b fix/error-calculo-iva
```

### 3. Trabajar y Committear

Haces tus cambios en el código. Luego guardas.

```
git add .
git commit -m "feat: añade modelo de usuario con pydantic"
```

Tip: *Usa "Conventional Commits" (feat, fix, docs, style, refactor).*

### 4. Publicar (Push)

Subes tu rama a la nube (GitHub/GitLab).

```
git push origin feat/crear-endpoint-usuarios
```

### 5. Pull Request (PR)

Esta es la parte más importante. En la interfaz web de GitHub, abres un "Pull Request".

+ Es una solicitud para fusionar tus cambios con la rama principal.

+ Aquí tus compañeros revisan tu código, sugieren mejoras y detectan errores antes de que lleguen a producción.

+ Solo cuando se aprueba, se hace el "Merge".

## Configuración para Notebooks (Opcional pero Recomendado)

Si debes usar notebooks, instala `nbstripout` para limpiar las salidas (outputs) antes de subir a Git. Esto permite guardar el código pero ignorar las gráficas y tablas que ensucian el historial.

```
poetry add --group dev nbstripout
poetry run nbstripout --install
```
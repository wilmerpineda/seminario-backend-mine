# 1.4 Guía Técnica: Configuración de Entorno (Git + VS Code)

Esta guía complementaria está diseñada para resolver los problemas técnicos más comunes antes de empezar a programar. Sigue estos pasos para dejar tu computador listo para el desarrollo profesional

## Parte 1: Identidad en Git

Aunque hayas instalado Git, este no sabe quién eres. Cada "Commit" que hagas debe llevar tu firma.

1. Abre tu terminal (PowerShell o Terminal).

2. Ejecuta los siguientes comandos (reemplaza con tus datos reales):

```
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu_email@ejemplo.com"
```

**Nota**: Usa el mismo correo electrónico con el que creaste tu cuenta de GitHub para que tus contribuciones se registren correctamente en tu perfil.

## Parte 2: Vincular VS Code con GitHub

Olvídate de gestionar claves SSH manualmente por ahora. VS Code tiene una integración nativa excelente.

1. Abre Visual Studio Code.

2. En la barra lateral izquierda, busca el icono de Cuentas (un círculo con una silueta humana, usualmente abajo a la izquierda).

3. Haz clic en "Sign in to Sync Settings" (Iniciar sesión para sincronizar ajustes) o simplemente "Sign in".

4. Selecciona "Sign in with GitHub".

5. Se abrirá tu navegador. Autoriza el acceso a VS Code.

¡Listo! Ahora VS Code tiene permiso para clonar, hacer push y pull de tus repositorios privados sin pedirte contraseña a cada rato.

## Parte 3: Configuración Maestra de Poetry y VS Code

Este es el secreto para que VS Code detecte tus librerías automáticamente.

Por defecto, Poetry crea los entornos virtuales en una carpeta oculta en tu sistema (*/Users/tu/.cache/...*). Esto confunde a VS Code. Vamos a decirle a Poetry que cree el entorno dentro de la carpeta de tu proyecto.

En tu terminal, ejecuta este comando una única vez (queda configurado para siempre):

```
poetry config virtualenvs.in-project true
```

¿Qué hace esto?

La próxima vez que hagas `poetry install` en un proyecto nuevo, Poetry creará una carpeta llamada `.venv` justo al lado de tu código. VS Code ama esta carpeta y la detectará automáticamente.

## Parte 4: Seleccionar el Intérprete Correcto

Cuando abras un archivo de Python en VS Code, puede que veas errores o subrayados amarillos aunque ya hayas instalado las librerías con Poetry. Esto pasa porque VS Code está usando el Python "global" de tu computador, no el del proyecto.

**Pasos para arreglarlo:**

1. Abre cualquier archivo .py de tu proyecto (ej. `run.py` o `conversion.py`).

2. Mira la **esquina inferior derecha** de VS Code. Verás algo como `3.10.1 64-bit` o `Select Interpreter`.

3. Haz clic ahí (o presiona `Ctrl+Shift+P` y escribe: `Python: Select Interpreter`).

4. Busca en la lista la opción que diga (`'venv': poetry`) o que tenga la ruta `./.venv/bin/python`. Debería tener una estrella o decir "*Recommended*".

5. Selecciónalo.

Ahora, cuando abras una nueva terminal en VS Code (`Ctrl+ñ` o `Ctrl+Shift+´`), verás que automáticamente aparece (`.venv`) al inicio de la línea. ¡Ya estás dentro del entorno correcto!

## Checklist de Verificación

Antes de la próxima clase, asegúrate de cumplir con esto:

[ ] Al escribir `git config --list` en la terminal, aparecen tu nombre y correo.

[ ] En VS Code, al abrir el proyecto, ves la carpeta `.venv` en el explorador de archivos (si no, borra el entorno anterior y corre `poetry install` de nuevo).

[ ] Al abrir una terminal en VS Code, el prompt empieza con (`.venv`).

[ ] Puedes hacer `git push` sin que te pida contraseña en la terminal.

Si tienes los 4 puntos, ¡tu entorno es nivel Senior! 🚀
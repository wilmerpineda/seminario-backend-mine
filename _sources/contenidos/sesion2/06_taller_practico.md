# 2.6 Proyecto Integrador - SmartPortfolio 🚀

¡Hemos llegado a la meta! Es hora de dejar la teoría y ensuciarse las manos.

En este taller final, ustedes no son estudiantes; son el Equipo Fundador de Ingeniería de una Fintech llamada "SmartPortfolio".

## 1. El Desafío de Negocio 💼

Actualmente, los analistas financieros de la empresa llevan el control de las inversiones en Excel.
El Problema: La semana pasada, un error de "copiar y pegar" en una fórmula de Excel costó $5,000 USD en pérdidas. La Solución: Ustedes deben construir el "Core Bancario" (Backend) en Python. Un sistema robusto, tipado y validado que impida errores humanos.

## 2. Reglas del Juego: Equipos y Roles 👥

Formarán equipos de 3 Personas. Cada uno tendrá un rol técnico en GitHub, simulando un entorno real de desarrollo.

### 🏗️ Rol A: El Arquitecto (Repository Owner)

+ Crea el repositorio en GitHub (smart-portfolio-core).
+ Configura las reglas de protección (nadie puede borrar main).
+ Define la estructura de carpetas inicial.
+ Revisa y aprueba los Pull Requests (PR).

### 💻 Roles B y C: Los Desarrolladores (Contributors)

+ Clonan el repositorio.
+ Crean ramas (feature/modelos, feature/reportes) para trabajar.
+ Escriben el código limpio usando Dataclasses y Type Hints.
+ Abren Pull Requests solicitando revisión.

## 3. Arquitectura del Sistema (Requerimientos Técnicos)

El sistema debe cumplir estrictamente con los siguientes diseños de clases.

### A. El Modelo de Datos (Dominio)

Archivo sugerido: `src/modelos.py`

1. `Instrumento` (Dataclass Inmutable)

    + Debe ser una @dataclass(frozen=True).
    + Atributos: `ticker` (str), `tipo` (str - ej: "Acción", "Bono"), `sector` (str).
    + Por qué: Un instrumento financiero como "AAPL" es un hecho, no cambia.

2. `Posicion` (Lógica de Negocio)

    + Atributos:

        - `instrumento`: (Debe ser del tipo clase Instrumento).
        - `cantidad`: (float).
        - `precio_entrada`: (float).

    + Validación con `@property`:
        - La `cantidad` NO puede ser negativa. Si intentan asignar -10, debe lanzar un `ValueError`.

    + Método `calcular_valor_actual(precio_mercado)`:
        - Retorna `cantidad * precio_mercado`.

### B. El Gestor (Lógica de Colección)

Archivo sugerido: `src/portafolio.py`

3. `Portafolio`
    + Debe contener una lista de posiciones.
    + Método `agregar_posicion(...)`: Recibe un objeto `Posicion` y lo guarda.
    + Reto de Tipado: Use `List[Posicion]` en los Type Hints.

## C. El Reportador (Aplicando SOLID - SRP)

Archivo sugerido: `src/reportes.py`

4. `ReportadorFinanciero`
    + Esta clase NO guarda datos. Solo recibe un `Portafolio` y genera salidas.
    + Método `imprimir_resumen(portafolio)`: Imprime en consola algo bonito.
    + Bonus (OCP): Si pueden, hagan que exporte a CSV o JSON.

## 4. Flujo de Trabajo (Git Flow) ​​​​🔁

Para aprobar, deben demostrar que saben trabajar en equipo sin pisarse el código.

### Paso 1: Inicialización (Arquitecto)

1. Crear repo en GitHub.
2. Clonar en local.
3. Crear estructura de carpetas:

```
smart-portfolio/
├── src/
│   ├── __init__.py
│   ├── modelos.py
│   └── ...
├── .gitignore (Python)
├── README.md
└── main.py (Script de prueba)
```

4. Hacer `git push origin main`.

### Paso 2: Desarrollo Paralelo (Devs)

Estos son los pasos a seguir para el desarrollo en paralelo:
+ Dev 1: Crea rama `feat/modelos`. Implementa `Instrumento` y `Posicion`.
+ Dev 2: Crea rama `feat/logica`. Implementa `Portafolio` y `Reportador`.

### Paso 3: Integración (Todos)

1. Cada Dev hace `git push` de su rama.
2. Abren un **Pull Request** en GitHub hacia `main`.
3. **Code Review**: El Arquitecto (y los otros devs) deben entrar a GitHub, leer el código y dejar al menos 1 comentario (pregunta o sugerencia).
4. Si todo está bien, hacer **Merge**.

## Criterios de Evaluación (Rúbrica) 📝

Su proyecto será evaluado bajo estos 3 pilares:

| 🧱 **Pilar Evaluado**                  |                                               📌 **Peso** | 🏆 **Criterio de Éxito**                                                                             |
| -------------------------------------- | --------------------------------------------------------: | ---------------------------------------------------------------------------------------------------- |
| **Calidad de Código (Python Moderno)** | <span style="color:#60A5FA; font-weight:bold;">40%</span> | Uso correcto de `@dataclass`, validaciones con `@property`, y **Type Hints en todas las funciones**. |
| **Arquitectura (POO + SOLID)**         | <span style="color:#34D399; font-weight:bold;">30%</span> | Separación clara entre módulos (`modelos.py` vs `reportes.py`), clases con una sola responsabilidad. |
| **Colaboración (Git)**                 | <span style="color:#FBBF24; font-weight:bold;">30%</span> | Flujo limpio con **ramas**, historial visible y **Pull Request documentado y aprobado**.             |


## Entregable Final

No deben enviar archivos adjuntos. Solo deben enviar el Link del Repositorio de GitHub. En el README.md del repo deben poner los nombres de los integrantes y sus roles.

### 💡 Pista para el main.py

Su script final para probar que todo funciona debería verse así:

```
from src.modelos import Instrumento, Posicion
from src.portafolio import Portafolio
from src.reportes import ReportadorFinanciero

# 1. Definir Activos
apple = Instrumento(ticker="AAPL", tipo="Acción", sector="Tecnología")
tesoro = Instrumento(ticker="US10Y", tipo="Bono", sector="Gobierno")

# 2. Crear Operaciones (Con validación automática)
pos1 = Posicion(instrumento=apple, cantidad=10, precio_entrada=150)
pos2 = Posicion(instrumento=tesoro, cantidad=5, precio_entrada=100)

# 3. Gestionar Portafolio
fondo = Portafolio()
fondo.agregar_posicion(pos1)
fondo.agregar_posicion(pos2)

# 4. Reportar (SOLID en acción)
reportador = ReportadorFinanciero()
reportador.imprimir_resumen(fondo)
```
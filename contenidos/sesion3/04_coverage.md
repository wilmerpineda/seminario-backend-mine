## 3.4 📊 Code Coverage: ¿qué tanto probamos realmente?

Escribiste **10 tests**. Genial 👏  
Pero ahora viene la pregunta incómoda:

> ¿Estás probando **todo tu código**… o solo el **10%**?

El **Code Coverage (Cobertura)** es una métrica que nos indica **qué líneas de nuestro código fueron ejecutadas durante la ejecución de los tests**.  
No mide calidad directamente, pero sí nos da una **señal objetiva** de qué tan protegida está nuestra base de código.

---

## 🧠 ¿Qué mide exactamente el coverage?

Cuando ejecutas tus tests con cobertura activada, la herramienta revisa:

- Qué **líneas ejecutables** se ejecutaron
- Cuáles **nunca fueron tocadas**
- En qué archivos están los mayores vacíos de pruebas

📌 Importante:  
El coverage **no sabe si el resultado es correcto**, solo sabe si el código fue ejecutado.

---

## 🧩 Instalación del plugin

Para usar coverage con Pytest necesitamos un plugin adicional: `pytest-cov`.

Si trabajas con Poetry, instálalo como dependencia de desarrollo:

```bash
poetry add pytest-cov --group dev
```

Esto asegura que:
- No se incluya en producción
- Esté disponible para desarrollo y CI

---

## ▶️ Generando el reporte en consola

Una vez instalado, ejecuta tus tests con la bandera `--cov`.

```bash
# Apuntamos a la carpeta 'src' para medir solo NUESTRO código
poetry run pytest --cov=src
```

El resultado será una tabla similar a esta en la terminal:

```text
Name                          Stmts   Miss  Cover
-------------------------------------------------
src/smart_portfolio/model.py     45      5    88%
src/smart_portfolio/utils.py     10     10     0%
-------------------------------------------------
TOTAL                            55     15    72%
```

---

## 🧮 ¿Cómo leer este reporte?

- **Stmts (Sentencias)**  
  Líneas de código ejecutables detectadas.

- **Miss (Perdidas)**  
  Líneas que los tests **nunca tocaron**.

- **Cover**  
  Porcentaje de líneas ejecutadas al menos una vez.

📌 Ejemplo de lectura:
- `utils.py` tiene **0%** → ningún test lo está usando
- `model.py` tiene buena cobertura, pero aún hay caminos sin probar

---

## 🌐 Reporte visual (HTML)

La verdadera potencia del coverage aparece cuando lo ves **línea por línea**.

Ejecuta:

```bash
poetry run pytest --cov=src --cov-report=html
```

Esto generará una carpeta llamada:

```text
htmlcov/
```

Dentro encontrarás un archivo `index.html`.  
Ábrelo en tu navegador y verás tu código **pintado**:

- 🟢 **Verde** → línea probada
- 🔴 **Rojo** → línea no probada (⚠️ aquí suelen vivir los bugs)
- 🟡 **Amarillo** → ramas parcialmente cubiertas (`if / else`)

---

## ⚠️ La falacia del 100%

:::{warning}
Tener **100% de cobertura** **no significa** que tu código sea perfecto.  
Solo significa que **todas las líneas fueron ejecutadas**.

Puedes ejecutar una línea que hace:

```python
return 2 + 2 == 5
```

…y aun así tener 100% de coverage.

👉 **La calidad de los tests importa más que la cantidad.**
:::

---

## 🧠 Buen criterio profesional

Usa el coverage para:

- 🔍 Detectar código muerto
- 🧪 Encontrar ramas sin tests
- 🧱 Priorizar dónde escribir nuevos tests

No lo uses para:

- ❌ Inflar métricas sin sentido
- ❌ Escribir tests inútiles solo para “pintar de verde”
- ❌ Castigar equipos por no llegar al 100%

---

## 🎯 Cierre del capítulo

El coverage no es un objetivo final.  
Es un **instrumento de diagnóstico**.

Los buenos equipos no preguntan:
> “¿Tenemos 100%?”

Preguntan:
> “¿Estamos probando lo que **realmente importa** del negocio?”

Y ahí es donde el testing se vuelve una ventaja competitiva 🚀

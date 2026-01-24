# 🛡️ Ingeniería de Datos y Calidad: Guía de Testing Automatizado

    **Para el estudiante de BI**: En el mundo de los datos, la confianza es la moneda de cambio. Un dashboard visualmente impactante no sirve de nada si los números subyacentes son incorrectos. El testing automatizado es tu póliza de seguro contra decisiones basadas en datos erróneos.

## 1. Fundamentos: La Filosofía del Testing en Negocios

¿Por qué un analista o ingeniero de datos debería escribir pruebas? En Ciencia de Datos e Inteligencia de Negocios, el objetivo principal es *mitigar riesgos financieros y reputacionales*.

Imagina un error en tu código. Existen dos tipos:

### 💥 Error Ruidoso (Loud Error)

El programa falla inmediatamente.

+ Ejemplo: Intentas dividir por cero o conectar a una base de datos con la contraseña incorrecta. El script se detiene y sale un error en rojo.

+ Impacto: Bajo. Te das cuenta al instante y lo arreglas antes de entregar el reporte.

### 🐍 Error Silencioso (Silent Error) — El enemigo del BI

La lógica es incorrecta, pero el código sigue corriendo sin quejarse.

+ Ejemplo: Un cálculo de margen de ganancia usa el costo bruto en lugar del neto. El reporte muestra un ROI de 15% cuando la realidad es -2%.

+ Impacto: Catastrófico. La gerencia toma decisiones de inversión basadas en una mentira. Nadie se da cuenta hasta meses después.

Conclusión: El testing automatizado es la red de seguridad que atrapa estos errores silenciosos antes de que lleguen al Dashboard del CEO.

## 2. Estrategia: La Pirámide de Testing

No todos los tests tienen el mismo costo ni valor. En un proyecto de datos, debemos estructurarlos jerárquicamente:

### 🔻 La Base: Unit Tests (Pruebas Unitarias)

Son el cimiento de la pirámide y donde debes invertir el 70% de tu tiempo.

+ ¿Qué son? Prueban una sola pieza aislada de lógica (una función de limpieza, un cálculo de KPI).

+ Ejemplo BI: Verificar que una función calcular_iva(monto) retorna exactamente el 19% o 21% según corresponda.

+ Ventaja: Corren en milisegundos. Si algo falla, sabes exactamente en qué línea de código fue.

### 🔸 El Centro: Integration Tests (Pruebas de Integración)

+ ¿Qué son? Verifican cómo interactúan dos piezas distintas o sistemas.

+ Ejemplo BI: Tu script de Python toma datos, los transforma y los carga en una base de datos SQL. ¿Los tipos de datos coinciden? ¿Se cortaron los textos largos?

+ Objetivo: Asegurar que las "tuberías" (pipelines) conectan bien.

### 🔺 La Cima: End-to-End (E2E)

+ ¿Qué son? Simulan todo el flujo del dato, desde el archivo crudo (CSV/API) hasta el reporte final.

+ Desventaja: Son lentos y difíciles de mantener. Úsalos con moderación para flujos críticos.

## 3. Herramienta Estándar: Pytest

Para implementar esto en Python (el lenguaje estándar en Data), utilizamos pytest. Es la herramienta favorita de la industria por ser limpia, directa y poderosa.

**Configuración**

Pytest actúa como un "sabueso": busca automáticamente en tu proyecto cualquier archivo que empiece por test_ y ejecuta las funciones dentro que también empiecen por test_.

### 🧪 Ejecución de tests con Pytest (usando Poetry)

| Comando                  | Acción                                                                 | ¿Cuándo usarlo? 🧠                                              | Ejemplo práctico 📌 |
|--------------------------|-------------------------------------------------------------------------|------------------------------------------------------------------|---------------------|
| `poetry run pytest`      | Ejecuta **todos los tests** del proyecto.                               | Antes de hacer un *commit* o *push* para validar que todo funciona. | Verificar que el proyecto está estable antes de subir cambios. |
| `poetry run pytest -v`   | Modo **verbose**. Muestra qué test se ejecuta, pasa o falla.            | Cuando quieres entender el flujo de ejecución o revisar cobertura lógica. | Identificar exactamente qué test falló en un pipeline CI. |
| `poetry run pytest -x`   | Detiene la ejecución **al primer error** encontrado.                   | Ideal para **debug** cuando hay muchos fallos encadenados.       | Corregir un bug crítico sin ruido de otros errores. |

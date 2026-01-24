# 🧪 Cómo pensar un test profesional (patrón AAA)

Un test profesional —por simple que sea— sigue una **estructura mental clara**.  
No se trata solo de “probar código”, sino de **validar una hipótesis de negocio**.

En este ejemplo vamos a probar una función sencilla pero muy común:  
👉 **el cálculo de un descuento según el tipo de cliente**.

---

### 🧠 Función de negocio a probar

Supongamos que tenemos la siguiente función en nuestro código productivo:

```python
def calcular_descuento(precio: float, es_vip: bool) -> float:
    """
    Calcula el precio final aplicando un descuento si el cliente es VIP.

    Parameters
    ----------
    precio : float
        Precio base del producto.
    es_vip : bool
        Indica si el cliente pertenece al segmento VIP.

    Returns
    -------
    float
        Precio final después de aplicar el descuento.
    """
    if es_vip:
        return precio * 0.80  # 20% de descuento
    return precio
```

---

### 🧩 El patrón AAA (Arrange – Act – Assert)

Un buen test sigue siempre el patrón **AAA**, que hace explícita la intención del test:

1. **Arrange** → preparar el escenario  
2. **Act** → ejecutar la funcionalidad  
3. **Assert** → verificar la hipótesis  

Este patrón mejora la legibilidad, el mantenimiento y la comunicación del test.

---

### 🧪 Test unitario usando Pytest

```python
# Archivo: test_negocio.py

from negocio import calcular_descuento


def test_descuento_para_clientes_vip():
    # 1. Arrange (Preparar el escenario)
    precio_base = 100
    cliente_es_vip = True

    # 2. Act (Ejecutar la funcionalidad)
    precio_final = calcular_descuento(precio_base, cliente_es_vip)

    # 3. Assert (Verificar la hipótesis)
    # Esperamos que 100 con 20% de descuento sea 80
    assert precio_final == 80
```

---

### 🛡️ El poder del `assert`

En Python, `assert` actúa como un **guardián lógico**.

Le dices explícitamente al código:

> “Afirmo que esto es verdad.  
> Si no lo es, detén todo y grita.”

Pytest intercepta ese "grito" y lo transforma en un reporte claro y accionable.  

```text
E       assert 85 == 80
E        + where 85 = calcular_descuento(100, True)
```

---

### 🎯 Idea clave para llevarte

> Un buen test no solo detecta errores.  
> **Protege las reglas del negocio** frente a cambios accidentales.

---

## 💡 Siguiente paso sugerido

Para fortalecer esta batería de tests, lo natural sería añadir:

- Un test para **clientes no VIP**
- Un test con **precios decimales**
- Tests para **casos borde** (valores inválidos o extremos)

Así es como se construyen tests profesionales, mantenibles y confiables.


# 🚀 Escalando tus tests en proyectos de BI y Data Science

Cuando tus proyectos de **Business Intelligence** crecen —ETLs complejos, múltiples fuentes de datos, modelos de *Machine Learning*— los tests simples ya no son suficientes.  
Necesitas **herramientas más potentes**, pero también más elegantes.

En esta sección veremos cuatro conceptos clave que marcan la diferencia entre *tests básicos* y *tests profesionales*.

---

### 🛠️ Fixtures: tus datos de prueba reutilizables

En BI y Data Science es muy común necesitar **datos falsos o controlados** para probar:

- Un `DataFrame` pequeño
- Un JSON de ejemplo
- Un conjunto mínimo de registros representativos

Crear estos datos manualmente en cada test es repetitivo y propenso a errores.  
Aquí es donde entran las **fixtures** de Pytest.

#### 🧠 Idea clave
Una *fixture* es una función que **prepara datos o recursos** y Pytest los **inyecta automáticamente** en los tests que los necesitan.

#### 🍳 Analogía (Mise en place)
Es como cocinar con todos los ingredientes **ya lavados, picados y medidos** antes de empezar.  
No repites trabajo y reduces errores.

---

#### 🧪 Ejemplo de fixture con Pandas

```python
import pytest
import pandas as pd


@pytest.fixture
def datos_ventas_dummy():
    """
    DataFrame pequeño y controlado para pruebas de ventas.
    Reutilizable en múltiples tests.
    """
    return pd.DataFrame({
        "producto": ["A", "B"],
        "precio": [100, 200],
        "cantidad": [1, 2]
    })
```

#### ✅ Uso de la fixture en un test

```python
def test_total_ventas(datos_ventas_dummy):
    # Pytest inyecta automáticamente el DataFrame
    assert datos_ventas_dummy["precio"].sum() == 300
```

📌 **Ventajas**:
- Datos consistentes entre tests
- Código más limpio
- Fácil mantenimiento si cambian los datos

---

### 🔄 Parametrización: no te repitas (DRY)

Un antipatrón común es escribir **muchos tests casi idénticos** para distintos valores de entrada.

Si quieres probar una función con varios escenarios, **parametriza**.

#### 🧠 Idea clave
La parametrización permite ejecutar **el mismo test múltiples veces**, cambiando solo los datos.

---

#### 🧪 Ejemplo: cálculo de impuestos

```python
import pytest


@pytest.mark.parametrize(
    "input_monto, esperado",
    [
        (100, 119),   # Caso normal
        (0, 0),       # Caso borde: cero
        (10, 11.9),   # Caso con decimales
    ],
)
def test_calculo_iva(input_monto, esperado):
    assert calcular_iva_con_impuesto(input_monto) == esperado
```

📌 **Beneficios**:
- Menos código
- Más cobertura de escenarios
- Tests más expresivos y legibles

---

### 🎭 Mocking: fingiendo la realidad (de forma inteligente)

A veces tu código depende de elementos externos:

- APIs (bancos, clima, tasas de cambio)
- Bases de datos
- Servicios en la nube

Si esos servicios fallan —o no tienes internet— **tu test también fallaría**, aunque tu lógica esté bien.

#### 🧠 Solución: Mocking

El *mocking* consiste en **fingir la respuesta** de esos servicios externos.

> No pruebas la API.  
> Pruebas **cómo tu código reacciona** a una respuesta.

#### 🎯 Beneficios
- Tests rápidos
- Tests gratuitos
- Tests reproducibles
- Cero dependencia de terceros

*(Normalmente se usa `unittest.mock` o librerías similares)*

---

### 📊 Coverage (cobertura de tests)

El *coverage* es una métrica porcentual que indica **qué parte de tu código fue ejecutada por los tests**.

- 80% de coverage → el 80% de las líneas se ejecutaron
- 20% nunca se probaron

#### ⚠️ Advertencia importante

> Un **100% de cobertura no garantiza cero bugs**  
> Pero un **10% de cobertura garantiza problemas futuros**

La cobertura es una **señal**, no un objetivo ciego.

#### 🧭 Buen criterio profesional
- Usa coverage para **detectar zonas sin tests**
- No sacrifiques calidad de tests solo por subir el porcentaje

---

### 🧠 Cierre conceptual

Los tests profesionales en BI y Data Science no buscan solo “que el código pase”.  
Buscan:

- 🔒 Proteger reglas de negocio
- 🔁 Garantizar reproducibilidad
- 🚀 Facilitar la evolución del proyecto

Fixtures, parametrización, mocking y coverage no son extras.  
Son parte del **kit básico de un/a profesional del dato**.
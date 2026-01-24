## 🧩 Testeando Clases y Manejo de Errores

Probar **funciones puras** (input → output) suele ser sencillo.  
Probar **clases**, en cambio, requiere una mirada más cuidadosa: las clases tienen **estado interno**, colaboran con otros objetos y evolucionan a lo largo de su ciclo de vida.

En esta sección veremos cómo testear:

- 🔁 Cambios de estado en objetos
- 🚨 Manejo explícito de errores (*unhappy path*)
- 🎭 Mocking más realista y explícito en clases

---

## 🔄 Testeando el ciclo de vida de un objeto

Supongamos que estamos modelando un **portafolio de inversión**.  
Una regla básica del negocio es:

> Al agregar una posición, el portafolio debe reflejar ese cambio en su estado interno.

---

### 🧠 Hipótesis de negocio

- Un portafolio vacío no tiene posiciones
- Al agregar una posición válida:
  - La lista de posiciones crece
  - El instrumento agregado es el esperado

---

### 🧪 Test de cambio de estado

```python
# test_portafolio.py

def test_agregar_posicion_cambia_estado(portafolio_vacio, posicion_aapl):
    # 1. Estado inicial
    assert len(portafolio_vacio.posiciones) == 0

    # 2. Acción
    portafolio_vacio.agregar_posicion(posicion_aapl)

    # 3. Verificación de estado
    assert len(portafolio_vacio.posiciones) == 1
    assert portafolio_vacio.posiciones[0].instrumento.ticker == "AAPL"
```

📌 **Idea clave**:  
No estamos probando *cómo* se guarda la posición internamente,  
estamos probando **el efecto observable del método**.

---

## 🚨 Testeando el "camino infeliz" (*Unhappy Path*)

Un sistema robusto no solo funciona cuando todo sale bien.  
Debe **fallar correctamente** cuando se usa mal.

En testing profesional:
- Un error esperado **es un test que pasa**
- Un error no controlado **es un bug**

---

### 🧠 Regla de negocio

> No se puede crear una posición con cantidad negativa o cero.

---

### 🏗️ Código productivo

```python
# models.py

class CantidadInvalidaError(ValueError):
    """Error lanzado cuando la cantidad no es válida."""
    pass


@dataclass
class Posicion:
    instrumento: object
    cantidad: int
    precio: float

    def __post_init__(self):
        if self.cantidad <= 0:
            raise CantidadInvalidaError("La cantidad debe ser positiva")
```

---

### 🧪 Test del error esperado

```python
# test_models.py

import pytest


def test_crear_posicion_negativa_lanza_error(instrumento_mock):
    # El test PASA si el código FALLA con el error correcto
    with pytest.raises(CantidadInvalidaError):
        Posicion(
            instrumento=instrumento_mock,
            cantidad=-10,
            precio=100
        )
```

📌 **Observa que**:
- No validamos el mensaje exacto
- Validamos el **tipo de error**
- El test documenta una **regla del negocio**

---

## 🎭 Mocking en clases: ejemplo explícito

Ya vimos el concepto de mocking.  
Ahora lo usamos de forma **concreta y explícita**.

Supongamos que `Instrumento` es una clase compleja:
- Consulta APIs externas
- Tiene muchas validaciones
- No queremos depender de ella en este test

---

### 🧠 Estrategia

Para testear `Posicion`, **no necesitamos un Instrumento real**.  
Solo necesitamos que tenga los atributos mínimos que el código usa.

---

### 🧪 Mock simple con `unittest.mock`

```python
from unittest.mock import Mock


def test_posicion_con_instrumento_mock():
    instrumento_mock = Mock()
    instrumento_mock.ticker = "AAPL"

    posicion = Posicion(
        instrumento=instrumento_mock,
        cantidad=10,
        precio=150
    )

    assert posicion.instrumento.ticker == "AAPL"
```

🎯 **Qué estamos probando realmente**:
- Que `Posicion` acepta un objeto con la interfaz esperada
- No dependemos de la implementación real de `Instrumento`

---

## 🧠 Comparación rápida: Fixture vs Mock

| Enfoque  | ¿Cuándo usarlo? |
|--------|----------------|
| Fixture | Cuando el objeto es simple y reutilizable |
| Mock    | Cuando el objeto es complejo, lento o externo |

En etapas tempranas, **fixtures suelen ser suficientes**.  
A medida que el sistema crece, el *mocking* se vuelve indispensable.

---

## 🧠 Idea clave para llevarte

> Testear clases no es testear atributos.  
> Es testear **comportamientos y cambios de estado**.

Y un buen manejo de errores:
- Documenta reglas
- Protege el dominio
- Hace el sistema más confiable

---

## 🚀 Siguiente paso natural

Después de esto, el camino lógico es:
- Mockear **APIs externas**
- Simular **fallos de servicios**
- Testear **flujos completos (integration tests)**

Pero eso ya es nivel *advanced*

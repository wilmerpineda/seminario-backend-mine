## 3.5 🧪 Taller Práctico: Blindando el SmartPortfolio (Tests + PR)

### 🎯 Objetivo
Implementar una suite de pruebas profesional para el proyecto **SmartPortfolio**, alcanzando:

- ✅ **≥ 90% de cobertura** en el módulo de modelos  
- ✅ Uso obligatorio de:
  - `pytest.fixture`
  - `@pytest.mark.parametrize`
  - `pytest.approx`
- ✅ Entrega mediante **Pull Request en GitHub**, siguiendo buenas prácticas de commits

---

## 🧰 Contexto del repositorio y flujo GitHub
Este taller simula un flujo real de trabajo en equipo:

- Desarrollo en una **rama feature**
- **Commits pequeños, claros y atómicos**
- Revisión mediante **Pull Request**
- Validación con **coverage** y evidencia reproducible

---

## 1) 🧱 Preparación del entorno

### 1.1 Crear rama de trabajo
```bash
git checkout main
git pull origin main
git checkout -b feat/test-suite
```

### 1.2 Instalar dependencias de testing
```bash
poetry add pytest pytest-cov --group dev
```

### 1.3 Estructura esperada
```text
tests/
  conftest.py
  test_models.py
```

---

## 2) 🧪 Desarrollo de tests

### A) 🛠️ Fixtures

Definan fixtures para reutilizar objetos del dominio.

**Requeridas:**
- `instrumento_test`: instrumento genérico (ej. TSLA, AAPL)
- `portafolio_vacio`: portafolio sin posiciones

```python
# tests/conftest.py
import pytest

@pytest.fixture
def instrumento_test():
    return Instrumento(ticker="TSLA", nombre="Tesla")

@pytest.fixture
def portafolio_vacio():
    return Portafolio()
```

---

### B) 🔄 Tests de lógica (parametrizados)

La clase `Posicion` debe implementar un método como  
`calcular_ganancia_no_realizada()`.

```python
# tests/test_models.py
import pytest

@pytest.mark.parametrize(
    "precio_entrada, precio_actual, cantidad, esperado",
    [
        (100, 150, 10, 500),
        (200, 180, 5, -100),
        (50, 50, 7, 0),
    ],
)
def test_calculo_pnl(
    precio_entrada,
    precio_actual,
    cantidad,
    esperado,
    instrumento_test,
):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=cantidad,
        precio_entrada=precio_entrada,
    )

    pnl = posicion.calcular_ganancia_no_realizada(
        precio_actual=precio_actual
    )

    assert pnl == pytest.approx(esperado)
```

---

### C) 🚨 Validación de errores (Unhappy Path)

Aseguren que `Portafolio` lance una excepción propia si se intenta
remover un activo inexistente.

```python
import pytest

def test_remover_activo_inexistente_lanza_error(portafolio_vacio):
    with pytest.raises(PosicionNoExisteError):
        portafolio_vacio.remover_posicion(ticker="NFLX")
```

---

## 3) 📊 Reporte de Coverage

### 3.1 Consola
```bash
poetry run pytest -v --cov=src --cov-report=term-missing
```

### 3.2 Reporte HTML
```bash
poetry run pytest --cov=src --cov-report=html
```

Abrir:
```text
htmlcov/index.html
```

Objetivo mínimo: **≥ 90% de cobertura en models**.

---

## 4) ✅ Commits y Pull Request

### Commits sugeridos
1. `test: add base fixtures for portfolio and instrument`
2. `test: add parametrized PnL scenarios`
3. `test: add unhappy path for missing position`
4. `chore: raise models coverage above 90%`

### Publicar rama
```bash
git push -u origin feat/test-suite
```

### Pull Request
**Título sugerido**  
`feat(test): add pytest suite and coverage for models`

El PR debe incluir:
- Archivos de test nuevos
- Captura de `pytest -v`
- Captura de `pytest --cov` con ≥ 90%

---

## ✅ Checklist de calidad

- [ ] Uso de `pytest.fixture`
- [ ] Uso de `parametrize`
- [ ] Uso de `pytest.approx`
- [ ] Test de error con `pytest.raises`
- [ ] Asserts claros y semánticos
- [ ] Commits claros y atómicos
- [ ] Coverage ≥ 90%

---

### 🧠 Cierre
Este taller evalúa algo más que código:  
evalúa **disciplina profesional en testing**, dominio del flujo GitHub
y capacidad de proteger reglas de negocio con evidencia reproducible.

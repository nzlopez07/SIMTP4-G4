# Capa Boundary — Cambios y Comunicación con Simulación

## Resumen de cambios

La carpeta `app/` fue renombrada a `boundary/` para reflejar con mayor claridad su rol dentro de la arquitectura: actúa exclusivamente como la **capa de presentación y entrada/salida** del sistema, sin lógica de negocio propia.

## Estructura de la capa boundary

```
boundary/
├── __init__.py                        ← Flask app factory
├── rutas/
│   └── main.py                        ← Blueprint "main" con todas las rutas
├── static/
│   └── styles.css                     ← Estilos globales
└── templates/
    ├── base.html                      ← Template base (navbar + footer)
    ├── pagina-inicio.html             ← Hereda base.html
    ├── formulario-simulacion.html     ← Hereda base.html
    └── resultados.html                ← Hereda base.html
```

## Rutas HTTP expuestas

| Método | URL | Función | Descripción |
|---|---|---|---|
| `GET` | `/` | `index()` | Renderiza la página de inicio |
| `GET` | `/formulario` | `simulacion_form()` | Renderiza el formulario de parámetros |
| `POST` | `/simulacion/ejecutar` | `simulacion_ejecutar()` | Recibe parámetros, ejecuta la simulación y renderiza resultados |
| `GET` | `/simulacion/resultados` | `simulacion_resultados()` | Placeholder — sin almacenamiento persistente, devuelve lista vacía |

---

## Comunicación: Boundary → Simulación

### Datos que llegan al boundary (formulario HTML)

El formulario en `formulario-simulacion.html` envía los siguientes campos por POST:

| Campo HTML (`name`) | Tipo | Valor por defecto | Descripción |
|---|---|---|---|
| `hora_inicio` | `text` (`HH:MM:SS`) | `09:00:00` | Hora de inicio de la simulación |
| `hora_fin` | `text` (`HH:MM:SS`) | `21:00:00` | Hora de cierre (puede superar las 24 hs, ej: `27:00:00`) |
| `seed` | `number` | *(vacío)* | Semilla para reproducibilidad (opcional) |

### Lo que la ruta envía a la simulación

En `boundary/rutas/main.py`, la función `simulacion_ejecutar()` extrae los campos del formulario y los pasa a la capa de simulación:

```python
hora_inicio = request.form.get("hora_inicio")   # str, ej: "09:00:00"
hora_fin    = request.form.get("hora_fin")       # str, ej: "21:00:00"
seed        = request.form.get("seed")           # str | None
```

Luego instancia el motor y construye una fila del vector de estado con esos parámetros:

```python
motor = MotorSimulacion()          # simulacion.motor.MotorSimulacion

fila = FilaVectorEstado()          # simulacion.estadisticas.FilaVectorEstado
fila.iteracion = 1
fila.hora_simulada = 0.0
fila.evento_simulado = "InicioSimulacion"
fila.agregar_variable_auxiliar("hora_inicio", hora_inicio)
fila.agregar_variable_auxiliar("hora_fin", hora_fin)
if seed:
    fila.agregar_rnd("seed", seed)

motor.agregar_fila_vector(fila)
```

---

## Comunicación: Simulación → Boundary

### Datos que devuelve la simulación

El motor expone el vector de estado a través de `motor.vector_estado.filas`, una lista de instancias de `FilaVectorEstado`. La ruta las serializa llamando al método `como_dict()` de cada fila antes de pasarlas al template:

```python
filas_serializables = [f.como_dict() for f in motor.vector_estado.filas]
return render_template("resultados.html", filas=filas_serializables)
```

### Estructura del dict devuelto por `FilaVectorEstado.como_dict()`

Cada fila del vector de estado se serializa con la siguiente forma:

```python
{
    "iteracion":           int,          # Número de iteración
    "hora_simulada":       float,        # Reloj de la simulación (en minutos)
    "evento_simulado":     str,          # Nombre del evento procesado
    "proximos_eventos":    list,         # Eventos futuros programados
    "objetos":             dict,         # Estado de los objetos del sistema
    "variables_auxiliares": dict,        # Variables auxiliares (parámetros, etc.)
    "rnd_usados":          dict,         # Números aleatorios consumidos en la iteración
}
```

#### Ejemplo concreto con los datos actuales

```json
{
    "iteracion": 1,
    "hora_simulada": 0.0,
    "evento_simulado": "InicioSimulacion",
    "proximos_eventos": [],
    "objetos": {},
    "variables_auxiliares": {
        "hora_inicio": "09:00:00",
        "hora_fin": "21:00:00"
    },
    "rnd_usados": {
        "seed": "42"
    }
}
```

### Qué hace el template con los datos

`resultados.html` recibe la variable `filas` (lista de dicts) y la itera para mostrar cada fila:

```html
{% for fila in filas %}
  Iteración {{ fila.iteracion }} — Hora {{ fila.hora_simulada }}
  {{ fila | tojson(indent=2) }}
{% endfor %}
```

---

## Flujo completo de una petición POST

```
Usuario completa el formulario y hace clic en "Ejecutar simulación"
        │
        ▼
[Navegador] POST /simulacion/ejecutar
    Body: hora_inicio=09:00:00 & hora_fin=21:00:00 & seed=42
        │
        ▼
[boundary/rutas/main.py] simulacion_ejecutar()
    ├── Extrae: hora_inicio, hora_fin, seed de request.form
    ├── Crea: MotorSimulacion()
    ├── Crea: FilaVectorEstado() con los parámetros
    ├── Llama: motor.agregar_fila_vector(fila)
    └── Serializa: [f.como_dict() for f in motor.vector_estado.filas]
        │
        ▼
[boundary/templates/resultados.html]
    Recibe: filas = [{"iteracion": 1, "hora_simulada": 0.0, ...}]
    Renderiza: lista de filas del vector de estado
        │
        ▼
[Navegador] Muestra los resultados al usuario
```

---

## Clases de simulación usadas por el boundary

| Clase | Módulo | Uso en boundary |
|---|---|---|
| `MotorSimulacion` | `simulacion.motor` | Se instancia en cada POST para ejecutar la simulación |
| `FilaVectorEstado` | `simulacion.estadisticas` | Se usa para construir filas del vector de estado |
| `RegistroEstadisticas` | `simulacion.estadisticas` | Importado (aún sin uso directo en las rutas) |

---

## Estado actual y limitaciones

- El motor aún **no ejecuta la simulación completa** (`ejecutar()` lanza `NotImplementedError`). La ruta construye una única fila de ejemplo con los parámetros del formulario.
- No hay **persistencia**: los resultados solo existen durante el ciclo de vida del request. La ruta `/simulacion/resultados` devuelve siempre una lista vacía.
- Los parámetros `hora_inicio` y `hora_fin` llegan como `str` al motor; la conversión a minutos (o `datetime`) deberá realizarse dentro de `MotorSimulacion.ejecutar()` cuando se implemente.

# TP 4 Simulación "Eco-Clean"

Simulación de eventos discretos del lavadero "Eco-Clean":

- Horario: 09:00 a 21:00 (720 minutos). Al llegar las 21:00 se dejan de recibir autos, pero se terminan los que ya están en cola o en aspirado.
- Un único túnel de lavado (10–15 min, distribución uniforme).
- Cola del túnel: máximo 5 vehículos. El que llega con la cola llena se retira (cliente perdido).
- El 20 % de los autos que salen del túnel pasan a uno de los 2 puestos de aspirado.
- Aspirado: distribución exponencial negativa con media 20 min (3 aspirados cada 60 min → media = 60/3 = 20 min).
- Si los 2 puestos de aspirado están ocupados y el túnel termina un auto que requiere aspirado → túnel BLOQUEADO hasta que se libere un puesto.

### Métricas a calcular

- Cantidad de clientes perdidos por capacidad de cola.
- Porcentaje de tiempo que el túnel estuvo bloqueado.
- Tiempo promedio de horas extras (minutos trabajados después de las 21:00).

### Variables Aleatorias

| Variable | Distribución | Fórmula |
|---|---|---|
| Tiempo entre llegadas | Exponencial (media = 12 min) | `T = -12 * ln(RND)` |
| Tiempo de lavado | Uniforme (10–15 min) | `T = 10 + 5 * RND` |
| ¿Requiere aspirado? | Probabilidad (p = 0.20) | `Si RND ≤ 0.20 → requiere aspirado` |
| Tiempo de aspirado | Exponencial (media = 20 min) | `T = -20 * ln(RND)` |

## Arquitectura

```text
Frontend (HTML/CSS/JS)
        ↓
Flask
        ↓
MotorSimulacion
        ↓
Eventos / Objetos / Estadísticas / Randoms
```

La lógica principal del sistema se encuentra completamente desacoplada de la interfaz web.

Flask solamente:

- recibe parámetros;
- inicia la simulación;
- obtiene resultados;
- renderiza la información.

Toda la lógica de simulación se concentra en el MotorSimulacion.

### Uso de Flask

Se utilizará Flask como framework backend debido a:

- simplicidad;
- bajo nivel de complejidad;
- facilidad de integración con HTML;
- facilidad para dividir tareas entre integrantes;
- rapidez de desarrollo;
- buena separación entre interfaz y lógica.


## Diagrama de Clases

```
GeneradorAleatorio
    + generar_uniforme() → float
    + generar_exponencial(media) → float
    + generar_uniforme_entre(a, b) → float

Auto
    + id: int
    + estado: str          # En cola | En lavado | Esperando aspirado | En aspirado | Finalizado | Retirado
    + requiere_aspirado: bool
    + hora_llegada: float

ColaLavado
    + autos: deque
    + capacidad_max: int = 5
    + esta_llena() → bool
    + encolar(auto) → None
    + desencolar() → Auto

TunelLavado
    + estado: str          # Libre | Ocupado | Bloqueado
    + auto_actual: Auto | None
    + esta_libre() → bool
    + esta_bloqueado() → bool

PuestoAspirado
    + id: int
    + estado: str          # Libre | Ocupado
    + auto_actual: Auto | None
    + esta_libre() → bool

RegistroEstadisticas
    + clientes_perdidos: int
    + tiempo_bloqueado: float
    + tiempo_inicio_bloqueo: float | None
    + tiempo_fin_simulacion: float
    + registrar_perdida() → None
    + iniciar_bloqueo(tiempo) → None
    + finalizar_bloqueo(tiempo) → None
    + calcular_metricas() → dict

CalendarioEventos
    + _heap: list
    + agregar_evento(evento) → None
    + obtener_proximo() → Evento
    + esta_vacio() → bool

VectorEstado
    + filas: list[dict]
    + agregar_fila(snapshot) → None
    + obtener_rango(hora_inicio, cantidad) → list[dict]
    + obtener_ultima_fila() → dict

MotorSimulacion
    + reloj: float
    + generador: GeneradorAleatorio
    + calendario: CalendarioEventos
    + cola_lavado: ColaLavado
    + tunel: TunelLavado
    + puestos_aspirado: list[PuestoAspirado]
    + estadisticas: RegistroEstadisticas
    + vector_estado: VectorEstado
    + autos: dict[int, Auto]
    + contador_autos: int
    + simular(tiempo_max, max_iteraciones) → VectorEstado

Evento (abstracta)
    + tiempo: float
    + tipo: str
    + procesar(motor) → None       # Template Method
    # _validar(motor)              # Hook
    # _ejecutar(motor)             # Abstracto
    # _generar_eventos(motor)      # Abstracto
    # _actualizar_stats(motor)     # Hook

EventoLlegada(Evento)
EventoFinLavado(Evento)
EventoFinAspirado(Evento)
```

---

## Estructura de Archivos

```
SIMTP4-G4/
│
├── app/
│   ├── __init__.py
│   ├── rutas/
│   │   └── main.py                    ← Rutas Flask 
│   ├── templates/
│   │   ├── index.html                 ← Formulario de parámetros 
│   │   ├── simulacion.html            ← Vector de estado 
│   │   └── resultados.html            ← Métricas finales 
│   └── static/
│       └── styles.css
│
├── simulacion/
│   ├── __init__.py
│   ├── randoms/
│   │   ├── __init__.py
│   │   └── generador_aleatorio.py 
│   ├── objetos/
│   │   ├── __init__.py
│   │   ├── auto.py                
│   │   ├── cola_lavado.py         
│   │   ├── tunel_lavado.py        
│   │   └── puesto_aspirado.py     
│   ├── eventos/
│   │   ├── __init__.py
│   │   ├── evento.py               (clase base abstracta)
│   │   ├── evento_llegada.py      
│   │   ├── evento_fin_lavado.py   
│   │   └── evento_fin_aspirado.py 
│   ├── estadisticas/
│   │   ├── __init__.py
│   │   ├── registro_estadisticas.py 
│   │   └── vector_estado.py 
│   └── motor/
│       ├── __init__.py
│       ├── calendario_eventos.py  
│       └── motor_simulacion.py    
│
├── tests/
│   └── test_imports.py
│
├── documentacion/
│   ├── propuesta.md
│
├── main.py
├── run.ps1
└── run.sh
```

## Patrón Template Method

El patrón **Template Method** se aplica a la jerarquía de eventos.

La clase abstracta `Evento` define el **esqueleto del algoritmo** en su método `procesar()`, el cual llama en orden a pasos que las subclases concretas deben o pueden implementar.

```
Evento (abstracta)
│
├── procesar(motor)          ← Template Method: define el esqueleto
│     ├── _validar(motor)          ← Hook: override opcional
│     ├── _ejecutar(motor)         ← Abstracto: DEBE implementarse
│     ├── _generar_eventos(motor)  ← Abstracto: DEBE implementarse
│     └── _actualizar_stats(motor) ← Hook: override opcional
│
├── EventoLlegada
├── EventoFinLavado
└── EventoFinAspirado
```

### Esquema de código de la clase base

```python
from abc import ABC, abstractmethod

class Evento(ABC):
    def __init__(self, tiempo: float, tipo: str):
        self.tiempo = tiempo
        self.tipo = tipo

    # Template Method — NO se sobreescribe en subclases
    def procesar(self, motor):
        self._validar(motor)
        self._ejecutar(motor)
        self._generar_eventos(motor)
        self._actualizar_stats(motor)

    # Hook — override opcional
    def _validar(self, motor):
        pass

    # Paso abstracto — obligatorio en cada subclase
    @abstractmethod
    def _ejecutar(self, motor):
        pass

    # Paso abstracto — obligatorio en cada subclase
    @abstractmethod
    def _generar_eventos(self, motor):
        pass

    # Hook — override opcional
    def _actualizar_stats(self, motor):
        pass

    def __lt__(self, otro):
        return self.tiempo < otro.tiempo
```

## Consideraciones

### Parametrizables
- Media de llegadas: 12 min.
- Tiempo mínimo de lavado: 10 min.
- Tiempo máximo de lavado: 15 min.
- Capacidad de la cola: 5 vehículos.
- Probabilidad de aspirado: 20 %.
- Media de aspirado: 20 min (derivada de 3 aspirados/60 min).
- Cantidad de puestos de aspirado: 2.

### Manejo de horas extras
Al llegar `reloj >= 720`:
- No se programan nuevas llegadas.
- Se siguen ejecutando `EventoFinLavado` y `EventoFinAspirado` hasta vaciar el sistema.
- `tiempo_fin_simulacion` = `reloj` del último evento ejecutado.
- `horas_extras = max(0, tiempo_fin_simulacion - 720)` minutos.

### Reproducibilidad
El `GeneradorAleatorio` acepta una semilla opcional. Si se ingresa la misma semilla, la simulación produce exactamente los mismos resultados.

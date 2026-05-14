# Arquitectura Propuesta — TP 4 Simulación "Eco-Clean"

## Objetivo del Sistema

El sistema tiene como objetivo simular el funcionamiento del lavadero de autos "Eco-Clean" mediante una simulación de eventos discretos.

La aplicación deberá:

- Simular el comportamiento del sistema.
- Controlar eventos y tiempos.
- Mostrar el vector de estado.
- Calcular métricas estadísticas.
- Permitir la visualización de resultados mediante una interfaz web.
---

# Arquitectura General

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

---

# Decisiones Arquitectónicas

## Uso de Flask

Se utilizará Flask como framework backend debido a:

- simplicidad;
- bajo nivel de complejidad;
- facilidad de integración con HTML;
- facilidad para dividir tareas entre integrantes;
- rapidez de desarrollo;
- buena separación entre interfaz y lógica.

---

## No utilización de Base de Datos

No se utilizará una base de datos debido a que:

- la simulación es temporal;
- no existe persistencia necesaria;
- los resultados viven únicamente durante la ejecución;
- no existen múltiples usuarios concurrentes;
- todos los datos pueden mantenerse en memoria.
 
---

## Separación de Responsabilidades

Se busca una arquitectura modular donde cada componente tenga una única responsabilidad.

Esto permite:

- mejor mantenimiento;
- trabajo paralelo entre integrantes;
- menor acoplamiento;
- mayor claridad conceptual;
- facilidad de testing.

---

# Componentes Principales

# MotorSimulacion

Es el núcleo principal del sistema.

Responsabilidades:

- controlar el reloj de simulación;
- ejecutar eventos;
- avanzar el tiempo;
- controlar iteraciones;
- gestionar finalización;
- mantener el estado general;
- generar filas del vector de estado.

Conceptualmente:

```text
Es quien dirige toda la simulación.
```

---

# GeneradorAleatorio

Componente encargado de centralizar toda la generación de números aleatorios.

El GeneradorAleatorio será creado externamente al iniciar la simulación y luego será inyectado dentro del MotorSimulacion como una dependencia.

Conceptualmente:
MotorSimulacion
└── GeneradorAleatorio

Esto permite que toda la simulación utilice un único stream aleatorio compartido.

Responsabilidades:

- generar RNDs;
- controlar semillas;
- generar distribuciones;
- permitir reproducibilidad;
- facilitar testing.

Funciones posibles:
```
generar_uniforme()

generar_exponencial(media)

generar_uniforme_entre(a, b)
```
Ventajas:

- evita randoms dispersos por el código;
- facilita depuración;
- mejora trazabilidad;
- permite simulaciones reproducibles.

Los eventos no deberán generar números aleatorios directamente. Toda generación aleatoria deberá realizarse mediante el GeneradorAleatorio contenido dentro del MotorSimulacion.

---

# Auto

Entidad dinámica principal del sistema.

Representa un vehículo dentro de la simulación.

Atributos posibles:

```python
id
estado
requiere_aspirado
hora_llegada
```

Estados posibles:

```text
En cola
En lavado
Esperando aspirado
En aspirado
Finalizado
Retirado
```

---

# Evento

Clase base utilizada para representar sucesos que ocurren en un instante determinado.

Atributos:

```python
tiempo
tipo
```

Método principal:

```python
procesar()
```

Cada evento modifica el estado del sistema y puede generar nuevos eventos.

---

# Eventos Específicos

## EventoLlegada

Responsabilidades:

- crear auto;
- verificar cola;
- iniciar lavado o encolar;
- programar próxima llegada.

---

## EventoFinLavado

Responsabilidades:

- finalizar lavado;
- decidir si requiere aspirado;
- bloquear túnel si corresponde;
- iniciar siguiente lavado.

---

## EventoFinAspirado

Responsabilidades:

- liberar aspiradora;
- desbloquear túnel si corresponde;
- finalizar vehículo.

---

# ColaLavado

Representa la cola del túnel de lavado.

Características:

- política FIFO;
- capacidad máxima de 5 vehículos.

Responsabilidades:

- almacenar autos esperando;
- controlar capacidad;
- administrar orden de atención.

---

# TunelLavado

Representa el túnel principal de lavado.

Estados posibles:

```text
Libre
Ocupado
Bloqueado
```

Responsabilidades:

- lavar vehículos;
- controlar bloqueos;
- liberar o retener autos.

---

# PuestoAspirado

Representa cada puesto de aspirado manual.

Estados:

```text
Libre
Ocupado
```

Responsabilidades:

- aspirar vehículos;
- liberar recursos al finalizar.

---

# RegistroEstadisticas

Componente encargado de almacenar métricas y acumuladores.

Responsabilidades:

- clientes perdidos;
- tiempo bloqueado;
- horas extras;
- acumuladores;
- métricas finales.

Ventaja:

Permite separar cálculos estadísticos del motor principal.

---

# Funcionamiento General de la Simulación

## Paso 1

El MotorSimulacion:

- inicializa reloj;
- crea primera llegada;
- inicializa recursos.

---

## Paso 2

Se obtiene el próximo evento a ejecutar.

---

## Paso 3

El reloj avanza hasta el tiempo del evento.

---

## Paso 4

El evento procesa cambios en el sistema.

Puede:

- modificar estados;
- mover vehículos;
- generar nuevos eventos;
- actualizar estadísticas.

---

## Paso 5

El proceso continúa hasta:

- alcanzar el tiempo máximo X;
- o alcanzar 100000 iteraciones.

---

# Calendario de Eventos

Se utilizará un componente encargado de almacenar eventos futuros ordenados temporalmente.
(Acá podríamos implementarlo usando heapq de Python, si no me equivoco es una librería nativa, ya te resuelve el hacer el ordenamiento)
Conceptualmente:

```text
CalendarioEventos
```

Posibles funciones:
```text
agregar_evento(evento) (autoexplicativo xd)
obtener_proximo() (Mirar la cola para saber si hay algo)
esta_vacio() (autoexplicativo xd)
```
Internamente podrá implementarse utilizando una cola prioritaria.

Objetivo:

- obtener siempre el próximo evento cronológicamente.

---

# Estructura de Carpetas

```text
proyecto/
│
├── app/
│   ├── rutas/
│   ├── templates/
│   ├── static/
│
├── simulacion/
│   ├── motor/
│   ├── eventos/
│   ├── objetos/
│   ├── randoms/
│   ├── estadisticas/
│
├── tests/
│
├── main.py
```

---

# Consideraciones Importantes

## Separación entre Estado y Visualización

El estado interno del sistema no debe depender del vector visual mostrado al usuario.

El motor debe:

- mantener el estado real;
- generar snapshots;
- convertir snapshots en filas visuales.

---

# Conclusión

El foco principal del sistema se encuentra en el modelado correcto de:

- eventos;
- estados;
- recursos;
- colas;
- métricas;
- comportamiento temporal.

La interfaz web actúa únicamente como mecanismo de interacción y visualización, mientras que toda la lógica de simulación se concentra en el MotorSimulacion y sus componentes asociados.
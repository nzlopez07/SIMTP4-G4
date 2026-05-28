# Modulo de estadisticas

## Objetivo

El modulo de estadisticas se encarga de registrar y calcular las metricas finales pedidas por el enunciado del lavadero Eco-Clean.

Las tres metricas principales son:

- Cantidad de clientes perdidos por capacidad de cola.
- Porcentaje de tiempo que el tunel estuvo bloqueado por el sector de aspirado.
- Tiempo promedio de horas extras trabajadas despues de las 21:00.

Ademas, el modulo prepara los datos del vector de estado para que puedan mostrarse correctamente en la interfaz web.

## Archivos involucrados

El modulo se encuentra principalmente en:

- `simulacion/estadisticas/registro_estadisticas.py`
- `simulacion/estadisticas/vector_estado.py`

Tambien se integra con los eventos de la simulacion:

- `simulacion/eventos/evento_llegada.py`
- `simulacion/eventos/evento_fin_lavado.py`
- `simulacion/eventos/evento_fin_aspirado.py`
- `simulacion/eventos/evento_inicializacion.py`
- `simulacion/eventos/evento_nuevo_dia.py`

## RegistroEstadisticas

La clase `RegistroEstadisticas` concentra los acumuladores estadisticos de la simulacion.

Sus responsabilidades son:

- Registrar clientes perdidos.
- Registrar el inicio de un bloqueo del tunel.
- Registrar el fin de un bloqueo del tunel.
- Acumular el tiempo total de tunel bloqueado.
- Calcular horas extras.
- Contar jornadas simuladas.
- Calcular las metricas finales del enunciado.

### Clientes perdidos

Cuando llega un auto y la cola de lavado esta llena, el cliente se retira.

En ese caso se llama a:

```python
registrar_cliente_perdido(fila)
```

Esto incrementa el contador de clientes perdidos y deja el valor actualizado en la fila actual del vector de estado.

La metrica final se informa como:

```text
clientes_perdidos_por_capacidad
```

## Porcentaje de tunel bloqueado

El enunciado pide porcentaje de tiempo que el tunel estuvo bloqueado por el sector de aspirado.

El tunel queda bloqueado cuando:

1. Termina un lavado.
2. El auto requiere aspirado.
3. Los dos puestos de aspirado estan ocupados.

En ese momento se registra el inicio del bloqueo:

```python
iniciar_bloqueo_tunel(tiempo_inicio, fila)
```

Cuando termina un aspirado y se libera un puesto, el auto bloqueado puede pasar a aspirado. Ahi se registra el fin del bloqueo:

```python
finalizar_bloqueo_tunel(tiempo_fin, fila)
```

La duracion del bloqueo se calcula como:

```text
duracion_bloqueo = tiempo_fin_bloqueo - tiempo_inicio_bloqueo
```

El porcentaje final se calcula asi:

```text
porcentaje_tunel_bloqueado =
    tiempo_tunel_bloqueado / tiempo_total_simulacion * 100
```

Ejemplo:

```text
tiempo_total_simulacion = 720 min
tiempo_tunel_bloqueado = 36 min

porcentaje = 36 / 720 * 100 = 5%
```

Por eso, en tunel no se calcula un promedio. Se calcula un porcentaje, tal como pide el enunciado.

## Horas extras

El lavadero atiende de 09:00 a 21:00. Al llegar las 21:00 deja de recibir autos, pero debe terminar de atender los autos que quedaron dentro del sistema.

Si la simulacion termina despues de las 21:00, se generan horas extras.

El tiempo de horas extras de una jornada se calcula como:

```text
horas_extras = tiempo_fin_simulacion - 21:00
```

Si la simulacion termina antes o justo a las 21:00:

```text
horas_extras = 0
```

Como el enunciado pide tiempo promedio de horas extras, el modulo calcula:

```text
promedio_horas_extras =
    tiempo_total_horas_extras / cantidad_jornadas
```

Ejemplo:

```text
tiempo_total_horas_extras = 90 min
cantidad_jornadas = 3

promedio_horas_extras = 90 / 3 = 30 min
```

La pantalla de resultados muestra este valor como:

```text
Prom. horas extras
```

## FilaVectorEstado

La clase `FilaVectorEstado` representa una fila del vector de estado de la simulacion.

Guarda datos como:

- Numero de iteracion.
- Hora simulada.
- Evento simulado.
- Numeros aleatorios usados.
- Proximos tiempos de llegada, lavado y aspirado.
- Autos totales.
- Cantidad de autos en cola.
- Clientes perdidos.
- Tiempo acumulado de horas extras.
- Tiempo acumulado de tunel bloqueado.
- Estado del tunel.
- Estado de los puestos de aspirado.

## Serializacion para la interfaz

El metodo:

```python
como_dict()
```

convierte la fila a un diccionario simple para que Flask pueda mandarla al template HTML.

Los `datetime` se muestran como hora:

```text
HH:MM:SS
```

Los `timedelta` estadisticos se muestran en minutos.

Ejemplo:

```text
timedelta(minutes=15) -> 15
timedelta(minutes=10, seconds=30) -> 10.5
```

Esto facilita comparar los resultados con las formulas del enunciado.

## Integracion con eventos

El modulo de estadisticas no ejecuta la simulacion por si solo. Los eventos le informan cuando ocurre algo relevante.

### EventoLlegada

Si la cola esta llena:

```python
motor.registro.registrar_cliente_perdido(fila_actual)
```

### EventoFinLavado

Si el auto requiere aspirado y no hay puestos disponibles:

```python
motor.registro.iniciar_bloqueo_tunel(tiempo, fila_actual)
```

### EventoFinAspirado

Si habia un auto bloqueando el tunel y se libera un puesto:

```python
motor.registro.finalizar_bloqueo_tunel(tiempo, fila_actual)
```

### EventoInicializacion y EventoNuevoDia

Registran las jornadas simuladas:

```python
motor.registro.registrar_jornada(tiempo)
```

Esto permite calcular correctamente el promedio de horas extras.

## Metricas finales

El metodo principal para obtener los resultados es:

```python
calcular_metricas_finales(fila, tiempo_inicio)
```

Devuelve un diccionario con:

```python
{
    "clientes_perdidos_por_capacidad": ...,
    "porcentaje_tiempo_tunel_bloqueado": ...,
    "tiempo_horas_extras": ...,
    "tiempo_horas_extras_minutos": ...,
    "tiempo_promedio_horas_extras": ...,
    "tiempo_promedio_horas_extras_minutos": ...,
    "cantidad_jornadas": ...,
}
```

## Pruebas realizadas

Se agregaron pruebas para validar:

- Que los acumuladores estadisticos inicien en cero.
- Que los tiempos se serialicen en minutos.
- Que las metricas finales coincidan con las formulas del enunciado.
- Que el promedio de horas extras se calcule por jornada.

Comando usado:

```bash
python -m pytest tests -q -p no:cacheprovider
```

Resultado:

```text
7 passed
```

## Resumen

La parte de estadisticas permite justificar los resultados finales de la simulacion.

En particular:

- Clientes perdidos se calcula como contador acumulado.
- Tunel bloqueado se calcula como porcentaje del tiempo total simulado.
- Horas extras se calcula como promedio por jornada.
- El vector de estado se serializa en un formato facil de mostrar y verificar.

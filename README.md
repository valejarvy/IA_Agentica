# Sistema de IA Agentica

## Que es IA agentica

La IA agentica organiza una tarea en agentes con responsabilidades diferentes. Cada agente recibe informacion, toma una accion dentro de su rol y entrega un resultado al siguiente agente.

## Objetivo del proyecto

Este proyecto muestra un flujo academico sencillo para convertir una idea de programa en requisitos, diseno, codigo y pruebas. El ejemplo generado administra registros con calificaciones y calcula promedios. La idea del usuario se conserva como objetivo del analisis.

## Agentes

| Agente | Funcion | Skills utilizadas |
|---|---|---|
| Analista | Analizar el problema | analizar_requisitos, disenar_programa |
| Programador | Crear el codigo | disenar_programa, generar_codigo |
| Tester | Comprobar el codigo | realizar_pruebas |

Los tres documentos de definicion estan en `agentes/`. `main.py` los carga y comprueba antes de iniciar el flujo.

## Skills

Las cuatro skills tienen un archivo independiente en `skills/`:

- `analizar_requisitos`: obtiene objetivo, entradas, procesos, salidas y reglas.
- `disenar_programa`: propone la clase, funciones y archivo del programa.
- `generar_codigo`: establece reglas para crear codigo sencillo y validado.
- `realizar_pruebas`: define casos normales, incorrectos y limite, e informa resultados.

## Flujo de trabajo

```text
Usuario -> AnalistaAgente -> analizar_requisitos -> disenar_programa
        -> ProgramadorAgente -> generar_codigo
        -> TesterAgente -> realizar_pruebas -> resultado final
```

Si una prueba falla, `TesterAgente` informa el problema a `ProgramadorAgente`. Este regenera una version corregida y `TesterAgente` vuelve a probarla.

## Como ejecutar

Se necesita Python 3. No hay paquetes externos: `requirements.txt` documenta que solo se usa la biblioteca estandar.

Desde la carpeta `sistema_ia_agentica`, ejecute:

```powershell
python main.py --idea "Quiero un programa para registrar estudiantes y calcular su promedio"
```

Tambien puede ejecutar `python main.py` y escribir la idea cuando se solicite.

Para observar el ciclo de correccion de forma intencional:

```powershell
python main.py --idea "Registrar estudiantes" --simular-error
```

El programa generado queda en `salida/programa_generado.py`.

## Ejemplo de uso

```text
REQUISITOS PRODUCIDOS POR AnalistaAgente
- Objetivo: Quiero un programa para registrar estudiantes y calcular su promedio

ProgramadorAgente genero: salida/programa_generado.py
- Calculo normal: APROBADA
- Entrada incorrecta: nombre vacio: APROBADA
- Caso limite invalido: nota mayor a 100: APROBADA
- Caso limite valido: notas 0 y 100: APROBADA

RESULTADO FINAL: Programa aprobado.
```

## Por que es un sistema multiagente

El sistema tiene tres roles independientes: analisis, programacion y pruebas. Cada uno carga su propia definicion y skills desde archivos fisicos distintos, produce una salida para otro agente y participa en una iteracion de correccion cuando el tester detecta un error. Por eso no es un unico proceso que realiza todas las tareas sin separacion de responsabilidades.

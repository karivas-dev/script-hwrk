# Analizador educativo de logs

## Descripción

Este proyecto contiene un analizador educativo de archivos de registros (`.txt`)
desarrollado en Python 3. El programa permite seleccionar un archivo mediante
`tkinter.filedialog`, analiza sus líneas y muestra estadísticas y detalles de
los errores en la consola.

El analizador reconoce los niveles `INFO`, `WARNING` y `ERROR`. También valida
las fechas con el formato `YYYY-MM-DD` usando `datetime` y detecta:

- Registros incompletos.
- Fechas inválidas o con formato incorrecto.
- Niveles desconocidos.
- Líneas vacías o mal formateadas.

## Archivos del proyecto

- [`analizador_logs.py`](./analizador_logs.py): script principal.
- [`ejemplo_logs.txt`](./ejemplo_logs.txt): archivo de ejemplo con registros
  válidos y diferentes errores.
- [`prueba_logs_validos.txt`](./prueba_logs_validos.txt): archivo de prueba
  completamente bien formado.

## Requisitos y ejecución

- Python 3.
- Módulo `tkinter` disponible en la instalación de Python. No se utilizan
  dependencias externas instalables mediante `pip`.

Para ejecutar el programa:

```bash
python analizador_logs.py
```

Se abrirá un selector de archivos. Seleccione un archivo `.txt` para iniciar
el análisis.

## Reflexión técnica

### Uso de inteligencia artificial

La inteligencia artificial apoyó la estructura inicial del programa y sugirió
la separación en funciones: selección del archivo, lectura, validación de
fechas, análisis de líneas, generación de estadísticas y presentación del
reporte. También ayudó a proponer expresiones regulares para reconocer el
nivel y la fecha, y casos de prueba para comprobar registros válidos e
incorrectos.

La IA fue utilizada como apoyo para revisar la lógica y detectar casos límite,
pero el código fue revisado y adaptado para cumplir los requisitos de la
entrega.

### Decisiones del estudiante

El estudiante decidió:

- Mantener el proyecto sin clases y sin dependencias externas.
- Considerar un evento identificado cuando su nivel pertenece a los niveles
  permitidos, aunque el registro tenga otros errores.
- Contabilizar por separado las fechas inválidas y las líneas incompletas o
  mal formateadas.
- Conservar la información parcial de un registro incorrecto para mostrar
  mensajes de error más útiles.
- Mostrar el número de línea y el texto original en el detalle del reporte.

### Ejemplo de una sugerencia mejorable de la IA

Una primera propuesta podía contar únicamente las líneas completamente válidas
como eventos. Esa interpretación habría ocultado registros con un nivel
reconocido pero con una fecha inválida o un mensaje ausente.

El estudiante detectó el problema al comparar el conteo con el archivo de
ejemplo. La lógica se corrigió separando dos conceptos: `eventos_identificados`
se incrementa cuando el nivel es reconocido, mientras que
`registros_validos` solo se incrementa cuando el nivel, la fecha y el mensaje
son correctos.

Esto permitió obtener estadísticas más precisas y conservar el detalle de los
errores sin perder información útil del registro.

### Aprendizaje

La IA resulta útil para proponer estructuras, ejemplos y verificaciones, pero
sus sugerencias deben contrastarse con los requisitos y con resultados
observables. El estudiante debe comprender las decisiones del código, probar
los casos límite y corregir interpretaciones que no coincidan con el
comportamiento esperado. En este proyecto, la IA funcionó como una herramienta
de apoyo y revisión, no como reemplazo del razonamiento ni de la validación del
estudiante.

## Evidencia de pruebas

### 1. Archivo bien formado

Archivo: [`prueba_logs_validos.txt`](./prueba_logs_validos.txt)

Contiene cinco registros con niveles permitidos, fechas existentes en formato
`YYYY-MM-DD` y mensajes no vacíos:

```text
[INFO] 2025-01-10 User logged in
[WARNING] 2025-02-15 Multiple login attempts
[ERROR] 2025-03-20 Database unavailable
[INFO] 2025-04-01 Report generated
[ERROR] 2025-05-05 Backup failed
```

Resultados esperados y obtenidos:

- Líneas analizadas: `5`.
- Eventos identificados: `5`.
- Fechas inválidas: `0`.
- Líneas incompletas o mal formateadas: `0`.
- Registros válidos: `5`.
- Porcentaje de registros válidos: `100.00%`.

### 2. Archivo con errores e inconsistencias

Archivo: [`ejemplo_logs.txt`](./ejemplo_logs.txt)

Incluye una línea sin fecha, fechas inexistentes, una línea sin nivel, niveles
desconocidos, una línea vacía y un registro sin mensaje.

Resultados esperados y obtenidos:

| Métrica | Resultado |
|---|---:|
| Líneas analizadas | 18 |
| Eventos identificados | 14 |
| Eventos `INFO` | 5 |
| Eventos `WARNING` | 4 |
| Eventos `ERROR` | 5 |
| Fechas inválidas | 4 |
| Líneas incompletas o mal formateadas | 10 |
| Registros válidos | 8 |
| Porcentaje de registros válidos | 44.44% |

Además de las estadísticas, el programa muestra el número de cada línea
incorrecta, sus motivos y el texto original.

### Comando de validación

Desde la carpeta del proyecto se puede comprobar la sintaxis con:

```bash
python -m py_compile analizador_logs.py
```

La lógica de análisis también puede verificarse con:

```bash
python -c "import analizador_logs as a; r=a.analizar_lineas(a.leer_archivo('ejemplo_logs.txt')); print(a.generar_estadisticas(r))"
```


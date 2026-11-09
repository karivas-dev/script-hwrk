"""Analizador educativo de archivos de registros.

El programa no usa clases ni dependencias externas. Analiza cada línea de un
archivo, conserva la información parcial encontrada y muestra un resumen.
"""

import re
from datetime import datetime
from tkinter import Tk, filedialog


NIVELES_VALIDOS = ("INFO", "WARNING", "ERROR")


def seleccionar_archivo():
    """Abre un cuadro de diálogo y devuelve la ruta del archivo elegido."""
    ventana = Tk()
    ventana.withdraw()
    try:
        return filedialog.askopenfilename(
            title="Seleccione el archivo de logs",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
    finally:
        ventana.destroy()


def leer_archivo(ruta):
    """Lee un archivo línea por línea y devuelve sus líneas sin saltos finales."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return [linea.rstrip("\r\n") for linea in archivo]
    except FileNotFoundError:
        print(f"Error: no existe el archivo '{ruta}'.")
    except (OSError, UnicodeError) as error:
        print(f"Error al leer el archivo: {error}")
    return None


def validar_fecha(fecha):
    """Devuelve True solo si la fecha tiene formato ISO y existe en el calendario."""
    if not fecha or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fecha):
        return False
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def analizar_linea(linea, numero):
    """Analiza una línea y devuelve un diccionario con sus datos y errores."""
    resultado = {
        "numero": numero,
        "texto": linea,
        "nivel": None,
        "fecha": None,
        "mensaje": "",
        "nivel_reconocido": False,
        "fecha_valida": False,
        "valido": False,
        "errores": [],
    }
    texto = linea.strip()

    if not texto:
        resultado["errores"].append("línea vacía")
        return resultado

    coincidencia = re.match(r"^\[([^\]]+)\]\s*(.*)$", texto)
    if not coincidencia:
        resultado["errores"].append("falta el nivel entre corchetes")
        return resultado

    resultado["nivel"] = coincidencia.group(1).upper()
    resultado["nivel_reconocido"] = resultado["nivel"] in NIVELES_VALIDOS
    if not resultado["nivel_reconocido"]:
        resultado["errores"].append(
            f"nivel desconocido: {coincidencia.group(1)}"
        )

    resto = coincidencia.group(2).strip()
    partes = resto.split(maxsplit=1)
    if partes and re.match(r"^\d{4}", partes[0]):
        resultado["fecha"] = partes[0]
        resultado["mensaje"] = partes[1].strip() if len(partes) > 1 else ""
    else:
        resultado["mensaje"] = resto

    if resultado["fecha"] is None:
        resultado["errores"].append("falta la fecha")
    elif validar_fecha(resultado["fecha"]):
        resultado["fecha_valida"] = True
    else:
        resultado["errores"].append(
            f"fecha inválida o con formato incorrecto: {resultado['fecha']}"
        )

    if not resultado["mensaje"]:
        resultado["errores"].append("falta el mensaje")

    resultado["valido"] = not resultado["errores"]
    return resultado


def analizar_lineas(lineas):
    """Analiza todas las líneas y devuelve una lista de resultados."""
    return [analizar_linea(linea, numero)
            for numero, linea in enumerate(lineas, start=1)]


def generar_estadisticas(resultados):
    """Calcula las estadísticas principales a partir de los resultados."""
    estadisticas = {
        "total_lineas": len(resultados),
        "eventos_identificados": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "fechas_invalidas": 0,
        "incompletas_o_mal_formateadas": 0,
        "registros_validos": 0,
    }

    for resultado in resultados:
        if resultado["nivel_reconocido"]:
            estadisticas["eventos_identificados"] += 1
            estadisticas[resultado["nivel"]] += 1
        if resultado["fecha"] is not None and not resultado["fecha_valida"]:
            estadisticas["fechas_invalidas"] += 1
        if resultado["valido"]:
            estadisticas["registros_validos"] += 1
        else:
            estadisticas["incompletas_o_mal_formateadas"] += 1

    total = estadisticas["total_lineas"]
    estadisticas["porcentaje_validos"] = (
        estadisticas["registros_validos"] * 100 / total if total else 0
    )
    return estadisticas


def mostrar_reporte(nombre_archivo, resultados, estadisticas):
    """Muestra el resumen y el detalle de errores en la consola."""
    print("\n" + "=" * 60)
    print(f"ANÁLISIS DEL ARCHIVO: {nombre_archivo}")
    print("=" * 60)
    print(f"Líneas analizadas:                 {estadisticas['total_lineas']}")
    print(f"Eventos identificados:             {estadisticas['eventos_identificados']}")
    print(f"Eventos INFO:                      {estadisticas['INFO']}")
    print(f"Eventos WARNING:                   {estadisticas['WARNING']}")
    print(f"Eventos ERROR:                     {estadisticas['ERROR']}")
    print(f"Fechas inválidas:                  {estadisticas['fechas_invalidas']}")
    print(
        "Líneas incompletas/mal formateadas:"
        f" {estadisticas['incompletas_o_mal_formateadas']}"
    )
    print(f"Registros válidos:                 {estadisticas['registros_validos']}")
    print(f"Porcentaje de registros válidos:  {estadisticas['porcentaje_validos']:.2f}%")

    errores = [resultado for resultado in resultados if not resultado["valido"]]
    if errores:
        print("\nDETALLE DE LÍNEAS CON ERRORES")
        print("-" * 60)
        for resultado in errores:
            motivos = "; ".join(resultado["errores"])
            print(f"Línea {resultado['numero']}: {motivos}")
            print(f"  Texto: {resultado['texto'] or '(vacía)'}")


def main():
    """Coordina la selección, lectura, análisis y presentación del reporte."""
    ruta = seleccionar_archivo()
    if not ruta:
        print("No se seleccionó ningún archivo.")
        return

    lineas = leer_archivo(ruta)
    if lineas is None:
        return

    resultados = analizar_lineas(lineas)
    estadisticas = generar_estadisticas(resultados)
    mostrar_reporte(ruta, resultados, estadisticas)


if __name__ == "__main__":
    main()

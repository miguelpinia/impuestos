# Impuestos

Este script ayuda a leer archivos CFDI.xml que contienen la
información de facturas hechas por una persona física o moral. En
particular, extrae, el importe, descuento, impuestos trasladados y
total de uno o más archivos xml. Estos valores son la suma total de
los reportados en cada uno de estos archivos.

Este script contiene dos funciones principales. La primera
`process_cfdi`, se encarga de procesar un sólo archivo xml (parámetro
file_name). Devolviendo un diccionario con los siguientes campos
`[importe, descuento, impuestos, total]`.

La segunda función `process_cfdi_folder` recibe como parámetro el
folder donde se encuentran todos los archivos xml a procesar. Devuelve
un diccionario con los siguientes campos: `[importe, descuento,
impuestos, total]`.

 Más información adentro del archivo `facturas.py`.

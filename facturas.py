#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Administración de archivos de CFDI.
Autor: Miguel Angel Piña Avelino
email: miguel_pinia@ciencias.unam.mx
twitter: @miguelpinia

Descripción:
  Este script ayuda a leer archivos CFDI.xml que contienen la
  información de facturas hechas por una persona física o moral. En
  particular, extrae, el importe, descuento, impuestos trasladados y
  total de uno o más archivos xml. Estos valores son la suma total de
  los reportados en cada uno de estos archivos.

  Este script contiene dos funciones principales. La primera
  `process_cfdi`, se encarga de procesar un sólo archivo xml
  (parámetro file_name). Devolviendo un diccionario con los siguientes
  campos `[importe, descuento, impuestos, total]`.

  La segunda función `process_cfdi_folder` recibe como parámetro el
  folder donde se encuentran todos los archivos xml a
  procesar. Devuelve un diccionario con los siguientes campos:
  `[importe, descuento, impuestos, total]`.
"""

import argparse
import os
import os.path
import xml.etree.ElementTree as ET


def process_cfdi(file_name):
    """
    Procesa un archivo xml para obtener el importe, descuento,
    impuestos y total descritos.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()
    datos = {}
    for child in root:
        if 'Conceptos' in child.tag:
            conceptos = child
            importe = sum([float(concepto.attrib['Importe'])
                           for concepto in conceptos])
            descuento = sum([float(concepto.attrib.get('Descuento'))
                             for concepto in conceptos
                             if concepto.attrib.get('Descuento') is not None])
            datos['importe'] = float(f'{importe:.2f}')
            datos['descuento'] = float(f'{descuento:.2f}')
        if 'Impuestos' in child.tag:
            impuestos = child
            impuesto = float(impuestos.attrib.get('TotalImpuestosTrasladados'))
            datos['impuestos'] = float(f'{impuesto:.2f}')
    total = datos['importe'] - datos['descuento'] + datos['impuestos']
    datos['total'] = float(f'{total:.2f}')
    return datos


def process_cfdi_folder(folder_path):
    """
    Procesa todos los archivos xml en una carpeta.
    """
    impuestos = 0
    total = 0
    importe = 0
    descuento = 0
    for file_ in os.listdir(folder_path):
        if file_.endswith(".xml"):
            datos = process_cfdi(os.path.join(folder_path, file_))
            importe += datos['importe']
            descuento += datos['descuento']
            impuestos += datos['impuestos']
            total += datos['total']
    print(
        'Importe:\t{:.2f}\nDescuento:\t{:.2f}\nImpuestos:\t{:.2f}\nTotal:\t\t{:.2f}'.format(
            importe,
            descuento,
            impuestos,
            total))
    return {'importe': float(f'{importe:.2f}'),
            'descuento': float(f'{descuento:.2f}'),
            'impuestos': float(f'{impuestos:.2f}'),
            'total': float(f'{total:.2f}')}


def main():
    """
    Método principal. Genera un help para la apliación y se encarga de
    invocar la función principal para calcular los impuestos.
    """
    desc = '''
    Herramienta para la contabilidad mensual. Permite calcular los
    gastos hechos a partir de los cfdi.xml que son generados en cada
    factura. Estos archivos deben estar en una carpeta y estos deben
    ser del mes que se quieren calcular los impuestos.
    '''
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-d',
        '--directory',
        metavar='Directory',
        help='''
        Debe ser una ruta hacia un directorio.
        Por ejemplo: ~/foo/bar/
        ''')
    args = parser.parse_args()
    if args.directory:
        xml_folder_path = args.directory
        process_cfdi_folder(xml_folder_path)


if __name__ == "__main__":
    main()

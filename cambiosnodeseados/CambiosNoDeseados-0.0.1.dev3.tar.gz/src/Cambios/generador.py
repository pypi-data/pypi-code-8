#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Generador')

from StringIO import StringIO
import traceback
from glob import glob
from os import path

from pygame import image
from lxml.etree import parse, XSLT, DTD, tostring, XMLParser
from weasyprint import HTML, CSS, default_url_fetcher


CC = path.join(path.abspath(path.dirname(__file__)), 'Cartas')
CE = path.join(path.abspath(path.dirname(__file__)), 'Estilos')
CP = path.join(path.abspath(path.dirname(__file__)), 'PreGeneradas')

parser = XMLParser(dtd_validation=False)
xslt = XSLT(parse(path.join(CE, 'alt.xsl')))
css = CSS(filename=path.join(CE, 'alt.css'))


def main(parser, xslt, css):

    cartas = glob(path.join(CC, '*.xml'))
    total = len(cartas)

    for carta in cartas:
        REG.info('Transformando {} ({} de {})'.format(carta, cartas.index(carta)+1, total))

        try:
            xml = parse(carta, parser)
        except Exception:
            error = traceback.format_exc()
            REG.warning('Error de de Parceo: {}'.format(error))

        transformar(xml, xslt, css)
    REG.info('Archivos de cartas creados')


def transformar(xml, xslt, css):
    nombre = u'{}-{}{}'.format(
        xml.xpath('//nombre')[0].text,
        xml.xpath('//serial')[0].text,
        xml.xpath('//vercion')[0].text)
    html = HTML(tree=xslt(xml))
    html.write_png(
        target=path.join(CP, u'{}.png'.format(nombre)),
        stylesheets=[css,],
        resolution=600)


def ProducirImagen(xml, codigo):
    nombre = path.join(CP, '{}.png'.format(codigo))
    REG.debug('Generango PNG de {} en {} a resolucion de {}'.format(codigo, nombre, 96*3))
    with open(nombre, 'w') as temp:
        html = HTML(tree=xslt(xml))
        html.write_png(target=temp, stylesheets=[css,], resolution=96*3)

    return nombre


if __name__ == '__main__':
    main(parser, xslt, css)

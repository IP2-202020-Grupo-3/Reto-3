"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicialización del catálogo
# ___________________________________________________


def init():
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):

    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8"),
                                delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def accidentsSize(analyzer):
    return model.accidentsSize(analyzer)


def indexHeight(analyzer):
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    return model.indexSize(analyzer)


def minKey(analyzer):
    return model.minKey(analyzer)


def maxKey(analyzer):
    return model.maxKey(analyzer)

def accidentsDateSeverity(analyzer, date):
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.accidentsDateSeverity(analyzer, fecha.date())
    
def accidentsBeforeDate(analyzer, date):
    fecha = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.accidentsBeforeDate(analyzer, fecha.date())

def accidentsRangeDate(analyzer, dateStart, dateEnd):
    fechaIni = datetime.datetime.strptime(dateStart, '%Y-%m-%d')
    fechaEnd = datetime.datetime.strptime(dateEnd, '%Y-%m-%d')
    return model.accidentsRangeDate(analyzer, fechaIni.date(), fechaEnd.date())

def getAccidentsByRangeState(analyzer, dateStart, dateEnd):
    fechaIni = datetime.datetime.strptime(dateStart, '%Y-%m-%d')
    fechaEnd = datetime.datetime.strptime(dateEnd, '%Y-%m-%d')
    return model.getAccidentsByRangeState(analyzer, fechaIni.date(), fechaEnd.date())
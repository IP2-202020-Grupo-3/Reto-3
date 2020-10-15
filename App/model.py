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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from App import controller
from DISClib.DataStructures import listiterator as it
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catálogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {'accidents': None,
                'dateIndex': None,
                "hourIndex": None
                }

    analyzer['accidents'] = lt.newList('ARRAY_LIST', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer["hourIndex"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar información al catálogo

def addAccident(analyzer, accident):
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    updateHourIndex(analyzer['hourIndex'], accident)
    return analyzer

def updateDateIndex(map, accident):
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map

def updateHourIndex(map, accident):
    occurredhour = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurredhour, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.time().replace(second=0, microsecond=0))
    if entry is None:
        datentry = newDataEntry(accident)
        if accidentdate.minute >= 0 and accidentdate.minute < 15:
            om.put(map, accidentdate.time().replace(minute=0, second=0, microsecond=0), datentry)
        if accidentdate.minute >= 15 and accidentdate.minute < 30:
            om.put(map, accidentdate.time().replace(minute=30, second=0, microsecond=0), datentry)
        elif accidentdate.minute >= 30 and accidentdate.minute < 59:
            om.put(map, accidentdate.time().replace(minute=30, second=0, microsecond=0), datentry)
    else:
        datentry = me.getValue(entry)
    addHourIndex(datentry, accident)
    return map

def addHourIndex(datentry, accident):
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)

    return datentry

def addDateIndex(datentry, accident):
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)

    return datentry

def newDataEntry(accident):
    entry = {'lstaccidents': None}
    entry['lstaccidents'] = lt.newList('ARRAY_LIST', compareDates)
    return entry


# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):

    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    return om.maxKey(analyzer['dateIndex'])

def accidentsDateSeverity(analyzer, date):
    sev1 = 0
    sev2 = 0
    sev3 = 0
    sev4 = 0
    accidentdate = om.get(analyzer['dateIndex'], date)
    if accidentdate['key'] is not None:
        accidentlist = me.getValue(accidentdate)['lstaccidents']
        for i in range(0, lt.size(accidentlist)):
            if int(accidentlist["elements"][i]["Severity"]) == 1:
                sev1 += 1
            elif int(accidentlist["elements"][i]["Severity"]) == 2:
                sev2 += 1
            elif int(accidentlist["elements"][i]["Severity"]) == 3:
                sev3 += 1
            elif int(accidentlist["elements"][i]["Severity"]) == 4:
                sev4 += 1
        return sev1, sev2, sev3, sev4
    elif accidentdate['key'] is None:
        return 0, 0, 0, 0

def accidentsBeforeDate(analyzer, date):
    accidentdate = om.get(analyzer['dateIndex'], date)
    if accidentdate['key'] is not None:
        minima = minKey(analyzer)
        valor = om.values(analyzer["dateIndex"], minima, date)
        fechas = {}
        lstiterator = it.newIterator(valor)
        totalaccidents = 0
        while (it.hasNext(lstiterator)):
            lstdate = it.next(lstiterator)
            totalaccidents += lt.size(lstdate['lstaccidents'])
            if lstdate['lstaccidents']["elements"][0]["Start_Time"] not in list(fechas.keys()):
                fechas[lstdate['lstaccidents']["elements"][0]["Start_Time"]] = lt.size(lstdate['lstaccidents'])
            else:
                fechas[lstdate['lstaccidents']["elements"][0]["Start_Time"]] += lt.size(lstdate['lstaccidents'])
        llaves = list(fechas.keys())
        valores = list(fechas.values())
        mayor = max(valores)
        fechaMax = str(llaves[valores.index(mayor)])
        fecha = fechaMax[0:10]

        return totalaccidents, fecha
    else:
        return 0, 0

def accidentsRangeDate(analyzer, dateStart, dateEnd):
        valor = om.values(analyzer["dateIndex"], dateStart, dateEnd)
        severidades = {"Severidad 1":0, "Severidad 2":0, "Severidad 3":0, "Severidad 4": 0}
        lstiterator = it.newIterator(valor)
        totalaccidents = 0
        while (it.hasNext(lstiterator)):
            lstdate = it.next(lstiterator)
            totalaccidents += lt.size(lstdate['lstaccidents'])
            fecha = lstdate['lstaccidents']["elements"][0]["Start_Time"]
            sev1dia, sev2dia, sev3dia, sev4dia, = controller.accidentsDateSeverity(analyzer, fecha[0:10])
            severidades["Severidad 1"] += sev1dia
            severidades["Severidad 2"] += sev2dia
            severidades["Severidad 3"] += sev3dia
            severidades["Severidad 4"] += sev4dia
        llaves = list(severidades.keys())
        valores = list(severidades.values())
        mayor = max(valores)
        sevMax = llaves[valores.index(mayor)]
            
        return totalaccidents, sevMax

def getAccidentsByRangeState(analyzer, initialDate, endDate):
        valor = om.values(analyzer["dateIndex"], initialDate, endDate)
        estados = {}
        fechas = {}
        lstiterator = it.newIterator(valor)
        totalaccidents = 0
        while (it.hasNext(lstiterator)):
            lstdate = it.next(lstiterator)
            totalaccidents += lt.size(lstdate['lstaccidents'])
            if lstdate['lstaccidents']["elements"][0]["State"] not in list(estados.keys()):
                estados[lstdate['lstaccidents']["elements"][0]["State"]] = lt.size(lstdate['lstaccidents'])
            else:
                estados[lstdate['lstaccidents']["elements"][0]["State"]] += lt.size(lstdate['lstaccidents'])

            if lstdate['lstaccidents']["elements"][0]["Start_Time"] not in list(fechas.keys()):
                fechas[lstdate['lstaccidents']["elements"][0]["Start_Time"]] = lt.size(lstdate['lstaccidents'])
            else:
                fechas[lstdate['lstaccidents']["elements"][0]["Start_Time"]] += lt.size(lstdate['lstaccidents'])

        llavesEstados = list(estados.keys())
        valoresEstados = list(estados.values())
        mayorEstados = max(valoresEstados)
        estadoMax = str(llavesEstados[valoresEstados.index(mayorEstados)])

        llavesFecha = list(fechas.keys())
        valoresFecha = list(fechas.values())
        mayorFecha = max(valoresFecha)
        fechaMax = str(llavesFecha[valoresFecha.index(mayorFecha)])
        fecha = fechaMax[0:10]


        return estadoMax, fecha

def accidentsPerHour(analyzer, hourStart, hourEnd):
    if hourStart.minute >= 0 and hourStart.minute < 15:
        fechaIni = hourStart.replace(minute=0, second=0, microsecond=0)
    elif hourStart.minute >= 15 and hourStart.minute < 30:
        fechaIni = hourStart.replace(minute=30, second=0, microsecond=0)
    elif hourStart.minute >= 30 and hourStart.minute < 59:
        fechaIni = hourStart.replace(minute=30, second=0, microsecond=0)
    if hourEnd.minute >= 0 and hourEnd.minute < 30:
        fechaFin = hourEnd.replace(minute=0, second=0, microsecond=0)
    elif hourEnd.minute >= 15 and hourEnd.minute < 30:
        fechaFin = hourEnd.replace(minute=30, second=0, microsecond=0)
    elif hourEnd.minute >= 30 and hourEnd.minute < 59:
        fechaFin = hourEnd.replace(minute=30, second=0, microsecond=0)

    valor = om.values(analyzer["hourIndex"], fechaIni, fechaFin)
    lstiterator = it.newIterator(valor)
    totalaccidents = 0
    print(valor)
    while (it.hasNext(lstiterator)):
        lstdate = it.next(lstiterator)
        totalaccidents += lt.size(lstdate['lstaccidents'])

    return totalaccidents

    

# ==============================
# Funciones de Comparación
# ==============================

def compareIds(id1, id2):
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareStates(state1, state2):
    state = me.getKey(state2)
    if (state1 == state):
        return 0
    elif (state1 > state):
        return 1
    else:
        return -1
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
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------

def newAnalyzer():
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('ARRAY_LIST', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
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

def addDateIndex(datentry, accident):
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    stateIndex = datentry['stateIndex']
    stateentry = m.get(stateIndex, accident['State'])
    if (stateentry is None):
        entry = newStateEntry(accident['State'], accident)
        lt.addLast(entry['lstaccidents'], accident)
        m.put(stateIndex, accident['State'], entry)
    else:
        entry = me.getValue(stateentry)
        lt.addLast(entry['lstaccidents'], accident)
    return datentry

def newDataEntry(accident):
    entry = {'stateIndex': None,'lstaccidents': None}
    entry['stateIndex'] = m.newMap(numelements=100,
                                     maptype='PROBING',
                                     comparefunction=compareStates)
    entry['lstaccidents'] = lt.newList('ARRAY_LIST', compareDates)
    return entry

def newStateEntry(state, accident):
    stateentry = {'state': None, 'lstaccidents': None}
    stateentry['state'] = state
    stateentry['lstaccidents'] = lt.newList('ARRRAY_LIST', compareStates)
    return stateentry

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


    

# ==============================
# Funciones de Comparacion
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
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

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config
from DISClib.ADT import orderedmap as om

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfile = r"C:\Users\Juan PC\Documents\Python Scripts\Reto-3\Data\us_accidents_small.csv"

# ___________________________________________________
#  Menú principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Mostrar la cantidad de accidentes por severidad en una fecha dada")
    print("4- Consultar cantidad de accidentes antes de una fecha")
    print("5- Consultar cantidad de accidentes entre fechas")
    print("6- Consultar el estado con más accidentes entre ciertas fechas")
    print("7- Consultar la cantidad de accidentes en un rango de horas. (Consulta todas las fechas)")
    print("0- Salir")
    print("*******************************************")


"""
Menú principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes ....")
        controller.loadData(cont, accidentsfile)
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
    elif int(inputs[0]) == 3:
        fecha = input("Entre la fecha a buscar (Formato: YYYY-MM-DD): ")
        print("\nBuscando accidentes en una fecha por severidad")
        sev1, sev2, sev3, sev4 = controller.accidentsDateSeverity(cont, fecha)
        print("Se encontró la siguiente cantidad de accidentes ocurridos el {0}:".format(fecha))
        print("Severidad 1 : {0}".format(sev1))
        print("Severidad 2 : {0}".format(sev2))
        print("Severidad 3 : {0}".format(sev3))
        print("Severidad 4 : {0}".format(sev4))
    elif int(inputs[0]) == 4:
        fecha = input("Entre la fecha a buscar (Formato: YYYY-MM-DD): ")
        print("\nBuscando accidentes antes de: {0}".format(fecha))
        cantidad, fechaMax = controller.accidentsBeforeDate(cont, fecha)
        print("Antes del {0} ocurrieron {1} accidentes. \nLa fecha con más accidentes es: {2}".format(fecha, cantidad, fechaMax))
    elif int(inputs[0]) == 5:
        fechaIni = input("Entre la fecha inicial a buscar (Formato: YYYY-MM-DD): ")
        fechaFin = input("Entre la fecha final a buscar (Formato: YYYY-MM-DD): ")
        print("\nBuscando accidentes entre {0} y {1}: ".format(fechaIni, fechaFin))
        cantidad, sevMax = controller.accidentsRangeDate(cont, fechaIni, fechaFin)
        print("Entre el {0} y el {1} ocurrieron {2} accidentes. \nLa severidad con más accidentes es: {3}".format(fechaIni, fechaFin, cantidad, sevMax))
    elif int(inputs[0]) == 6:
        fechaIni = input("Entre la fecha inicial a buscar (Formato: YYYY-MM-DD): ")
        fechaFin = input("Entre la fecha final a buscar (Formato: YYYY-MM-DD): ")
        print("\nBuscando estado con más accidentes entre {0} y {1}: ".format(fechaIni, fechaFin))
        estado, fechaMax = controller.getAccidentsByRangeState(cont, fechaIni, fechaFin)
        print("El estado que más accidentes tiene entre el {0} y {1} es: {2}. \nLa fecha con más accidentes es: {3}".format(fechaIni, fechaFin, estado, fechaMax))
    elif int(inputs[0]) == 7:
        horaIni = input("Entre la hora inicial a buscar (Formato: HH:MM): ")
        horaFin = input("Entre la hora final a buscar (Formato: HH:MM): ")
        print("\nBuscando accidentes entre {0} y {1}: ".format(horaIni, horaFin))
        totalaccidents, sev1, sev2, sev3, sev4, promedio = controller.accidentsPerHour(cont, horaIni, horaFin)
        print("Se han registrado {0} accidentes entre las horas de {1} y {2}. \nSe encontraron los siguientes accidentes: \nSeveridad 1: {3} \nSeveridad 2: {4} \nSeveridad 3: {5} \nSeveridad 4: {6} \nEl promedio de accidentes encontrados con respecto al total es: {7}".format(totalaccidents, horaIni, horaFin, sev1, sev2, sev3, sev4, promedio))
    else:
        sys.exit(0)
sys.exit(0)

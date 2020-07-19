from pathlib import Path
import collections

def pointcounter(respuestas_correctas, respuestas_alumno):

	rc = respuestas_correctas[2:]
	ra = respuestas_alumno[3:]
	ra = ajustar_lista(rc, ra)
	counter = 0

	for la, lb in zip(rc, ra):
		if la == lb:
			counter += 1

	return counter * 100 / len(rc)


def ajustar_lista(lista_completa, lista_alumno):
	'''
	Si la lista de respuestas del alumno esta incompleta, esta función rellena con -
	Si tiene más respuestas de las pedidas, elimina las últimas
	: param lista_completa : lista de respuestas completa
	: param lista_alumno : lista de respuestas del alumno
	'''

	correct_len = len(lista_completa)
	alumn_len = len(lista_alumno)

	missing_answers = correct_len - alumn_len 	

	for _ in range(missing_answers):
		lista_alumno.append('-')

	if missing_answers < 0:
		for _ in range(abs(missing_answers)):
			lista_alumno = lista_alumno[:-1]

	return lista_alumno

AlumnoInfo = collections.namedtuple(
	'alumnoInfo',
	'nombre, tarea_num, calificacion'
	)
alumnosDict = {}
alumnosList = []

with open("tareas/respuestas.txt", "r") as r:
	r = r.read().split('\n')

for tarea in Path("tareas/").iterdir():
	if tarea.is_file() and tarea.name.startswith('tarea'):
		with open(tarea, "r", encoding="utf-8", errors="ignore") as t:
			t = t.read()
			t = t.split('\n')

			calificacion = pointcounter(r,t) 
			alumnosList.append(t[1])
			alumnosDict[t[1]] =AlumnoInfo(nombre=t[0], tarea_num=t[2], calificacion=calificacion)
	

with open("calificacionesTodos.csv", "w") as f:
	header = "Nombre , email , Tarea , Calificación"
	f.write(header)
	f.write("\n")
	for aL in alumnosList:
		line = alumnosDict[aL].nombre + " , " + aL + " , " + str(alumnosDict[aL].tarea_num) + " ," + str(alumnosDict[aL].calificacion)
		f.write(line)
		f.write("\n")




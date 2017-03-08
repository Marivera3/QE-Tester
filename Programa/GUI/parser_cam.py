def hay_camara(nombre, directorio):
    if nombre:
        for cam in directorio:
            cam = cam.split(".")
            cam = cam[:-1]
            cam = ".".join(cam)
            if nombre in cam:
                return True
    else:
        return False


def crear_camara(path, nombre, area_pixel, ganancia=None):
    with open(path + "/" + nombre + ".txt", "w") as arch:
        arch.write("---" * 20 + "\n")
        arch.write("Nombre de la camara: {0}\nArea pixel: {1}\nGanancia de conversion: {2}\n".format(
            nombre, area_pixel, ganancia))


def agregar_mediciones_old(path, nombre, mediciones, path_fotos):
    with open(path + "/" + nombre + ".txt", "a") as arch:
        arch.write("Cantidad de mediciones: {0}\nPath de las fotos: {1}\n".format(
            mediciones, path_fotos))


def nueva_seccion_camara(path, nombre, mediciones, path_fotos, ganancia=None, area_pixel=None):
    with open(path + "/" + nombre + ".txt", "a") as arch:
        arch.write("---" * 20 + "\n")
        if bool(area_pixel):
            arch.write("Area pixel: {0}\n".format(area_pixel))
        if bool(ganancia):
            arch.write("Ganancia de conversion: {0}\n".format(ganancia))
        arch.write("Cantidad de mediciones: {0}\nPath de las fotos: {1}\n".format(
            mediciones, path_fotos))


def leer_camara(path, nombre):
    dict_retorno = dict()
    with open(path + "/" + nombre + ".txt", "r") as arch:
        for linea in arch:
            linea = linea.strip("\n").split(":")
            if "Nombre de la camara" in linea:
                dict_retorno["nombre"] = linea[-1].strip(" ")
            elif "Area pixel" in linea:
                dict_retorno["area_pixel"] = linea[-1].strip(" ")
            elif "Ganancia de conversion" in linea:
                if linea[-1]:
                    dict_retorno["ganancia"] = linea[-1].strip(" ")

    return dict_retorno


def isfloat(element):
    try:
        float(element)
    except ValueError:
        return False
    else:
        return True

if __name__ == '__main__':
    print(leer_camara(
        "C:\\Users\\maxri\\Documents\\UC\\Ipre\\QE tester1\\Programa\\Camaras", "Max"))

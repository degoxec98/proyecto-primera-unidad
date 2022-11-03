from random import randint
import pandas as pd
import csv,os
os.system("clear")

class Libro:
    def __init__(self, titulo: str, genero: str, ISBN: str, editorial: str, autor: list) -> None:
        self.__id = None
        self.__titulo = titulo
        self.__genero = genero
        self.__ISBN = ISBN
        self.__editorial = editorial
        self.__autor = autor

    def get_id(self) -> str:
        return self.__id
    
    def __set_id(self, id: str) -> None:
        self.__id = id
    
    def get_titulo(self) -> str:
        return self.__titulo
    
    def set_titulo(self, titulo: str) -> None:
        self.__titulo = titulo
    
    def get_genero(self) -> str:
        return self.__genero
    
    def set_genero(self, genero: str) -> None:
        self.__genero = genero
    
    def get_ISBN(self) -> str:
        return self.__ISBN
    
    def set_ISBN(self, ISBN: str) -> None:
        self.__ISBN = ISBN

    def get_editorial(self) -> str:
        return self.__editorial
    
    def set_editorial(self, editorial: str) -> None:
        self.__editorial = editorial
    
    def get_autor(self) -> list:
        return self.__autor
    
    def set_autor(self, autor: list) -> None:
        self.__autor = autor

    def libro_to_list(self, id = None) -> list:
        print(self.get_autor())
        autor = self.get_autor()[0]
        for i in range(1, len(self.get_autor())):
            autor += ("/" + self.get_autor()[i])
        if self.get_id() == None:
            self.__set_id(id)
        libro_enlista = [self.__id, self.__titulo, self.__genero, self.__ISBN, self.__editorial, autor]
        return libro_enlista

def validar_str(txt: str, longitud_max: int) -> str:
    while True:
        dato = input(txt)
        if  dato != "" and len(dato) <= longitud_max:
            return dato
        print("Ingrese un dato válido!")

def validar_int(txt: str) -> int:
    while True:
        dato = input(txt)
        if dato.isnumeric():
            return int(dato)
        print("Ingrese un dato válido!")

def ingresar_datos() -> Libro:
    titulo = validar_str("Ingrese el nombre del libro: ", 30)
    genero = validar_str("Ingrese el genero del libro: ", 20)
    ISBN = validar_str("Ingrese el ISBN del libro: ", 20)
    editorial = validar_str("Ingrese el editorial del libro: ", 30)
    num_autores = validar_int("Ingrese el número de autores: ")
    autor = []
    for i in range(0, num_autores):
        autor.append(validar_str("Ingrese el nombre del autor: ", 30))
    return Libro(titulo, genero, ISBN, editorial, autor)


def listar_libros():
    with open('libros.csv') as f:
        reader = csv.reader(f)
        datos = []
        for i in reader:
            print(i)
            datos.append(i)

def agregar_libro():
    with open('libros.csv', 'a', newline='') as f:
        libro = ingresar_datos()
        id_auto = str(randint(3,1000))
        print(id_auto)
        nuevo_libro = libro.libro_to_list(id_auto)
        print(nuevo_libro)
        writer = csv.writer(f)
        writer.writerow(nuevo_libro)

def eliminar_libro():
    '''
    Función que elimina una entrada (fila / row)
    del archivo libro.csv
    '''
    # Cargar libro
    libros = pd.read_csv('libros.csv')
    # contador
    opcion = 1
    # base de mensaje
    mensaje = 'Ingrese:'
    # generando mensaje
    for i in libros.columns:
        mensaje += f'\n{opcion} para eliminar por {i}\n'
        opcion +=1
    
    # imprimiendo mensaje
    columna = int(input(mensaje)) - 1
    # busco la columna a la cual se refiere
    columna = libros.columns[columna]

    # buscar valor específico para borrar toda la fila 
    if columna == libros.columns[0]:
        id = int(input('Ingrese el ID (debe ser un número) a eliminar:\n'))
        libros = libros.loc[libros[columna] != id]
        #        libros.loc[libros[libros.columns[0]] != 1]
    elif columna ==  libros.columns[1]:
        titulo = input("Ingrese el título del libro que desea eliminar:\n")
        libros = libros.loc[libros[columna] != titulo.title()]
    elif columna == libros.columns[2]:
        genero = input("Ingrese el género del libro que desea eliminar:\n")
        libros = libros.loc[libros[columna] != genero.title()]
    elif columna == libros.columns[3]:
        isbn = input("Ingrese ISBN del libro que desea eliminar:\n")
        #creo que el csv['ISBN'] debe tener sólo el código isbn mas no empezar con ISBN..
        libros = libros.loc[libros[columna] != isbn.upper()]
    elif columna == libros.columns[4]:
        editorial = input("Ingrese la editorial del libro que desea eliminar:\n")
        libros = libros.loc[libros[columna] != editorial.title()]
    elif columna == libros.columns[5]:
        autor = input("Ingrese el autor del libro que desea eliminar:\n")
        libros = libros.loc[libros[columna] != autor.title()]
    
    # guardar libro modificado
    libros.to_csv('libros.csv',index=False)

def menu():
    print("menu")
    listar_libros()
    agregar_libro()

menu()


libro01 = Libro('Titulo 01', "Accion", "ISBN 01", "Editorial 01", ["Autor 01"])
libro02 = Libro('Titulo 01', "Accion", "ISBN 01", "Editorial 01", ["Autor 01", "Autor 02", "Autor 03"])

from tempfile import NamedTemporaryFile
import shutil, csv, time, os
import pandas as pd
os.system("clear")

class Book:
    def __init__(self, title: str, genre: str, ISBN: str, editorial: str, authors: list) -> None:
        self.__id = None
        self.__title = title
        self.__genre = genre
        self.__ISBN = ISBN
        self.__editorial = editorial
        self.__authors = authors

    def get_id(self) -> str:
        return self.__id
    
    def set_id(self, id: str) -> None:
        self.__id = id
    
    def get_title(self) -> str:
        return self.__title
    
    def set_title(self, title: str) -> None:
        self.__title = title
    
    def get_genre(self) -> str:
        return self.__genre
    
    def set_genre(self, genre: str) -> None:
        self.__genre = genre
    
    def get_ISBN(self) -> str:
        return self.__ISBN
    
    def set_ISBN(self, ISBN: str) -> None:
        self.__ISBN = ISBN

    def get_editorial(self) -> str:
        return self.__editorial
    
    def set_editorial(self, editorial: str) -> None:
        self.__editorial = editorial
    
    def get_authors(self) -> list:
        return self.__authors
    
    def set_authors(self, authors: list) -> None:
        self.__authors = authors
    
    def to_list(self) ->  list:
        return [self.__id, self.__title, self.__genre, self.__ISBN, self.__editorial, self.__authors]

    def to_dict(self, fields: list) -> list:
        return {
            fields[0]: self.__id,
            fields[1]: self.__title,
            fields[2]: self.__genre,
            fields[3]: self.__ISBN,
            fields[4]: self.__editorial,
            fields[5]: self.__authors
        }


class BookManagement:
    def __init__(self) -> None:
        self.__filename = 'libros.csv'
        self.__tempfile = NamedTemporaryFile(mode='w', delete=False)
        self.__fields = ['ID', 'Titulo', 'Genero', 'ISBN', 'Editorial', 'Autor']
        self.__books = []
        self.read = False

    def __generate_id(self):
        return str(int(self.__books[-1].get_id()) + 1)

    def exist_book(self, id):
        for book in self.__books:
            if book.get_id() == id:
                return True
        return False

    def read_file(self):
        with open(self.__filename) as f:
            reader = csv.reader(f)
            if not self.read:
                self.__books = []
            for i in reader:
                print(i)
                if not self.read:
                    id = i.pop(0)
                    book = FactoryBook.create(*i)
                    book.set_id(id)
                    self.__books.append(book)
            self.read = True

    def list_books(self):
        for book in self.__books:
            print(book.to_list())

    def add_book(self, book: list):
        book = FactoryBook.create(*book)
        book.set_id(self.__generate_id())
        self.__books.append(book)

    def update_book(self, id, book_update):
        i = 0
        for book in self.__books:
            if book.get_id() == id:
                book_update = FactoryBook.create(*book_update)
                book_update.set_id(id)
                self.__books[i] = book_update
            i += 1
    
    def save_changes(self):
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            for book in self.__books:
                writer.writerow(book.to_list())
            self.read = False


# ------------------------------------------
    
    def delete_book(self):
        self.save_changes()

        '''
        Función que elimina una entrada (fila / row)
        del archivo libro.csv
        '''
        input = Input()

        # Cargar libro
        book = pd.read_csv(self.__filename)

        # contador
        option = 1

        # base de mensaje
        message = 'Ingrese:'

        # generando mensaje
        for i in book.columns[[0,1,3]]:
            message += f'\n{option} para eliminar por {i}\n'
            option +=1

        # imprimiendo mensaje
        field = int(input.input_data(message,1,'int')) - 1

        if field == 2:
            field += 1

        # busco el field a la cual se refiere
        field = book.columns[field]

        # buscar valor específico para borrar toda la fila 
        if field == book.columns[0]:
            id = int(input.input_data('Ingrese el ID a eliminar:\n',
                    20,
                    type = 'int'))

            book = book.loc[book[field] != id]
            
        elif field ==  book.columns[1]:
            title = input.input_data('Ingrese el título del libro que desea eliminar:\n',
                                    30,
                                    type = 'str')

            book = book.loc[book[field] != title.capitalize()]

        elif field == book.columns[3]:
            isbn = input.input_data('Ingrese ISBN del libro que desea eliminar:\n',
                                    20,
                                    type='str')
            book = book.loc[book[field] != isbn.upper()]
        
        # guardar libro modificado
        book.to_csv(self.__filename,index=False)

        print("Se eliminó directamente en libros.csv")
        print("Por favor vuelva a leer el archivo eligiendo la opcion 01")
    

    def find_by_tit_isbn(self):
        self.save_changes()
        input = Input()
        
        while True:
            print('--- Buscar libro ---')
            for k, v in dict({'Titulo':1,'ISBN':2}).items():
                print(f'Ingrese {v} para buscar por {k}')
            field = int(input.input_data('',1,'int'))
            if field in [1,2]:
                if field == 2:
                    field = 3
                break
            else: print('Ingrese un valor válido.\n')

        book = pd.read_csv(self.__filename)

        field = book.columns[field]
        if field == book.columns[1]:
            while True:
                title = input.input_data('Ingrese el titulo del libro que desea buscar:\n',30,'str').capitalize()
                if title in list(book[field]):
                    print(book.loc[book[field] == title])
                    break
                print('El título no coincide con los almacenados en el archivo.')
        else:
            while True:
                isbn = input.input_data('Ingrese el ISBN del libro que desea buscar:\n',20,'str').upper()
                if isbn in list(book[field]):
                    print(book.loc[book[field] == isbn])
                    break
                print('El título no coincide con los almacenados en el archivo.')
        print("\nConsulta realizada!")
        print("Por favor vuelva a leer el archivo eligiendo la opcion 01\n")
        
        
    # Opción 6: Ordenar libros por título.
    def sort_by_title(self):
        self.save_changes()
        print('---Ordenando por título---')
        book = pd.read_csv(self.__filename)
        title = book.columns[1]
        print(book.sort_values(by=[title]))
        print("\nConsulta realizada!")
        print("Por favor vuelva a leer el archivo eligiendo la opcion 01\n")

    # Opción 7: Buscar libros por autor, editorial o género. Se deben sugerir las opciones y listar los resultados.
    def find_by_gen_auth_editor(self):
        self.save_changes()
        input = Input()
        
        while True:
            print('--- Buscar libro por autor o editorial ---')
            for k, v in dict({'Genero':1,'Editorial':2,'Autor':3}).items():
                print(f'Ingrese {v} para buscar por {k}')
            field = int(input.input_data('',1,'int'))
            if field in [1,2,3]:
                if field == 1:
                    field = 2
                elif field == 2:
                    field = 4
                else: field = 5
                break
            else: print('Ingrese un valor válido.\n')

        book = pd.read_csv(self.__filename)

        field = book.columns[field]
        if field == book.columns[2]:
            while True:
                genre = input.input_data('Ingrese el genero del libro que desea buscar:\n',30,'str').capitalize()
                if genre in list(book[field]):
                    print(book.loc[book[field] == genre])
                    break
                print('El género no coincide con los almacenados en el archivo.')
        elif field == book.columns[4]:
            while True:
                editorial = input.input_data('Ingrese la editorial del libro que desea buscar:\n',30,'str').capitalize()
                if editorial in list(book[field]):
                    print(book.loc[book[field] == editorial])
                    break
                print('La editorial no coincide con los almacenados en el archivo.')
        else:
            while True:
                author = input.input_data('Ingrese el autor del libro que desea buscar:\n',20,'str').capitalize()
                position = 0
                coincidencia = 0
                for i in book['Autor'].str.contains(author):
                    if i:
                        print(book[book['Autor'].str.contains('Autor 01')].iloc[[position]])
                        coincidencia += 1
                    position += 1
                if coincidencia != 0:
                    break
                else:
                    print('No se encuentra el autor que especifica.')
        print("\nConsulta realizada!")
        print("Por favor vuelva a leer el archivo eligiendo la opcion 01\n")
                
    # Opción 8: Buscar libros por número de autores. Se debe ingresar un número por ejemplo 2 (hace referencia a dos autores) y se deben listar todos los libros que contengan 2 autores.
    def find_by_number_of_authors(self):
        self.save_changes()
        input = Input()
        book = pd.read_csv(self.__filename)

        while True:
            print('---Buscar por numero de autores---')
            num_of_authors = int(input.input_data('Ingrese la cantidad de autores que hayan escrito el libro a buscar:\n',2,'int'))
            
            num_of_authors -= 1
            print(book.loc[ book['Autor'].str.count('/|,') == num_of_authors])
            break

        print("\nConsulta realizada!")
        print("Por favor vuelva a leer el archivo eligiendo la opcion 01\n")


class FactoryBook:
    @staticmethod
    def create(title: str, genre: str, ISBN: str, editorial: str, authors: list):
        return Book(title, genre, ISBN, editorial, authors)

class Input:
    @classmethod
    def input_data(cls, input_text:str, max_length: int, type: str):
        while True:
            data = input(input_text)
            if cls.__validate(data, max_length, type):
                return data

    @classmethod
    def __validate(cls, data, max_length, type):
        if type == 'str':
            return cls.__validate_str(data, max_length)
        if type == 'int':
            return cls.__validate_int(data, max_length)
        return False

    @classmethod
    def __validate_str(cls, data:str, max_length: int):
        return  data != "" and len(data) <= max_length

    @classmethod
    def __validate_int(cls, data:str, max_length: int):
        return  data != "" and data.isnumeric() and len(data) <= max_length


def input_data_to_record() -> Book:
    input = Input()
    title = input.input_data("Ingrese el nombre del libro: ", 30, 'str')
    genre = input.input_data("Ingrese el genero del libro: ", 20, 'str')
    ISBN = input.input_data("Ingrese el ISBN del libro: ", 20, 'str')
    editorial = input.input_data("Ingrese el editorial del libro: ", 30, 'str')
    authors_num = int(input.input_data("Ingrese el número de autores: ", 10, 'int'))
    authors = []
    for i in range(0, authors_num):
        authors.append(input.input_data("Ingrese el nombre del autor: ", 30, 'str'))
    return [title, genre, ISBN, editorial, authors]

def input_id() -> str:
    return Input.input_data("Ingrese el ID a actualizar: ", 10, 'int')


def switch(case, book_management):
    if case == 1:
        book_management.read_file()
        return
    elif book_management.read == False and case != 0:
        print("Tienes que leer el archivo (Opción 1) para poder elegir las opciones!")
        return
    elif case == 2:
        book_management.list_books()
        return
    elif case == 3:
        book_management.add_book(input_data_to_record())
        return 
    elif case == 4:
        book_management.delete_book()
        return
    elif case == 5:
        book_management.find_by_tit_isbn()
        return
    elif case == 6:
        book_management.sort_by_title()
        return
    elif case == 7:
        book_management.find_by_gen_auth_editor()
        return
    elif case == 8:
        book_management.find_by_number_of_authors()
        return
    elif case == 9:
        id = input_id()
        if book_management.exist_book(id):
            book_management.update_book(id, input_data_to_record())
        else:
            print("No se encontró el libro")
        return
    elif case == 10:
        book_management.save_changes()
        print("Guardado exitoso!")
        return
    

def print_options(options):
    for option in options:
        print(option)
    print(" ")

def main():
    options = [
        "Opción 1: Leer archivo actual",
        "Opción 2: Listar libros",
        "Opción 3: Agregar libro",
        "Opción 4: Eliminar libro",
        "Opción 5: Buscar libro por ISBN o por título",
        "Opción 6: Ordenar libros por título",
        "Opción 7: Buscar libros por autor, editorial o género",
        "Opción 8: Buscar libros por número de autores",
        "Opción 9: Actualizar datos de un libro",
        "Opción 10: Guardar Cambios",
        "Opción 0: Salir"
    ]
    book_management = BookManagement()
    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    case = 11
    while True:
        print_options(options)
        while case not in index: 
            case = int(Input.input_data("Ingrese la opción: ", 3, 'int'))
        switch(case, book_management)
        if case == 0:
            print("\nSaliendo de la aplicación...")    
            break
        print("\nRegresando al menú principal...\tEspere 10 segundos...\n")
        time.sleep(1)
        case = 11


main()

from tempfile import NamedTemporaryFile
import shutil, csv, os
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
        self.__booklist = list()

    def __generate_id(self):
        with open(self.__filename) as f:
            reader = csv.reader(f)
            *_, last = reader
            return str(int(last[0]) + 1)

    def exist_book(self, id):
        with open(self.__filename) as f:
            reader = csv.reader(f)
            for row in reader:
                if id == row[0]:
                    return True
            return False


    def list_books(self):
        books = []
        with open(self.__filename) as f:
            reader = csv.reader(f)
            for i in reader:
                id = i.pop(0)
                book = FactoryBook.create(*i)
                book.set_id(id)
                books.append(book)
        for book in books:
            print(book.to_list())

    def add_book(self, book: list):
        with open(self.__filename, 'a', newline='') as f:
            writer = csv.writer(f)
            book = FactoryBook.create(*book)
            book.set_id(self.__generate_id())
            writer.writerow(book.to_list())

    def update_book(self, id, book):
        with open(self.__filename, 'r') as f, self.__tempfile:
            reader = csv.DictReader(f, fieldnames= self.__fields)
            writer = csv.DictWriter(self.__tempfile, fieldnames= self.__fields)
            book = FactoryBook.create(*book)
            book.set_id(id)
            for row in reader:
                if row['ID'] == id:
                    row = book.to_dict(self.__fields)
                writer.writerow(row)
        shutil.move(self.__tempfile.name, self.__filename)
    
    def delete_book(self):
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
    
    # Opción 5: Buscar libro por ISBN o por título. Se debe sugerir las opciones y listar el resultado.
    def find_book(self):
        input = Input()
        excec = False
        
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
        # while excec == False:
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
        

        # print(field) # para visualizar.. luego eliminar


        # return book

    # Opción 6: Ordenar libros por título.
    # Opción 7: Buscar libros por autor, editorial o género. Se deben sugerir las opciones y listar los resultados.
    # Opción 8: Buscar libros por número de autores. Se debe ingresar un número por ejemplo 2 (hace referencia a dos autores) y se deben listar todos los libros que contengan 2 autores.
            

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



def menu():
    book_management = BookManagement()

    # book_management.list_books()
    # #book_management.add_book(input_data_to_record())
    # id = input_id()
    # if book_management.exist_book(id):
    #     book_management.update_book(id, input_data_to_record())
    # else:
    #     print("No se encontró el libro")

    # book_management.delete_book()
    book_management.find_book()


menu()

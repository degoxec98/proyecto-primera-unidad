
#from libro import Input
import requests, time, concurrent.futures
start = time.time()
        

class Request:
    def __make_request(self, url: str):
        response = requests.get(url)
        payload = {}
        if response.status_code == 200:
            payload = response.json()
        return payload

    def __build_pokemon_url(self, pokemon_name):
        return f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'

    def __get_pokemons(self, urls):
        print('ID |     NAME    |   ABILITY     | IMAGE' )
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in urls:
                futures.append(executor.submit(self.__make_request, url=url))
            for future in concurrent.futures.as_completed(futures):
                pokemon = future.result()
                ability = pokemon.get('abilities', [])[0]['ability']['name']
                image_url = pokemon.get('sprites', [])['front_default']
                id = pokemon.get('id', [])
                name = pokemon.get('name', [])
                print(f'{id} | {name} | {ability} | {image_url}')
                    

    def pokemons_by_generation(self, id: str):
        url = f'https://pokeapi.co/api/v2/generation/{id}'
        payload = self.__make_request(url)
        results = payload.get('pokemon_species', [])
        urls = []
        for pokemon in results:
            urls.append(self.__build_pokemon_url(pokemon["name"]))
        self.__get_pokemons(urls)

    def pokemons_by_form(self, url):
        payload = self.__make_request(url)
        self.__get_pokemons([(payload.get('pokemon', [])['url'])])

    def all_pokemons_form(self):
        url = f'https://pokeapi.co/api/v2/pokemon-form/?limit=2000'
        payload = self.__make_request(url)
        count = payload.get('count', [])
        results = payload.get('results', [])
        return count, results

    def pokemons_by_ability(self, id: str):
        url = f'https://pokeapi.co/api/v2/ability/{id}'
        payload = self.__make_request(url)
        results = payload.get('pokemon', [])
        urls = []
        for result in results:
            urls.append(self.__build_pokemon_url(result["pokemon"]["name"]))
        self.__get_pokemons(urls)

    def __show_some_abilities(self, results):
        i = 0
        options = []
        print("Elija una de las siguientes habilidades")
        for result in results:
            print(f'Opcion {i}: {result["name"]}')
            options.append(i)
            i += 1
        return options

    def get_some_abilities(self):
        url = f'https://pokeapi.co/api/v2/ability'
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()
            results = payload.get('results', [])
            return self.__show_some_abilities(results)
    
    def __show_some_habitats(self, results):
        i = 0
        options = []
        print("Elija una de los siguientes habitats")
        for result in results:
            print(f'Opcion {i}: {result["name"]}')
            options.append(i)
            i += 1
        return options
    
    def get_some_habitats(self):
        url = f'https://pokeapi.co/api/v2/pokemon-habitat'
        response = requests.get(url)
        if response.status_code == 200:
            payload = response.json()
            results = payload.get('results',[])
            return self.__show_some_habitats(results)

    def pokemons_by_habitat(self, id: str):
        url = f'https://pokeapi.co/api/v2/pokemon-habitat/{id}'
        payload = self.__make_request(url)
        results = payload.get('pokemon_species', [])
        urls = []
        for pokemon in results:
            urls.append(self.__build_pokemon_url(pokemon["name"]))
        self.__get_pokemons(urls)
    


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


def switch(case, request):
    if case == 1:
        id = Input.input_data("Ingrese la Generación de pokemon: ", 3, 'int')
        request.pokemons_by_generation(id)
        return
    elif case == 2:
        i, results = request.all_pokemons_form()
        number = int(Input.input_data(f"Sugerencia: ingrese un número en el intervalo del 1 al {i}: ", 3, 'int'))
        request.pokemons_by_form(results[number-1]['url'])
        return
    elif case == 3:
        options = request.get_some_abilities()
        op = 25
        while op not in options:
            op = int(Input.input_data('Ingrese una opcion: ', 3, 'int'))
        request.pokemons_by_ability(str(op + 1))
        return 
    elif case == 4:
        options = request.get_some_habitats()
        op = 25
        while op not in options:
            op=int(Input.input_data('Ingrese una opción: ',1,'int'))
        request.pokemons_by_habitat(str(op + 1))
        return
    elif case == 5:
        i, results = request.all_pokemons_type()
        number = int(Input.input_data(f'Sugerencia: Ingrese un numero en el intervalo del 1 al {i}: ',2,'int'))
        request.pokemons_by_type(results[number-1]['url'])
        return
    

def print_options(options):
    for option in options:
        print(option)
    print(" ")

def main():
    options = [
        "Opción 1: Listar pokemons por generación",
        "Opción 2: Listar pokemons por forma",
        "Opción 3: Listar pokemons por habilidad",
        "Opción 4: Listar pokemons por habitat",
        "Opción 5: Listar pokemons por tipo",
        "Opción 0: Salir"
    ]
    
    request = Request()

    index = [0, 1, 2, 3, 4, 5]
    case = 6
    while True:
        print_options(options)
        while case not in index: 
            case = int(Input.input_data("Ingrese la opción: ", 3, 'int'))
        switch(case, request)
        if case == 0:
            print("\nSaliendo de la aplicación...")    
            break
        print("\nRegresando al menú principal...\tEspere 10 segundos...\n")
        time.sleep(1)
        case = 6

main()

end = time.time()

print(end-start)

print(end-start)
import requests
import os
os.system('clear')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Opción 1: Listar pokemons por generación. 
# Se ingresa alguna generación (1, 2, 3, ..) 
# y se listan todos los pokemon respectivos.
def list_by_ability(url = 'https://pokeapi.co/api/v2/ability/',
                    offset=0,limit = 327):
    args = {'offset':offset,'limit':limit}
    response = requests.get(url,params=args)

    if response.status_code == 200:
        payload = response.json()#['results']#[0]['url']
        results = payload.get('results',[]) #returns a list

    counter = 0
    




# Opción 2: Listar pokemons por forma.
# Se ingresa alguna forma (deben sugerir valores) 
# y se listan todos los pokemons respectivos.






# Opción 3: Listar pokemons por habilidad.
# Se deben sugerir opciones a ingresar para interactuar.
def list_by_ability(url = 'https://pokeapi.co/api/v2/ability/',
                    offset=0,limit = 327):
    args = {'offset':offset,'limit':limit}
    response = requests.get(url,params=args)

    if response.status_code == 200:
        payload = response.json()#['results']#[0]['url']
        results = payload.get('results',[]) #returns a list

    counter = 0

    if results:   
        print(bcolors.HEADER + '--- Mostrando habilidades ----' + bcolors.ENDC,
                '\nSi no encuentras la habilidad que quieres, puedes seguir buscando',
                '\nCuando la encuentres ingresa su opción.')
        for option, ability in enumerate(results):
            ability = ability['name']
            print(f'{bcolors.BOLD}Opción {option+1} : {ability.capitalize()} {bcolors.ENDC}')
            counter += 1
            neg_ans = ''
            while counter == 10:
                next_block = input('Quieres que se muestren más habilidades?(s/n): ').lower()
                if next_block == 's':
                    counter = 0
                else: 
                    neg_ans = 'n'
                break
            if neg_ans == 'n' or '':
                break

        ability = int(input(bcolors.HEADER + '\nSeleccione la opción de la habilidad que desea listar: ' + bcolors.ENDC))-1

        print(f'\n--- Elegiste la habilidad {results[ability]["name"].upper()} ---\n')        
        ability_url = results[ability]['url']
        response2 = requests.get(ability_url)
        payload2 = response2.json()
        pokemons_info = payload2.get('pokemon',[])
        pokemon_names = list()
        image_list = list()
        for pokemon in pokemons_info:
            pokemon_names.append(pokemon['pokemon']['name'])
            pokemon_url = pokemon['pokemon']['url']
            response3 = requests.get(pokemon_url)
            payload3 = response3.json()
            pokemon_img_link = payload3['sprites']['front_default']
            image_list.append(pokemon_img_link)
        pokemon_and_images = list(zip(pokemon_names,image_list))

        for poketuple in pokemon_and_images:
            print(f'{bcolors.OKBLUE}Pokemon{bcolors.ENDC}:'
                    f'{poketuple[0].capitalize()}',\
                    f'\nLink: {bcolors.OKGREEN}{poketuple[1]}\
                    {bcolors.ENDC}','\n--- ---')


list_by_ability()





# Opción 4: Listar pokemons por habitat. 
# Se deben sugerir opciones a ingresar para interactuar.






# Opción 5: Listar pokemons por tipo.
# Se deben sugerir opciones a ingresar para interactuar.

# Nota: listar pokemons involucra: nombre, habilidad y URL de la imagen

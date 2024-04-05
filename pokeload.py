import os
from requests_html import HTMLSession
import pickle

pokemon_base = {
    "name" : "",
    "type" : None,
    "current_health" : 100,
    "base_health" : 100,
    "level" : 1,
    "current_exp" : 0,
    "attacks" : None,
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

def session():
    session = HTMLSession()
    return session


def get_pokemon(index):
    # Url de la base del pokemon
    url = "{}{}".format(URL_BASE, index)
    pokemon_page = session().get(url)
    pokemon = pokemon_base.copy()
    # Sacamos el nombre del pokemon
    pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n")[0]

    # Metemos los tipos del pokemon en una lista
    pokemon["type"] = []
    # Encontramos el tipo de cada pokemon
    pokemon_type = (pokemon_page.html.find(".pkmain", first=True).
                            find(".bordeambos", first=True).find("img"))
    for type in pokemon_type:
        pokemon["type"].append(type.attrs["alt"])

    pokemon["attacks"] = []
    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name" : attack_item.text.split("\n")[2],
            "type" : attack_item.find(".center img", first=True).attrs["alt"],
            "min_level" : attack_item.text.split("\n")[1],
            "damage" : attack_item.text.split("\n")[5].replace("--", "0"),
        }
        pokemon["attacks"].append(attack)

    return pokemon


# Cargamos todos los pokemones del archivo
def get_all_pokemon_file():
    try:
        # Cargamos el archivo con los pokemones almacenados
        print("CARGANDO EL ARCHIVO DE POKEMONS...")
        with open("pokefile.pkl", "rb") as pokefile:
            all_pokemon = pickle.load(pokefile)


    except FileNotFoundError:
        print("¡ARCHIVO NO ENCONTRADO!, CARGANDO DE INTERNET...")

        # Almacenamos los pokemones en una lista
        all_pokemon = []
        for index in range(151):
            all_pokemon.append(get_pokemon(index + 1))
            barra_progreso(index)


        # Guardamos los pokemones en un archivo externo
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemon, pokefile)

        print("¡TODOS LOS POKEMONES HAN SIDO CARGADOS CON EXITO!")
    return all_pokemon


def barra_progreso(index):
    os.system("cls")
    porcen = int(index*100/150)
    n_diferencia = 10
    n_porcen = int(porcen/10)
    n_diferencia -= n_porcen
    # Se va restando la diferencia a medida que avanza el progreso de la barra
    # El porcentaje aumenta
    barra = ("""Cargando los pokemos en la base de datos: \n
    |{}{}|""".format("*"*n_porcen," "*n_diferencia,))
    print("{}  {}%, {} de 150 pokemos completado".format(barra,porcen,index))


def main():
    print(get_all_pokemon_file())


if __name__ == '__main__':
    main()
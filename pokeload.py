from random import randrange
from requests_html import HTMLSession

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="

# Diccionario: Definimos la base de un pokemon
pokemon_base = {
    "name" : "",
    "current_health" : 100,
    "base_health" : 100,
    "level" : 1,
    "type" : "",
    "current_exp" : 0
}

def url():
    url_list = []
    for pokemon_page in range(1, 7):
        url = "{}{}".format(URL_BASE, pokemon_page)
        url_list.append(url)
    return url_list


def session():
    session = HTMLSession()
    return session


def get_pokemon(url_list):
    pokemons_dictionary = []
    for pokemons in url_list:
        pokemon = pokemon_base.copy()
        pokemon_info = session().get(pokemons)
        pokemon["name"] = pokemon_info.html.find(".mini", first=True).text.split("\n")[0]
        pokemons_dictionary.append(pokemon)

    return pokemons_dictionary


def main():
    url_list = url()
    pokemons = get_pokemon(url_list)
    print(pokemons)
    # AGREGAR AL DICCIONARIO EL TIPO DE POKEMON QUE ES


if __name__ == '__main__':
    main()

from requests_html import HTMLSession
import pickle

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk="
URL_BASE_ATAQUE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="

pokemon_min_num = 1
pokemon_max_num = 7


# Diccionario: Definimos la base de un pokemon
pokemon_base = {
    "name" : "",
    "current_health" : 100,
    "base_health" : 100,
    "level" : 1,
    "type" : None,
    "current_exp" : 0,
    "attacks" : None
}


def url():
    url_list = []
    for pokemon_page in range(pokemon_min_num, pokemon_max_num):
        url = "{}{}".format(URL_BASE, pokemon_page)
        url_list.append(url)
    return url_list

def url_ataques():
    url_list_ataques = []
    for pokemon_attacks in range(pokemon_min_num, pokemon_max_num):
        url = "{}{}".format(URL_BASE_ATAQUE, pokemon_attacks)
        url_list_ataques.append(url)
    return url_list_ataques



def session():
    session = HTMLSession()
    return session


def get_pokemon(url_list, url_list_ataques):
    pokemons_dictionary = []
    for pokemons in url_list:
        pokemon = pokemon_base.copy()
        pokemon_info = session().get(pokemons)
        pokemon["name"] = pokemon_info.html.find(".mini", first=True).text.split("\n")[0]

        # Convertimos el valor 'type' en una lista
        # Le damos valor a la clave 'type'
        pokemon["type"] = []
        for img in pokemon_info.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
            pokemon["type"].append(img.attrs["alt"])

        pokemon["attacks"] = []
        for pokemon_attack in url_list_ataques:
            pokemon_info_attack = session().get(pokemon_attack)
            for attack_item in pokemon_info_attack.html.find(".pkmain")[-1].find("tr .check3"): # [-1] Es el ultimo elemento de la lista
                attack = {
                    "name" : attack_item.find("td", first=True).find("a", first=True).text,
                    "type" : attack_item.find("td")[1].find("img", first=True).attrs["alt"],
                    "min_level" : attack_item.find("th", first=True).text,
                    "damage" : int(attack_item.find("td")[3].text.replace("--", "0"))
                }
                pokemon["attacks"].append(attack)

        pokemons_dictionary.append(pokemon)

    return pokemons_dictionary


def get_all_pokemon():
    try:
        print("Cargando el archivo de pokemons...")
        # Abrimos el archivo con los datos guardados
        # rb (read binary)
        with open("pokefile.pkl", "rb") as pokefile:
            # Carga el archivo 'pokefile'
            pickle.load(pokefile)

    except FileNotFoundError:
        print("Archivo no encontrado, cargando de internet...")
        all_pokemons = []
        url_list = url()
        url_list_attacks = url_ataques()
        pokemons = get_pokemon(url_list, url_list_attacks)
        for pokemon in pokemons:
            all_pokemons.append(pokemon)
            print("*", end="")

        # Guardar la variable para no volver a cargarla
        # La mantenemos intacta dentro de nuestra memoria

        # import pickle
        # .pkl (extension)
        # wb (write binary)
        with open("pokefile.pkl", "wb") as pokefile:
            # .dump (le da el formato de json{})
            # De la variable 'all_pokemons' lo metemos a 'pokefile'
            # pickle (guardamos el valor en memoria)
            pickle.dump(all_pokemons, pokefile)
        print("\n!Lista de pokemons cargada!")

        return all_pokemons


def main():
    for pokemon in get_all_pokemon():
        print(pokemon)


if __name__ == '__main__':
    main()
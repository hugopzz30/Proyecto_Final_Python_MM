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



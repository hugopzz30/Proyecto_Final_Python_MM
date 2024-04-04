import random
from pprint import pprint
from pokeload import get_all_pokemon

def get_player_profile(pokemon_list):
    return {
        "player_name" : input("¿Cuál es tu nombre? "),
        "pokemon_inventory" : [random.choice(pokemon_list) for player_pokemons in range(3)],
        "combats" : 0,
        "pokeballs" : 0,
        "health_potion" : 0,
    }


# List Comprehension
"""
# Ambos son iguales
# Se le llama 'List Comprehension' simplifica el ingresar un dato a una lista
[random.choice(pokemon_list) for player_pokemons in range(3)]
---------------------------------------------------
for player_pokemons in range(3):
    profile["pokemon_inventory"].append(random.randint(len(pokemon_list)))
"""


def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def get_pokemon_info(pokemon):
    return "{} | lvl {} | hp {} / {}".format(pokemon["name"],
                                             pokemon["level"],
                                             pokemon["current_health"],
                                             pokemon["base_health"])


def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        print("Elige con que Pokemon lucharas")
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
           return  player_profile["pokemon_inventory"][int(input(" ¿Cual eliges? "))]
        except (ValueError, IndexError):
            print("Opcion Invalida")


def player_attack(player_pokemon, enemy_pokemon):
    # Implementar multiplicadores en base al tipo de pokemon enemigo
    # Pokemon tipo debilidades, buscar debilidades
    # Cuando se elige el ataque del usuario, solo se muestran los ataques en ese nivel
    pass


def enemy_attack(enemy_pokemon, player_pokemon):
    pass


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]

            print("Tu pokemon ha subido al nivel {}".format(get_pokemon_info(pokemon)))


def cure_pokemon(player_profile, player_pokemon):
    pass

def capture_with_pokeball(player_profile, enemy_pokemon):
    pass


def fight(player_profile, enemy_pokemon):
    print("---Nuevo Combate---")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    print("Contrincantes: {} vs {}".format(get_pokemon_info(player_pokemon),
                                           get_pokemon_info(enemy_pokemon)))

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        # En cada turno, tener la opcion de que hacer
        action = None
        # A : Atacar
        # P : Pokeball
        # V : Pocion de vida
        # C : Cambiar Pokemon
        while action not in ["A", "P", "V", "C"]:
            action = input("¿Que deseas hacer [A]tacar, [P]okeball, [V]ida, [C]ambiar Pokemon")

        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            # Lista que almacena los ataques realizados en cada pelea
            attack_history.append(player_pokemon)
            # Random
        elif action == "V":
            # Si el ususario tiene curas en el inventario, se aplica cura 50 de vida hasta llegar a 100
            # Si el usuario no tiene, no se cura
            cure_pokemon(player_profile, player_pokemon)
        elif action == "P":
            # Si el usuario tiene pokeballs, se tira una
            # Hay una probabilidad random de capturar al pokemon con respecto a su vida
            # Si se captura pasa a estar en el inventario con la misma salud
            capture_with_pokeball(player_profile, enemy_pokemon)
        elif action == "C":
            # Cambiamos de pokemon
            player_pokemon = choose_pokemon(player_profile)

        enemy_attack(enemy_pokemon, player_pokemon)

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            player_pokemon = choose_pokemon(player_profile)
            # SI UN POKEMON SE MUERE, PODER ESCOGER UNO
            # SI LA VIDA DE UN POKEMON ES MENOS CERO, LA REGRESAMOS A CERO

    if enemy_pokemon["current_health"] == 0:
        print("Has Ganado!")
        # Asignar experiencia, mediante una lista
        assign_experience(attack_history)

    # COSAS A IMPLEMENTAR
        # AL FINAL DEL COMBATE, SI LA VIDA ENEMIGA ES 0, GANAMOS


    print("---Fin del Combate---")
    input("Presiona ENTER para continuar")



def get_item_lottery(player_profile):
    """ Segun un factor aleatorio al jugador le puede tocar una pokeball o una cura """
    pass


def main():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile(pokemon_list)

    # Imprime en formato JSON
    # pprint(player_profile)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        get_item_lottery(player_profile)

    print("Has perdido en el combate n{}".format(player_profile["combats"]))

if __name__ == '__main__':
    main()
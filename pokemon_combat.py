import random
from pokeload import get_all_pokemon


def get_player_profile (pokemon_list):
    return {
        "name" : input("Ingresa tu nombre: "),
        "pokemons_inventory" : [random.choice(pokemon_list) for player_pokemon in range(3)],
        "combats" : 0,
        "pokeballs" : 2,
        "health_potion" : 1
    }


def get_pokemon_info(pokemon):
    return "{} | lvl {} | hp {}/{}".format(pokemon["name"],
                                           pokemon["level"],
                                           pokemon["current_health"],
                                           pokemon["base_health"])


def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        for index in player_profile["pokemons_inventory"]:
            print("[{}] - {}".format(index, get_pokemon_info(player_profile)))
        try:
              return player_profile["pokemons_inventory"][int(input("Escoge tu pokemon: "))]
        except (ValueError, IndexError):
            print("Opcion Invalida")


def player_attack(player_pokemon, enemy_pokemon):
    #Crear funcion en la que atacas
    pass

def enemy_attack(enemy_pokemon, player_profile):
    # Crear funcion cuando ataca el pokemon contrario
    pass



def fight(player_profile, enemy_pokemon):
    print("*--- NUEVO COMBATE ---*")

    attack_history = []
    player_pokemon = choose_pokemon(player_profile)

    print("{} vs {}".format(player_pokemon["name"], enemy_pokemon["name"]))
    print("Tu pokemon {}\n"
          "Pokemon enemigo{}".format(get_pokemon_info(player_pokemon),
                      get_pokemon_info(enemy_pokemon)))

    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None

        try:
            while action not in [1, 2, 3, 4, 5]:
                action = input("¿Que deseas hacer? \n"
                               "[1] Atacar\n"
                               "[2] Lanzar Pokebola\n"
                               "[3] Dar Pocion Curativa a tu pokemon\n"
                               "[4] Cambiar Pokemon\n"
                               "[5] Huir del combate")
        except (ValueError, IndexError):
            print("Ingrese un dato correcto")


        if action == 1:
            player_attack(player_pokemon, enemy_pokemon)
            # Lista que almacena los ataques realizados en cada pelea
            attack_history.append(player_pokemon)
        elif action == 2:
            capture_with_pokeball(player_profile, enemy_pokemon)
        elif action == 3:
            cure_pokemon(player_pokemon, player_profile)
        elif action == 4:
            choose_pokemon(player_profile)
        elif action == 5:
            run_from_combat()


        enemy_attack(enemy_pokemon, player_profile)


def capture_with_pokeball(player_profile, enemy_pokemon):
    pass


def cure_pokemon(player_pokemon, player_profile):
    pass


def run_from_combat():
    pass


def any_player_pokemon_lives(player_profile):
    return [sum(pokemon["current_health"] for pokemon in player_profile["pokemons_inventory"])] > 0


def main ():
    pokemon_list = get_all_pokemon()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)

    print("Has perdido el combate, tus pokemones no son suficientemente fuertes.")



if __name__ == '__main__':
    main()
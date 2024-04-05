import os
import random
from pprint import pprint
from pokeload import get_all_pokemon_file


def get_player_info(pokemon_list):
    return {
        "name": input("Ingresa tu nombre: "),
        "combats" : 0,
        "pokeballs" : 1,
        "health_potion" : 1,
        "pokemon_inventory" : [random.choice(pokemon_list) for pokemon in range(3)]
    }


def any_pokemon_alive(player_info):
    return sum([pokemon["current_health"] for pokemon in player_info["pokemon_inventory"]]) > 0


def pokemon_presentation(pokemon):
    return ("{} {}| lvl {} | CH: {}/{} | CE: {}".format(pokemon["name"],
                                                          pokemon["type"],
                                                          pokemon["level"],
                                                          pokemon["current_health"],
                                                          pokemon["base_health"],
                                                          pokemon["current_exp"]))

def choose_pokemon(player_info):
    pokemon_chosen = None
    while not pokemon_chosen:
        print("Escoge el Pokemon con el que vas a luchar")
        for index in range(len(player_info["pokemon_inventory"])):
            print("{} - {}".format(index, pokemon_presentation(player_info["pokemon_inventory"][index])))

        try:
            return player_info["pokemon_inventory"][int(input("Escoge un Pokemon: "))]
        except (ValueError, IndexError):
            os.system("cls")
            print("Escoge una opcion Valida")


def chosen_attack(attack):
    return "{} | Damage : {} | Type: {} | MinLevel : {}".format(attack["name"],
                                                                attack["damage"],
                                                                attack["type"],
                                                                attack["min_level"])

def enemy_attack(enemy_pokemon, fighter_pokemon):

    if fighter_pokemon["current_health"] < 0:
        fighter_pokemon["current_health"] = 0

    attack = random.choice(enemy_pokemon["attacks"])
    print("Informacion del ataque enemigo.\n"
          "{}".format(chosen_attack(attack)))

    fighter_pokemon["current_health"] -= int(attack["damage"])

    print("Recibiste {} de daño.".format(int(attack["damage"])))

    print("\nTu pokemon tiene {} de vida".format(fighter_pokemon["current_health"]))



def player_attack(fighter_pokemon, enemy_pokemon):
    if enemy_pokemon["current_health"] < 0:
        enemy_pokemon["current_health"] = 0

    attack_chosen = None
    try:
        while not attack_chosen:
            for index in range(len(fighter_pokemon["attacks"])):
                print("{} - {}".format(index, chosen_attack(fighter_pokemon["attacks"][index])))

            attack_chosen = fighter_pokemon["attacks"][int(input("Escoge un ataque: "))]

    except (ValueError, IndexError):
        print("Escoge una opcion valida")


    enemy_pokemon["current_health"] -= int(attack_chosen["damage"])

    print("El enemigo recibio {} de daño.".format(int(attack_chosen["damage"])))

    print("\nEl pokemon enemigo tiene {} de vida".format(enemy_pokemon["current_health"]))


def player_withdrawal(player_info, enemy_pokemon, fighter_pokemon):
    if player_info["pokeballs"] and player_info["health_potion"] > 0:
        print("Huyes del combate, pero has perdido objetos y tu pokemon ha recibido daño")
        player_info["pokeballs"] -= 1
        player_info["health_potion"] -= 1

    enemy_attack(enemy_pokemon, fighter_pokemon)
    print("Huyes, pero a que costo...")


def cure_pokemon(player_info, fighter_pokemon):
    if fighter_pokemon["current_health"] >= 100:
        print("Tu pokemon ya tiene el maximo de vida")
    else:
        if player_info["health_potion"] > 0:
            fighter_pokemon["current_health"] += 30
            if fighter_pokemon["current_health"] > 100:
                fighter_pokemon["current_health"] = 100
            print("Tu pokemon tiene {} de vida".format(fighter_pokemon["current_health"]))
            player_info["health_potion"] -= 1
        else:
            print("No tienes pociones de curacion.")


def throw_pokeball(player_info, enemy_pokemon, fighter_pokemon):
    if player_info["pokeballs"] > 0:
        if enemy_pokemon["current_health"] <= 20:
            player_info["pokemon_inventory"].append(enemy_pokemon)
            print("Has capturado a {}.\n"
                  "¡FELICIDADES!".format(enemy_pokemon["name"]))
            player_info["pokeballs"] -= 0
        else:
            enemy_attack(enemy_pokemon, fighter_pokemon)
            print("El pokemon enemigo te ha atacado y ha escapado")
            fight(player_info, enemy_pokemon)



def fight(player_info, enemy_pokemon):
    print("\n --- Nuevo Combate ---")
    fighter_pokemon = choose_pokemon(player_info)
    print("\n{} vs {}".format(fighter_pokemon["name"], enemy_pokemon["name"]))


    while any_pokemon_alive(player_info) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in [1, 2, 3, 4, 5]:
            try:
                action = int (input("Escoge tu siguiente movimiento\n"
                               "[1] Atacar\n"
                               "[2] Huir\n"
                               "[3] Dar Pocion de salud a tu pokemon\n"
                               "[4] Lanzar Pokeball\n"
                               "[5] Cambiar Pokemon\n"))

            except (ValueError, IndexError):
                print("Escoge una opcion valida...")

        if action == 1:
            player_info["combats"] += 1
            player_attack(fighter_pokemon, enemy_pokemon)
            enemy_attack(enemy_pokemon, fighter_pokemon)
        elif action == 2:
            player_withdrawal(player_info, enemy_pokemon, fighter_pokemon)
            enemy_attack(enemy_pokemon, fighter_pokemon)
            fight(player_info, enemy_pokemon)
        elif action == 3:
            cure_pokemon(player_info, fighter_pokemon)
        elif action == 4:
            throw_pokeball(player_info, enemy_pokemon, fighter_pokemon)
        elif action == 5:
            fighter_pokemon = choose_pokemon(player_info)

        if fighter_pokemon["current_health"] <= 0 and any_pokemon_alive(player_info):
            fighter_pokemon["current_health"] = 0
            fighter_pokemon = choose_pokemon(player_info)

    if enemy_pokemon["current_health"] <= 0:
        enemy_pokemon["current_health"] = 0
        print("Has Ganado!")
        assign_experience(fighter_pokemon, player_info)


def assign_experience(fighter_pokemon, player_info):
    fighter_pokemon["current_exp"] += 5
    if fighter_pokemon["current_exp"] >= 20:
        fighter_pokemon["current_exp"] = 0
        fighter_pokemon["level"] += 1

    player_info["pokeballs"] += random.randint(0, 1)
    player_info["health_potion"] += random.randint(0, 2)





def main():
    pokemon_list = get_all_pokemon_file()
    player_info = get_player_info(pokemon_list)

    print("HOLA {}, ¡Preparate para el combate!".format(player_info["name"].upper()))
    print("Tus pokemones son:")
    for index in range(len(player_info["pokemon_inventory"])):
        print(pokemon_presentation(player_info["pokemon_inventory"][index]))

    while any_pokemon_alive(player_info):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_info, enemy_pokemon)





if __name__ == '__main__':
    main()
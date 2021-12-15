from enum import IntEnum
import random


class info(IntEnum):
    name = 0
    type = 1
    cr = 2
    stat_url = 3
    goog_url = 4
    cr_num = 5
    biome = 6


def interpret_cr(cr_str):
    cr = cr_str
    if cr_str.find("Unspecified") != -1:
        cr = -1
    if cr_str.find(" or ") != -1:
        cr = cr_str.split(" or ")[0]
    if cr_str.find("/") != -1:
        cr = int(cr_str[0]) / int(cr_str[2])
    cr = float(cr)
    return cr


def fetch_biomes():
    biome_file = open("biomes.txt")
    biome_kvp = []
    for line in biome_file:
        biome_kvp.append(line.split(" = "))
    return biome_kvp


def find_biome_for_monster(name, kvp):
    biome = "NaN"
    for key in kvp:
        if key[0] == name:
            biome = key[1]
    return biome


def fetch_monsters():
    biome_kvp = fetch_biomes()
    file = open("output.txt")

    monster_designator = "<h1 class=\"list-menu-item-heading\">"
    raw = []
    for line in file:
        if line.find(monster_designator) != -1:
            raw.append(line.split(monster_designator))

    monsters = []
    for entry in raw:
        ref = ""
        for monster in entry:
            monster_name = monster.split("</h1><h2 class=\"list-menu-item-label\">")
            if len(monster_name) == 2:
                monster_type = monster_name[1].split("</h2><h2 class=\"list-menu-item-label\">")
                challenge_rating = monster_type[1].split("</h2>")
                google = "https://www.google.com/search?q=dnd+beyond+5e"
                for word in monster_name[0].split(): google += ("+" + str(word))
                cr_num = interpret_cr(challenge_rating[0])
                biome = find_biome_for_monster(monster_name[0], biome_kvp)
                monster_info = (monster_name[0], monster_type[0], challenge_rating[0], ref, google, cr_num, biome)
                monsters.append(monster_info)
                ref = challenge_rating[1].split("href=\"")[1].split("\" class=\"menu")[0]
                ref = "https://www.dndwiki.io" + ref
    return monsters


def sort_monsters(monsters, info_criteria):
    if info_criteria == info.cr:
        info_criteria = info.cr_num
    monsters = sorted(monsters, key=lambda x: x[info_criteria])
    return monsters


def prefilter_monsters_incl(monsters, field, only_include):
    filtered_monsters = []
    for monster in monsters:
        if monster[field].find(str(only_include)) != -1:
            filtered_monsters.append(monster)
    return filtered_monsters


def prefilter_monsters_excl(monsters, field, only_include):
    filtered_monsters = []
    for monster in monsters:
        if monster[field].find(str(only_include)) == -1:
            filtered_monsters.append(monster)
    return filtered_monsters


def cr_filter_below(monsters, cr_num):
    filtered_monsters = []
    for monster in monsters:
        if monster[info.cr_num] <= cr_num:
            filtered_monsters.append(monster)
    return filtered_monsters


def cr_filter_exactly(monsters, cr_num):
    filtered_monsters = []
    for monster in monsters:
        if monster[info.cr_num] == cr_num:
            filtered_monsters.append(monster)
    return filtered_monsters


def cr_filter_range(monsters, lower, upper):
    filtered_monsters = []
    for monster in monsters:
        if lower <= monster[info.cr_num] <= upper:
            filtered_monsters.append(monster)
    return filtered_monsters


def print_all_monsters(monsters):
    for monster in monsters:
        for attribute in monster:
            print(attribute)
        print()
    return 0


def print_random_monster(monsters):
    i = random.randint(0, len(monsters) - 1)
    for attribute in monsters[i]:
        print(attribute)
    return 0


def main():
    # Necessary:
    monsters = fetch_monsters()

    # OPTIONAL FILTERS:======================================================================
    # only include the following
    monsters = prefilter_monsters_incl(monsters, info.biome, "NaN")

    # add the following
    monsters += prefilter_monsters_incl(monsters, info.type, "something overly specific to exclude")

    # remove any of the following
    monsters = prefilter_monsters_excl(monsters, info.type, "something overly specific to exclude")
    # =======================================================================================

    # CHALLENGE RATING FILTERS:==============================================================
    lower = 0
    exactly = 0
    range_m = 1

    cr_filter = 1.0
    range_upper = 0.25
    range_lower = 0
    # show monsters of CR or lower:
    if lower == 1:
        monsters = cr_filter_below(monsters, cr_filter)

    # show monsters of exactly CR:
    if exactly == 1:
        monsters = cr_filter_exactly(monsters, cr_filter)

    # show monsters between CR of lower and upper (inclusive):
    if range_m == 1:
        monsters = cr_filter_range(monsters, range_lower, range_upper)
    # =======================================================================================

    # SORTING FILTERS:=======================================================================
    # Sort list by name alphabetically first
    monsters = sort_monsters(monsters, info.name)
    # Sort by CR second
    monsters = sort_monsters(monsters, info.cr)
    # =======================================================================================

    # OUTPUT FILTERS:========================================================================
    all_monsters = 1
    random_monsters = 1

    # print all monsters
    if all_monsters == 1:
        print_all_monsters(monsters)
    # print a random monster from the selection
    if random_monsters == 1:
        print_random_monster(monsters)
    # =======================================================================================
    fetch_biomes()
    return 0


if __name__ == '__main__':
    main()

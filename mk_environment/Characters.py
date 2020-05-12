from enum import Enum
# An enumerable class used to specify which character can be used to interact with a game
class Characters(Enum):
    # Starting roster ( reptile,shang,goro?maybe later if at all.)

    SCORPION = "SCORPION"
    SUBZERO = "SUBZERO"
    LIUKANG = "LIUKANG"
    RAIDEN = "RAIDEN"
    SONYA = "SONYA"
    JOHNNY = "JOHNNY"
    KANO = "KANO"
#usage -> print(Characters["SCORPION"].value)
#x = "SCORPION"
#print(Characters[x])


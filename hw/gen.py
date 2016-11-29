import os
import textwrap
from main.models import Team 
import random

path = 'main/static/images/pokemons'

countries = [
    "Russia",
    "USA",
    "Italia",
    "Spain",
    "Germany",
    "Australia"
]

sportTypes = [
    "Football",
    "PokemonBall",
    "Golf",
    "Sleeping"
]

def fix():
    images = list(filter( lambda x : "jpg" in x , next(os.walk(path))[2]))
    for i in Team.objects.all():
        i.imageUrl = "images/pokemons/" + random.choice(images)
        i.save()

def generate():
    with open(os.path.join(path, 'names.txt'), "r") as file:
        names = file.read().split('\n')

    # print(names)

    with open(os.path.join(path, 'descs.txt'), "r") as file:
        descs = textwrap.wrap(file.read(), 200)

    # print ( descs )

    images = list(filter( lambda x : "jpg" in x , next(os.walk(path))[2]))

    print(images)

    for i in range(1000):
        t = Team()
        t.name = random.choice(names)
        t.country = random.choice(countries)
        t.sportType = random.choice(sportTypes)
        t.imageUrl = "images/pokemons" + random.choice(images)
        t.desc = random.choice(descs)
        t.prizeCount = random.randrange(2, 999)
        t.save()
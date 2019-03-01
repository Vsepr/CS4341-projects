# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
from testcharacter import TestCharacter

# Create the game
# random.seed(312) # TODO Change this if you want different random choices
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("monster", # name
                                    "M",       # avatar
                                    3, 9,      # position
                                    1          # detection range
))

# TODO Add your character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
# g.go()


counter = 0
for x in range(10):
    # Create the game
    random.seed(x) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(SelfPreservingMonster("monster",  # name
                                        "M",  # avatar
                                        3, 9,  # position
                                        1  # detection range
                                        ))

    # TODO Add your character
    g.add_character(TestCharacter("me",  # name
                                  "C",  # avatar
                                  0, 0  # position
                                  ))

    # Run!
    g.go()
    for events in g.world.events:
        if "found the exit" in str(events):
        # if str(events).contains("found the exit"):
            print('TRUEAEEEEEEEE MOFOOOOOOOO')
            counter += 1
print("We won [{}] amount of times".format(counter))

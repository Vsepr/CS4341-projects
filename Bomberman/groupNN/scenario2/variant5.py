# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../groupNN')
# from testcharacter import TestCharacter
from scenario2Character import TestCharacter

# Create the game
# random.seed(123) # TODO Change this if you want different random choices
random.seed(1) # WE LOOOOOOOOOOSE
# random.seed(2) # WE LOOOOOOOOOOSE
# random.seed(3) # TODO Change this if you want different random choices
# random.seed(4) # TODO Change this if you want different random choices
# random.seed(5) # TODO Change this if you want different random choices
# random.seed(6) # TODO Change this if you want different random choices
# random.seed(7) # TODO Change this if you want different random choices
# random.seed(8) # LOOOOOOOOOOOOOOOSE
# random.seed(9) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(StupidMonster("monster", # name
                            "S",       # avatar
                            3, 5,      # position
))
g.add_monster(SelfPreservingMonster("monster", # name
                                    "A",       # avatar
                                    3, 13,     # position
                                    2          # detection range
))

# TODO Add your character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
# g.go()


counter = 0
for x in range(100):
    # Create the game
    random.seed(x) # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("monster",  # name
                                "S",  # avatar
                                3, 5,  # position
                                ))
    g.add_monster(SelfPreservingMonster("monster",  # name
                                        "A",  # avatar
                                        3, 13,  # position
                                        2  # detection range
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

# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import operator


class TestCharacter(CharacterEntity):
    def do(self, wrld):
        # Your code here

        # Initialize some variables that we are going to be using at each iteration of the board as it is
        # being played.
        goal = self.get_exit(wrld)
        start = self.get_my_location(wrld)
        bomb = self.get_bomb(wrld)
        # Just returns the direction that you would want to move if only trying to move away from corners.
        x_dir, y_dir = self.get_direction(start, wrld)
        # Returns the x and y coordinates, as a tuple, so that we can determine the next best move based on our
        # searching algorithm
        next_move = self.a_star(wrld, start, goal, 0)

        # The next best position - current position = (dx, dy) to move to get to the next best position
        try:
            dx = next_move[0] - start[0]
            dy = next_move[1] - start[1]
        except TypeError:
            pass
        # Monsters are within a range that you should run from.
        # If monsters are determined to be within this range, we will override the current best
        # direction to move, and instead of aiming to get to the exit portal in the fastest manner,
        # we will be working on attempting to place bombs and run away from the monster.
        run_from_monster = self.check_monster(start, wrld, 3)

        try:
            # If there is a monster in a given radius around us:
            if run_from_monster:
                print("STATE: MONSTER")
                # STATE: MONSTER ( There are a monsters within our range)
                # Place bomb and hope it dies
                self.place_bomb()
                # Determining best move away from monster
                monster_move_away = self.a_star(wrld, start, run_from_monster[0], -1)
                dx = monster_move_away[0] - start[0]
                dy = monster_move_away[1] - start[1]
                if dy > 1 or dx > 1 or dx < -1 or dy < -1:
                    dx = 0
                    dy = 0
                self.move(dx, dy)
            # If the next best move is a wall:
            elif wrld.wall_at(*next_move):
                print("STATE: AWAY FROM CORNERS")
                # Move away from boundaries
                self.move(x_dir, y_dir)
            # If the next move location is in the line of sight (los) of a bomb, or there is an explosion
            # at the location of the next move and during the next board iteration: CHECK THIS IN TESTING
            elif next_move[0] == bomb[0] or next_move[1] == bomb[1] or wrld.next()[0].explosion_at(*next_move):
                print("STATE: BOMB / EXPLOTION")
                # If there is a bomb in the current line of site of the character, and there is not an explosion next
                # iteration of the board at the location we wish to go to:
                if bomb[0] == start[0] or bomb[1] == start[1]:
                    bomb_move_away = self.a_star(wrld, start, bomb, -1)
                    dx = bomb_move_away[0] - start[0]
                    dy = bomb_move_away[1] - start[1]
                    if dy > 1 or dx > 1 or dx < -1 or dy < -1:
                        dx = 0
                        dy = 0
                    self.move(dx, dy)
                else:
                    self.move(0, 0)

                # todo how does code gets in here if run_from_monster is going to be empty in the bomb case. Shouldnt this case come first??
                if run_from_monster:
                    print("I am doing A* away from Bomb")
                print("THIS IS THE MONSTER I FOUND WHEN IN BOMB STATE: ")
                print(run_from_monster[0])
                monster_move_away = self.a_star(wrld, start, run_from_monster[0], -1)
                dx = monster_move_away[0] - start[0]
                dy = monster_move_away[1] - start[1]
                self.move(dx, dy)
            else:
                print("STATE: A* MODE")
                self.move(dx, dy)
                if wrld.wall_at(start[0], start[1] + 1) or wrld.wall_at(start[0], start[1] - 1):
                    self.place_bomb()
                elif wrld.wall_at(start[0]+1, start[1]) or wrld.wall_at(start[0]-1, start[1]):
                    self.place_bomb()
        except (IndexError, TypeError):
            pass

    # Checks if there are monsters within a program specified radius of your character
    # Puts these locations into a list, returns this list of monster locations
    @staticmethod
    def check_monster(start, wrld, radius):
        monsters_near = []
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                if wrld.next()[0].monsters_at(start[0] + x, start[1] + y):
                    # monster was found
                    monsters_near.append((start[0] + x, start[1] + y))
        return monsters_near

    # Gets the direction to move if you want to move opposite the closest boundaries
    # Useful in some cases for evading getting cornered.
    @staticmethod
    def get_direction(start, wrld):
        x = 1
        y = 1
        if start[0] > wrld.width()/2:
            x = -1
        if start[1] > wrld.height()/2:
            y = -1
        return x, y

    # Find the exit on the map, return the coordinates of the map
    @staticmethod
    def get_exit(wrld):
        # Find the exit to use for heuristic A*
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.exit_at(x, y):
                    return x, y
        return -1, -1

    # Find the bomb on the map (assumed only one), return the coordinates of the bomb
    @staticmethod
    def get_bomb(wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.bomb_at(x, y):
                    return x, y
        return -1, -1

    # Find your current location on the map, return the coordinates
    @staticmethod
    def get_my_location(wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.characters_at(x, y):
                    return x, y

    # Determining the heuristic value, being Euclidean Distance between the two coordinates given
    @staticmethod
    def heuristic(start, goal):
        (x1, y1) = start
        (x2, y2) = goal
        value = (x2 - x1)**2 + (y2 - y1)**2
        return value

    # A* Algorithm which will be used to determine and return the best move coordinates
    def a_star(self, wrld, start, goal, min_max):  # Min/max; 0 min 1 max
        # Find all possible moves from the current position.
        neighbors = self.get_neighbors(start, wrld)
        neighbors_values = []
        # For all valid neighbors to your current position, add them to the neighbor list
        # alongside their heuristic evaluation
        for neighbor in neighbors:
            neighbors_values.append((neighbor[0], neighbor[1], self.heuristic(neighbor, goal)))
        # Sort the neighbor list, in accordance to their heuristic value
        neighbors_values.sort(key=operator.itemgetter(2))

        # List of places to move to, assuming we are running away from a point
        # not attempting to get closer to a point. Used for running away from monsters/bombs
        runaway_list = []
        # if min_max = 0, we are trying to GET to our goal, not run away
        if min_max == 0:
            try:
                # return the tuple of the best possible space to be in next
                return neighbors_values[0][0], neighbors_values[0][1]
            except IndexError:
                pass
        # If we are trying to run away:
        else:
            # todo this seems to be returning walls as possible moves too
            # Loop through neighbors, do not include neighbor locations that will put you against a wall,
            # or an explosion
            for neighbor in neighbors_values:
                if neighbor[0] != wrld.width() and neighbor[1] != wrld.height \
                        and neighbor[0] != 0 and neighbor[1] != 0 and not \
                        wrld.next()[0].explosion_at(neighbor[0], neighbor[1]):
                    runaway_list.append(neighbor)
            try:
                # If there are no places to run to, pray and stay still
                if not runaway_list:
                    return 0, 0
                # Else, return the last element that was added, as this has the highest value, which we are looking
                # for when running away rather than moving towards
                return runaway_list[-1][0], runaway_list[-1][1]
            except IndexError:
                pass

    # Gets all neighbors in all possible move spaces. Does not add any spaces that are out bounds,
    # a wall, or an explosion/bomb.
    @staticmethod
    def get_neighbors(start, wrld):
        x = start[0]
        y = start[1]
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),
                     (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        result = []
        # check that neighbors are inside wrld bounds
        for neighbor in neighbors:
            if 0 <= neighbor[0] < wrld.width() and 0 <= neighbor[1] < wrld.height():
                if not wrld.wall_at(*neighbor) and not wrld.bomb_at(*neighbor) \
                        and not wrld.next()[0].next()[0].explosion_at(*neighbor):
                    result.append(neighbor)
        return result

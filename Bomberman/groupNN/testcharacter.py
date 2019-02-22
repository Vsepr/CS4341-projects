# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import heapq
import operator


class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        # self.move(1, 0)

        goal = self.get_exit(wrld)
        start = self.get_my_location(wrld)

        # if self.check_monster(start, 2, wrld): # if list empty returns false
        #     print("fukkkk")
        # else:
        #     nextMove = self.a_star(wrld, start, goal) # returns (x,y) coordinate of next move
        nextMove = self.a_star(wrld, start, goal)  # returns (x,y) coordinate of next move
        print("my start move is:")
        print(start)
        print("my next move is:")
        print(nextMove)
        dx = nextMove[0] - start[0]
        dy = nextMove[1] - start[1]
        print("my dx is {} and my dy is: {}".format(dx,dy))
        try:
            if wrld.wall_at(nextMove[0], nextMove[1]):
                # do stuff with wall
                # put  - 11 ticks to explode
                # move diagonally

                # wallNeighbors = []
                # if wrld.wall_at(start[0] +1, start[1]):
                #     if wrld.wall_at(start[0], start[1] + 1):
                #         self.place_bomb()
                #         self.move(-1, -1)
                #         #move back
                #     else:
                #         self.move(0, 1)
                #         self.place_bomb()
                #         self.move(0, -1)
                # else:
                #     self.move(1,0)
                #     self.place_bomb()
                #     self.move(-1, 0)

                # start = (start[0] + dx, start[1] + dy)

                if (nextMove[0] + 1) >= wrld.width() and wrld.bomb_at(start[0], start[1]):
                    self.move(-1, -1)

                if not (nextMove[0] + 1) >= wrld.width() and wrld.bomb_at(start[0], start[1]):
                    self.move(1, -1)

                self.place_bomb()
            else:
                # there is no wall
                if wrld.bomb_at(nextMove[0], nextMove[1]) or wrld.explosion_at(nextMove[0], nextMove[1]):
                    self.move(0, 0)
                else:
                    start = (start[0] + dx, start[1] + dy)
                    self.move(dx, dy)

            print(start[0], start[1], nextMove[0], nextMove[1])
        except IndexError:
            pass

    def check_monster(self, start, radius, wrld):
        monstersList = [] # list of monsters within our radious
        for x in range(-radius, radius):
            for y in range(-radius,radius):
                if wrld.monsters_at(start[0]+x, start[1]+y):
                    monstersList.append((start[0]+x, start[1]+y))
        return monstersList

    def check_wall(self, start, radius, wrld):
        wallList = [] # list of monsters within our radious
        for x in range(-radius, radius):
            for y in range(-radius,radius):
                if wrld.wall_at(start[0]+x, start[1]+y):
                    wallList.append((start[0]+x, start[1]+y))
        return wallList




    @staticmethod
    def get_exit(wrld):
        # Find the exit to use for heuristic A*
        for x in range(wrld.width()):
            for y in range(wrld.height()):
                if wrld.exit_at(x, y):
                    return x, y
        pass

    # @staticmethod
    # def make_graph(wrld):
    #     graph_wrld = [wrld.width][wrld.height]
    #
    #     for i in range(0, wrld.width):
    #         for j in range(0, wrld.height):
    #             if wrld(i, j)

    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of current position in board
    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # RETURN [list of (int x, int y)]: coordinate positions of neighbors, it doesn't return a neighbor that has a
    def get_neighbors(self, start, wrld):
        x = start[0]
        y = start[1]
        neighbors = [(x+1, y), (x, y-1), (x-1, y), (x, y+1),
                     (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
        result = []
        # check that neighbors are inside wrld bounds and are not walls
        for neighbor in neighbors:
            if 0 <= neighbor[0] < wrld.width() and 0 <= neighbor[1] < wrld.height():
                result.append(neighbor)
        return result

    @staticmethod
    def get_my_location(wrld):
        # Find the exit to use for heuristic A*
        for x in range(0, wrld.width()):
            for y in range(0, wrld.height()):
                if wrld.characters_at(x, y):
                    return x, y

    # Determining the heuristic value, being Euclidean Distance
    # @staticmethod
    def heuristic(self, start, goal, wrld):
        (x1, y1) = start
        (x2, y2) = goal

        # Euclidean distance is the hypotenuse
        # We add the squared values, and finding the sqrt is
        # not necessary as it will never effect the outcome
        value = (x2 - x1)**2 + (y2 - y1)**2
        penalty = 0
        if self.check_monster(start, 2, wrld):
            penalty = +5000
        if self.check_wall(start,1,wrld):
            penalty = +5000

        return value + penalty

    # PARAM [SensedWorld] wrld: wrld grid, used to get boundries
    # PARAM [tuple (int, int)] start: tuple with x and y coordinates of starting position in board
    # PARAM [tuple (int, int)] goal: tuple with x and y coordinates of exit position in board
    # RETURN [?????]: Possibly return list with tuples of (int, int). This would be the optimal path to traverse
    def a_star(self, wrld, start, goal):
        neighbors = self.get_neighbors(start, wrld)
        neighbors_values = []
        for neighbor in neighbors: # shouldn't this be for neighbor in neighbors: ???s
            neighbors_values.append((neighbor[0], neighbor[1], self.heuristic(neighbor, goal, wrld)))
        neighbors_values.sort(key=operator.itemgetter(2))
        print(neighbors_values)

        return neighbors_values[0][0], neighbors_values[0][1]

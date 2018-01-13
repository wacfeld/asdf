# when a car is on a lane, it behaves like in a list, however it starts getting precise motion
# when it goes into the center


class Portal:  # called Portal because cars start and end here, appearing and disappearing (there are multiple portals)
    def __init__(self, inter):  # the intersection it feed into; not road becase roads don't have an adjacent field
        self.cars = []
        self.adjintersection = inter

    def createcar(self):
        newcar = Car()
        self.cars.append(newcar)

    adjintersection = None
    location = None
    cars = None


class Car:
    def __init__(self):
        # cars spawn in Portals which are adjacent to the outer intersections

        self.state = "d"
        self.coords = [None, None]
        self.motionvector = [None, None]
        self.portal = True

    @staticmethod
    def decidedestination(startcoords):
        # TODO: figure out how this works
        return 'dummy data'

    inportal = None
    state = None  # state can be either in a lane (digital) or in the middle of an intersection (analog)
    turning = None  # 'left', 'forward', 'right'
    destination = None  # which portal it wants to get to; decided by MindController

    # these only apply when in analog state
    coords = None  # (0,0) is center of intersection, x moves right, y moves up
    motionvector = None  # TODO: decide if this should be a vector, or direction and velocity


class Lane:
    def __init__(self, d, parent):  # direction is l, r, or f for left, right, forward
        self.cars = []
        self.direction = d
        self.parentroad = parent

    def numberofcars(self):
        return len(self.cars)

    capacity = None  # how many cars it can hold; right and left are less, forward is more
    # TODO: (see comment above) figure out exact numbers

    direction = None
    parentroad = None
    cars = None  # first in the array are closest to middle of intersection


class Road:
    # The number of intersections varies, but not the number of lanes
    # note that intersections at the edge still have 4 roads

    def __init__(self):
        self.left = Lane('l', self)
        self.forward = Lane('f', self)
        self.right = Lane('r', self)
        self.crossng = ZebraCrossing(self)

    left = None
    forward = None
    right = None
    size = None  # how many cars it can hold; how far a car has to travel (digitally) to get to the middle
    crossing = None  # a ZebraCrossing; placed here for easy access from cars


class Middle:
    # the middle of the intersection; split up into nxn squares
    # n must be even to evenly split up the roads leading in and out
    # TODO: ^ decide what n is

    def __init__(self, s, parent):  # s is side length
        self.size = s
        self.squares = [[None]*s]*s
        self.parent = parent

    size = None
    squares = None
    parent = None


class Pedestrian:
    # sole purpose is to spawn and 'walk' across an intersetion
    # walking is a digital task, so they have no location; see ZebraCrossing

    def __init__(self):
        self.walking = False

    def startwalking(self, intersection):
        pass

    walking = None


class ZebraCrossing:
    # where pedestrians cross; pedestrians do not move, but take x time to cross
    # since by law you aren't allowed to drive if the pedestrians are anywhere on the pavement
    # belongs to Road object

    def __init__(self, parent):  # parent is a Road
        self.occupied = False
        self.numberofpedestrians = 0
        self.parentroad = parent

    def checkoccupied(self):  # called by pedestrian before and after crossing
        if not self.numberofpedestrians:
            self.occupied = False
        else:
            self.occupied = True

    # when a pedestrian is crossing it adds 1 to numberofpedestrians, when it leaves it subtracts 1
    # the crossing checks when numberofpedestrians == 0 and then it becomes not occupied
    numberofpedestrians = None
    occupied = None
    parent = None


class Light:  # applies to traffic and pedestrian lights, since they are effectively the same, except in timing
    def __init__(self, parent):  # will figure out parenttype on its own
        self.state = 'r'  # not random chance because it's up to the NN to change this
        self.parenttype = 'z' if type(parent) is ZebraCrossing else 'r'
        self.parent = parent

    # either 'z' for zebra crossing, or 'r' for road
    parenttype = None  # we can infer the light type from this
    parent = None  # either Road or ZebraCrossing
    state = None  # can be 'r', 'y', 'g','l', last one means left turning, doesn't apply for pedestrian lights


class Intersection:
    # an intersection consists of 4 roads and a middle; everything else is contained inside the roads
    # intersections do NOT have roads leading out of them, only in
    # once a car goes through, it immediately transfers to the next intersection

    # whichroads is a string of 4 1s and 0s telling you what roads are active, going clockwise
    # note that an inactive road is not necessarily an edge road, since the edges typically have roads for the portals
    # adj always is a tuple of 4 since if it's on the edge it has portals
    def __init__(self, adj, whichroads):
        self.adjacents = adj
        self.initroads(whichroads)
        self.middle = Middle(5, self)  # TODO: change 5 to something else

    @classmethod
    def initwithoutadjacents(cls, whichroads):  # still has roads because everything must have at least 1 road!
        cls.adjacents = (None, None, None, None)
        cls.initroads(whichroads)

    def initroads(self, whichroads):  # called by __init__ and initwithoutadjacents to save room
        self.roads = []
        for b in whichroads:  # b for boolean
            if int(b):
                newroad = Road()
                self.roads.append(newroad)
            else:
                # TODO: figure out, should this append None, or an inactive road?
                # (if it's the latter we would make that a parameter for the constructor)
                # in fact, unless we are actually going to remove random roads,
                # this might not even be necessary
                self.roads.append(None)

    # these are the roads, or portals, adjacent to this intersection
    # after everything is complete adjacents should always be a tuple of 4 because the edges have portals
    adjacents = None
    roads = None  # these are ordered up, right, down, left - clockwise
    middle = None

    # note that lights do NOT correspond to the opposite road, rather, a light on road X controls road X


class MindController:
    # this controls all the interactions of the simulation, aside from controlling the traffic lights
    # makes does things like make cars move, spawn
    # also monitors stuff like downtime
    # TODO: finish this
    pass


def main():
    print("Program start")


if __name__ == "__main__":
    main()

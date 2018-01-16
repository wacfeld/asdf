class Portal:  # called Portal because cars/pedestrians start and end here (there are multiple portals)
    # attaches to road of intersection
    # cars coming from the intersection go directly from Middle to Portal

    def __init__(self, road):
        self.cars = []
        self.peds = []
        self.adjroad = road  # the road it feeds into

    # TODO: should we merge cars and peds into one list (as well as the functions)?

    def createcar(self):
        newcar = Car(self)
        self.cars.append(newcar)
        return newcar  # gives car to MindController, the one that calls the function and decides the car's destination

    def createped(self):  # basically same as createcar()
        newped = Pedestrian(self)
        self.peds.append(newped)
        return newped

    def deletecar(self, c):  # removes car forever
        del self.cars[self.cars.index(c)]  # get index of c in cars, then delete that element

    def deleteped(self, p):
        del self.peds[self.peds.index(p)]


class Car:
    def __init__(self, p):
        # cars spawn in Portals which are adjacent to the outer intersections
        # location == 'l', 'p' is digital; 'm' is analog
        # when turning cars follow a rough circle

        self.parent = p  # either Portal, Lane, or Middle; this also tells us how it should behave
        # ^cars are always in a digital state

        self.location = 'p'  # 'l', 'm', 'p' for Lane, Middle, Portal; also doubles as parent
        self.destination = None  # the portal it wants to get to

        # these only apply when in the middle of an intersection
        self.coords = [None, None]  # (0,0) is center of Intersection, x moves right, y moves up
        self.motionvector = [None, None]  # where it moves next in the Intersection; might change to direction and angle


class Lane:
    def __init__(self, d, parent, c):
        self.cars = []  # first in the array are closest to middle of intersection
        self.direction = d  # direction is l, r, or f
        self.parentroad = parent
        self.capacity = c  # how many cars it can hold; right and left are less, forward is more
        # TODO: figure out eact numbers for capacity


class Road:
    # TODO: should the number of lanes be 2 or 3? and should it change?
    # note that intersections at the edge still have 4 roads (1 or two are technically Portals)

    def __init__(self):
        self.left = Lane('l', self)
        self.forward = Lane('f', self)
        self.right = Lane('r', self)

        self.crossing = ZebraCrossing(self)  # a ZebraCrossing; placed here for easy access from cars
        self.light = Light(self)  # note that lights control the road they belong to, not the opposite!


class Middle:
    # the middle of the intersection; split up into nxn squares
    # n must be even to evenly split up the roads leading in and out
    # certain square are special; e.g. some are places a car can leave or enter an intersection
    # TODO: ^ decide what n is

    def __init__(self, s, parent):  # s is side length
        self.size = s
        self.squares = [[None]*s]*s
        self.parent = parent


class Sidewalk:
    # small square at the four corners of intersections, where pedestrians stay when not crossing roads
    def __init__(self, p, c1, c2):
        self.parent = p

        self.peds = []
        self.crossing1, self.crossing2 = c1, c2


class Pedestrian:
    # sole purpose is to spawn and occupy an intersection for x time
    # walking is a digital task
    # different pedestrians have different walking speeds
    # when a pedestrian walks it occupies, the crossing, stays on the same sidewalk,,
    # then after x time goes to the other sidwalk and unoccupies the crossing

    def __init__(self, p):
        self.walkingspeed = self.decidewalkingspeed()
        self.parent = p

    @staticmethod
    def decidewalkingspeed():
        # TODO: figure this out
        return 10

    def startwalking(self, intersection):
        # TODO: figure this out
        pass


class ZebraCrossing:
    # where pedestrians cross; pedestrians do not move, but take x time to cross
    # since by law you aren't allowed to drive if the pedestrians are anywhere on the pavement
    # belongs to Road object

    def __init__(self, parent):  # parent is a Road
        self.occupied = False
        self.numberofpedestrians = 0
        self.light = Light(self)

        self.parentroad = parent

        # where pedestrians stand
        self.sidewalk1 = None  # will initiate after ZebraCrossing is created
        self.sidewalk2 = None

        self.pedlight = Light(self)

    def checkoccupied(self):  # called by pedestrian before and after crossing
        if not self.numberofpedestrians:
            self.occupied = False
        else:
            self.occupied = True

    # when a pedestrian is crossing it adds 1 to numberofpedestrians, when it leaves it subtracts 1
    # the crossing checks when numberofpedestrians == 0 and then it becomes not occupied
    light = None
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
    def __init__(self, whichroads):
        self.adjacents = [None] * 4  # roads/portals adjacent to this intersection
        self.middle = Middle(5, self)  # TODO: change 5 to something else

        # creates sidewalks, which then get attached to zebracrossings in roads

        # initiates roads
        # roads are ordered clockwise
        self.roads = []
        for b in whichroads:  # b for boolean
            if int(b):
                newroad = Road()

                self.roads.append(newroad)
            else:
                self.roads.append(None)

        # set the crossings corresponding to sidewalks
        s1 = Sidewalk(self, self.roads[0], self.roads[1])
        s2 = Sidewalk(self, self.roads[1], self.roads[2])
        s3 = Sidewalk(self, self.roads[2], self.roads[3])
        s4 = Sidewalk(self, self.roads[3], self.roads[1])

        # set the sidewalks corresponding to crossings
        self.roads[0].crossing.s1 = s1
        self.roads[1].crossing.s1 = s2
        self.roads[2].crossing.s1 = s3
        self.roads[3].crossing.s1 = s4

        self.roads[0].crossing.s2 = s2
        self.roads[1].crossing.s2 = s3
        self.roads[2].crossing.s2 = s4
        self.roads[3].crossing.s2 = s1


class MindController:
    # this controls all the interactions of the simulation, aside from the traffic lights
    # does things like make cars move, spawn, etc.
    # for convenience

    def __init__(self, s):
        self.sidelength = s  # not including Portals
        self.intersections = [[None] * s] * s

    def initinter(self, s):
        for y in range(s):  # y goes top to bottom
            for x in range(s):  # x goes left to right
                self.intersections[y][x] = Intersection('1111')

        # need to do this twice to set the adjacent property
        for y in range(s):
            for x in range(s):
                inter = self.interseceions[y][x]
                coords = [[x, y-1], [x+1, y], [x, y+1], [x-1, y]]
                for adjcoord in coords:
                    if (not adjcoord[0] in range(s)) or (not adjcoord[1] in range(s)):  # then we create a portal
                        a = adjcoord[0]  # shorter
                        b = adjcoord[1]
                        road = inter.roads[0] if a < y else inter.roads[1] if x < b else inter.roads[2] if y < a else \
                            inter.roads[3]
                        portal = Portal(road)
                        inter.adj[coords.index([a, b])] = portal
                    else:
                        inter.adj[coords.index([a, b])] = self.intersections[b][a]


def main():
    print('Program start')


if __name__ == '__main__':
    main()

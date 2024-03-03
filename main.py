# Pygame Graphics engine from scratch
# Made by Elliott Faa and Asanshay Gupta, 2023

import pygame
import math
from pygame import gfxdraw
import numpy
from operator import itemgetter

# screen variables
screenWidth = 1280
screenHeight = 720

# simulation variables
simSpeed = 60

# camera variables
cameraPos = (0, 0, 1.2)
cameraAngle = (1, 1, 0)
FOV = 180
cameraPanSpeed = 0.02
cameraMoveSpeed = 0.1

# object variables
objects = []


# main object(s)
def create_object(points, connections, surfaces, color, drawPoints):
    """
    Creates an object to display in the 3D environment
    :param points: List of tuples (x, y, z) representing points in the array
    :param connections: List of tuples (i, j) representing lines between the ith and jth element in `points`
    :param surfaces: List of tuples (p1, p2, p3...) representing surfaces with vertices as the p1th, p2th... element of points
    :param color: Tuple (r, g, b) representing the color of the object
    :param drawPoints: Whether to draw the points as circles
    :return: void
    """
    objects.append((points, connections, color, drawPoints, surfaces))


# tetrahedron thingy
create_object(
    [(5, 5, 0), (5, 6, 0), (6, 5, 0), (5, 5, 2)],  # points
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],  # connections
    [(1, 2, 3)],  # surfaces
    (42, 157, 143),  # color
    True  # drawPoints
)

# cube
create_object(
    [(4, 6, 0), (4, 5, 0), (3, 6, 0), (3, 5, 0), (4, 6, 0.75), (4, 5, 0.75), (3, 6, 0.75), (3, 5, 0.75)], # points
    [(0, 1), (0, 2), (3, 1), (3, 2), (4, 5), (4, 6), (7, 5), (7, 6), (0, 4), (1, 5), (2, 6), (3, 7)], # connections
    [(2, 3, 7, 6), (0, 1, 4), (0, 1, 3, 2)], # surfaces
    (231, 111, 81),
    True
)

# pyramid?
create_object(
    [(2, 2, 0), (4, 2, 0), (4, 4, 0), (2, 4, 0), (3, 3, 2)],  # points: base corners and apex
    [(0, 1), (1, 2), (2, 3), (3, 0),  # base edges
     (0, 4), (1, 4), (2, 4), (3, 4)],  # side edges connecting base to apex
    [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)],  # surfaces: each triangle side
    (255, 215, 0),  # color: golden
    True  # drawPoints: yes
)

# house
create_object(
    [
        (1, 1, 0),  # 0 Front bottom left
        (1, 3, 0),  # 1 Front bottom right
        (0, 3, 0),  # 2 Back bottom right
        (0, 1, 0),  # 3 Back bottom left
        (1, 1, 2),  # 4 Front top left
        (1, 3, 2),  # 5 Front top right
        (0, 3, 2),  # 6 Back top right
        (0, 1, 2),  # 7 Back top left
        (0.5, 2, 3), # 8 Roof peak
    ],
    [  # Edges
        (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom square
        (4, 5), (5, 6), (6, 7), (7, 4),  # Top square
        (0, 4), (1, 5), (2, 6), (3, 7),  # Vertical lines
        (4, 8), (5, 8), (6, 8), (7, 8),  # Roof lines
    ],
    [  # Surfaces
        (0, 1, 5, 4),  # Front wall
        (1, 2, 6, 5),  # Right wall
        (2, 3, 7, 6),  # Back wall
        (3, 0, 4, 7),  # Left wall
        (4, 5, 8), (5, 6, 8), (6, 7, 8), (7, 4, 8)  # Roof surfaces
    ],
    (124, 252, 0),  # color: Lawn green for a vibrant look
    True  # drawPoints: yes, to highlight the structure's corners
)






# horizontal plane
points = []
connections = []
color = (255, 255, 255)
drawPoints = False

numberOfPlaneLines = 50
spacingOfPlaneLines = 1
for i in range(numberOfPlaneLines // 2):
    points.append((numberOfPlaneLines // 2 * spacingOfPlaneLines, i * spacingOfPlaneLines, 0))
    points.append((-numberOfPlaneLines // 2 * spacingOfPlaneLines, i * spacingOfPlaneLines, 0))
    connections.append((8 * i, 8 * i + 1))
    points.append((numberOfPlaneLines // 2 * spacingOfPlaneLines, -i * spacingOfPlaneLines, 0))
    points.append((-numberOfPlaneLines // 2 * spacingOfPlaneLines, -i * spacingOfPlaneLines, 0))
    connections.append((8 * i + 2, 8 * i + 3))
    points.append((i * spacingOfPlaneLines, numberOfPlaneLines // 2 * spacingOfPlaneLines, 0))
    points.append((i * spacingOfPlaneLines, -numberOfPlaneLines // 2 * spacingOfPlaneLines, 0))
    connections.append((8 * i + 4, 8 * i + 5))
    points.append((-i * spacingOfPlaneLines, numberOfPlaneLines // 2 * spacingOfPlaneLines, 0))
    points.append((-i * spacingOfPlaneLines, -numberOfPlaneLines // 2 * spacingOfPlaneLines, 0))
    connections.append((8 * i + 6, 8 * i + 7))
objects.append((points, connections, color, drawPoints))

# extra object (for diagnostics)
points = [(10, 10, 0), (10, 15, 0)]
connections = [(0, 1)]
drawPoints = True
color = (255, 0, 0)
# objects.append((points, connections, color, drawPoints))

# processed variables
horizontalRotation = math.atan(cameraAngle[1] / cameraAngle[0])
verticalRotation = 0
FOV = FOV / 180 * math.pi
horizontalRotationSpeed = 0
verticalRotationSpeed = 0
cameraTranslation = (0, 0, 0)
cameraAngle = (cameraAngle[0] + 0.0001, cameraAngle[1] + 0.0001, cameraAngle[2] + 0.0001)
cameraPos = (cameraPos[0] + 0.0001, cameraPos[1] + 0.0001, cameraPos[2] + 0.0001)


def findCenterOfPlane(cameraPos, cameraAngle):
    # Let a, b, c represent vector components of camera angle
    a, b, c = cameraAngle[0], cameraAngle[1], cameraAngle[2]

    # Let x, y, z represent 3d coordinates of camera pos
    x, y, z = cameraPos[0], cameraPos[1], cameraPos[2]

    magnitudeOfCameraPos = magnitude = math.sqrt(a ** 2 + b ** 2 + c ** 2)

    # Let x2, y2, z2 represent 3d coordinates of center of plane
    x2 = x + a / magnitude
    y2 = y + b / magnitude
    z2 = z + c / magnitude
    return (x2, y2, z2)


def findEquationOfPlane(cameraAngle, centerOfPlane):
    # Let a, b, c represent vector components of camera angle
    a, b, c = cameraAngle[0], cameraAngle[1], cameraAngle[2]

    # Let x, y, z represent 3d coordinates of center of plane
    x, y, z = centerOfPlane[0], centerOfPlane[1], centerOfPlane[2]

    d = -(a * x) - b * y - c * z

    return (a, b, c, d)


def findDistanceFromCamera(cameraPos, pointPos):
    # Let x1, y1, z1 = point pos coordinates
    x1, y1, z1 = pointPos[0], pointPos[1], pointPos[2]

    # Let x2, y2, z2 = camera pos coordinates
    x2, y2, z2, = cameraPos[0], cameraPos[1], cameraPos[2]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)



def findIntersectionOnPlane(cameraPos, pointPos, equationOfPlane):
    # Let x1, y1, z1 = point pos coordinates
    x1, y1, z1 = pointPos[0], pointPos[1], pointPos[2]

    # Let x2, y2, z2 = camera pos coordinates
    x2, y2, z2, = cameraPos[0], cameraPos[1], cameraPos[2]

    # Let p, q, r = direction vector from pointPos to cameraPos (direction of pointPos vector)
    p, q, r = x1 - x2, y1 - y2, z1 - z2

    # Let a, b, c, d = coefficients and constants of the equation of the plane
    a, b, c, d = equationOfPlane[0], equationOfPlane[1], equationOfPlane[2], equationOfPlane[3]

    LAMBDA = - (a * x1 + b * y1 + c * z1 + d) / (a * p + b * q + c * r)

    # Let x3, y3, z3 = coordinates of intersection on plane
    x3, y3, z3 = x1 + LAMBDA * p, y1 + LAMBDA * q, z1 + LAMBDA * r

    return (x3, y3, z3)


def findClosestPointOnHorizon(cameraAngle, centerOfPlane, intersectionOnPlane):
    # Let p, q = horizontal components (x and y) of camera angle
    p, q = cameraAngle[0], cameraAngle[1]

    # Let x1, y1, z1 = coordinates of center of plane
    x1, y1, z1 = centerOfPlane[0], centerOfPlane[1], centerOfPlane[2]

    # Let x2, y2, z2 = coordinates of intersection on plane (intersection of point vector with plane)
    x2, y2, z2 = intersectionOnPlane[0], intersectionOnPlane[1], intersectionOnPlane[2]

    LAMBDA = (q * x1 - q * x2 + p * y2 - p * y1) / (q ** 2 + p ** 2)

    # Let x3, y3, z3 = coordinates of closest point on horizon line
    x3, y3, z3 = x1 - LAMBDA * q, y1 + LAMBDA * p, z1

    direction = True
    if LAMBDA > 0:
        direction = True
    else:
        direction = False

    return (x3, y3, z3, direction)


def findScreenComponentDistances(centerOfPlane, intersectionOnPlane, closestPointOnHorizon):
    horizontalDistanceOnScreen = findDistance(centerOfPlane, closestPointOnHorizon)
    verticalDistanceOnScreen = findDistance(closestPointOnHorizon, intersectionOnPlane)

    if intersectionOnPlane[2] < closestPointOnHorizon[2]:
        verticalDistanceOnScreen *= -1

    '''
    if findHorizontalAngle(closestPointOnHorizon, cameraPos) > findHorizontalAngle(centerOfPlane, cameraPos):
        horizontalDistanceOnScreen *= -1
    '''

    if closestPointOnHorizon[3]:
        horizontalDistanceOnScreen *= -1

    return (horizontalDistanceOnScreen, verticalDistanceOnScreen)


def findDisplayDistances(screenComponentDistances, FOV, screenWidth):
    x, y = screenComponentDistances[0], screenComponentDistances[1]

    maxDistOnScreenForFOV = math.sin(FOV / 2)

    xDisplayDistance = x / maxDistOnScreenForFOV * screenWidth / 2
    yDisplayDistance = y / maxDistOnScreenForFOV * screenWidth / 2

    return xDisplayDistance, yDisplayDistance


def findDistance(p1, p2):
    # Basic formula to find distance between 2 points
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def findHorizontalAngle(p1, p2):
    # Establishing horizontal coordinates
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    slope = (y2 - y1) / (x2 - x1)

    angle = math.atan(slope)
    if x2 < x1 and y2 > y1:
        angle += math.pi
    if x2 < x1 and y2 <= y1:
        angle -= math.pi

    return angle


def findAngleBetweenVectors(v, w):
    # Establishing the 3 components of each vector
    v1, v2, v3 = v[0], v[1], v[2]
    w1, w2, w3 = w[0], w[1], w[2]

    magnitudeV = math.sqrt(v1 ** 2 + v2 ** 2 + v3 ** 2)
    magnitudeW = math.sqrt(w1 ** 2 + w2 ** 2 + w3 ** 2)

    angle = math.acos((v1 * w1 + v2 * w2 + v3 * w3) / (magnitudeV * magnitudeW))
    return angle


def modulateHorizontalComponents(vector):
    p, q = vector[0], vector[1]
    magnitude = math.sqrt(p ** 2 + q ** 2)
    p = p / magnitude
    q = q / magnitude

    return (p, q, vector[2])

# color utils

def darken(color, percentage):
    return tuple(max(int(c * (1 - percentage / 100)), 0) for c in color)





# Example file showing a basic pygame "game loop"

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                horizontalRotationSpeed = cameraPanSpeed
            if event.key == pygame.K_RIGHT:
                horizontalRotationSpeed = -cameraPanSpeed
            if event.key == pygame.K_UP:
                verticalRotationSpeed = cameraPanSpeed
            if event.key == pygame.K_DOWN:
                verticalRotationSpeed = -cameraPanSpeed
            if event.key == pygame.K_w:
                cameraTranslation = (cameraMoveSpeed, cameraTranslation[1], 0)
            if event.key == pygame.K_s:
                cameraTranslation = (-cameraMoveSpeed, cameraTranslation[1], 0)
            if event.key == pygame.K_a:
                cameraTranslation = (cameraTranslation[0], cameraMoveSpeed, 0)
                # cameraPos = (cameraPos[0] - cameraAngle[1], cameraPos[1] + cameraAngle[0], cameraPos[2])
            if event.key == pygame.K_d:
                cameraTranslation = (cameraTranslation[0], -cameraMoveSpeed, 0)
                # cameraPos = (cameraPos[0] + cameraAngle[1], cameraPos[1] - cameraAngle[0], cameraPos[2])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                horizontalRotationSpeed = 0
            if event.key == pygame.K_RIGHT:
                horizontalRotationSpeed = 0
            if event.key == pygame.K_UP:
                verticalRotationSpeed = 0
            if event.key == pygame.K_DOWN:
                verticalRotationSpeed = 0
            if event.key == pygame.K_w:
                cameraTranslation = (0, cameraTranslation[1], 0)
            if event.key == pygame.K_s:
                cameraTranslation = (0, cameraTranslation[1], 0)
            if event.key == pygame.K_a:
                cameraTranslation = (cameraTranslation[0], 0, 0)
            if event.key == pygame.K_d:
                cameraTranslation = (cameraTranslation[0], 0, 0)

    # CAMERA MOTION
    horizontalRotation += horizontalRotationSpeed
    verticalRotation += verticalRotationSpeed
    if abs(verticalRotation) > math.pi / 2 - 0.01:
        verticalRotation = numpy.sign(verticalRotation) * (math.pi / 2 - 0.01)
    cameraAngle = (math.cos(horizontalRotation), math.sin(horizontalRotation), math.tan(verticalRotation))
    cameraAngle = modulateHorizontalComponents(cameraAngle)

    if cameraTranslation[0] != 0 or cameraTranslation[1] != 0:
        cameraTranslation = modulateHorizontalComponents(cameraTranslation)

    cameraTranslation = (cameraMoveSpeed * cameraTranslation[0], cameraMoveSpeed * cameraTranslation[1], 0)
    cameraPos = (cameraPos[0] + cameraAngle[0] * cameraTranslation[0] - cameraAngle[1] * cameraTranslation[1],
                 cameraPos[1] + cameraAngle[1] * cameraTranslation[0] + cameraAngle[0] * cameraTranslation[1],
                 cameraPos[2])

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # GAME UPDATES
    centerOfPlane = findCenterOfPlane(cameraPos, cameraAngle)
    equationOfPlane = findEquationOfPlane(cameraAngle, centerOfPlane)

    objectsToRender = []

    pointsOnDisplay = []  # [[listOfPoints],(color)]
    for j in range(len(objects)):
        object = objects[j]
        points = object[0]
        connections = object[1]
        color = object[2]
        drawPoints = object[3]
        surfaces = object[4] if len(object) > 4 else []
        pointsOnDisplay = []

        for i in range(len(points)):
            pointPos = points[i]
            intersectionOnPlane = findIntersectionOnPlane(cameraPos, pointPos, equationOfPlane)
            closestPointOnHorizon = findClosestPointOnHorizon(cameraAngle, centerOfPlane, intersectionOnPlane)
            screenComponentDistances = findScreenComponentDistances(centerOfPlane, intersectionOnPlane,
                                                                    closestPointOnHorizon)
            displayDistances = findDisplayDistances(screenComponentDistances, FOV, screenWidth)

            isBehind = False
            if findAngleBetweenVectors(cameraAngle, (
                    pointPos[0] - cameraPos[0], pointPos[1] - cameraPos[1], pointPos[2] - cameraPos[2])) >= math.pi / 2:
                isBehind = True

            if (abs(displayDistances[1]) > 30000):
                displayDistances = (displayDistances[0] * numpy.sign(displayDistances[1]) * 30000 / displayDistances[1],
                                    numpy.sign(displayDistances[1]) * 30000)
            if (abs(displayDistances[0]) > 30000):
                displayDistances = (numpy.sign(displayDistances[0]) * 30000,
                                    displayDistances[1] * numpy.sign(displayDistances[0]) * 30000 / displayDistances[0])

            pointsOnDisplay.append(
                (int(screenWidth / 2 + displayDistances[0]), int(screenHeight / 2 - displayDistances[1]), isBehind))

        for i in range(len(pointsOnDisplay)):
            if drawPoints:
                if pointsOnDisplay[i][2] == True:
                    continue

                distance = findDistanceFromCamera(cameraPos, points[i])

                objectsToRender.append({"distance": distance, "type": "filled_circle",
                                        "content": [screen, pointsOnDisplay[i][0], pointsOnDisplay[i][1], 4, darken(color, distance*3)]})

            else:
                break

        for i in range(len(connections)):
            p1 = pointsOnDisplay[connections[i][0]]
            p2 = pointsOnDisplay[connections[i][1]]
            if p1[2] == True and p2[2] == True:
                continue
            if p1[2] == True:
                deltaX = p2[0] - p1[0]
                deltaY = p2[1] - p1[1]
                d1 = (numpy.sign(deltaX) * screenWidth - p1[0]) / deltaX
                d2 = (numpy.sign(deltaY) * screenWidth - p1[1]) / deltaY
                if d1 < d2:
                    p1 = (p1[0] + d1 * deltaX, p1[1] + d1 * deltaY, p1[2])
                else:
                    p1 = (p1[0] + d2 * deltaX, p1[1] + d2 * deltaY, p1[2])
            if p2[2] == True:
                deltaX = p1[0] - p2[0]
                deltaY = p1[1] - p2[1]
                d1 = (numpy.sign(deltaX) * screenWidth - p2[0]) / deltaX
                d2 = (numpy.sign(deltaY) * screenWidth - p2[1]) / deltaY
                if d1 < d2:
                    p2 = (p2[0] + d1 * deltaX, p2[1] + d1 * deltaY, p2[2])
                else:
                    p2 = (p2[0] + d2 * deltaX, p2[1] + d2 * deltaY, p2[2])

            distance = max(
                findDistanceFromCamera(cameraPos, points[connections[i][0]]),
                findDistanceFromCamera(cameraPos, points[connections[i][1]]))

            objectsToRender.append({"distance": distance, "type": "aaline",
                                    "content": [screen, darken(color, 50), (p1[0], p1[1]), (p2[0], p2[1])]})

        for i in range(len(surfaces)):
            surfaceBoundingPoints = []
            distance = 0
            skip_surface = False

            for point_index in surfaces[i]:
                p = pointsOnDisplay[point_index]

                if p[2] == True:
                    skip_surface = True
                    break

                distance += findDistanceFromCamera(cameraPos, points[point_index])

                surfaceBoundingPoints.append((p[0], p[1]))

            if skip_surface:
                continue

            distance /= len(surfaces[i])

            objectsToRender.append({"distance": distance, "type": "filled_polygon",
                                    "content": [screen, surfaceBoundingPoints, darken(color, i * 5)]})

    # diagnostics

    # RENDER YOUR GAME HERE


    renderQueue = sorted(objectsToRender, key=itemgetter('distance'), reverse=True)

    for rendering in renderQueue :
        content = rendering["content"]
        type = rendering["type"]
        if type == "filled_circle" :
            pygame.gfxdraw.filled_circle(content[0], content[1], content[2], content[3], content[4])
        elif type == "filled_polygon":
            pygame.gfxdraw.filled_polygon(content[0], content[1], content[2])
        elif type == "aaline":
            pygame.draw.aaline(content[0], content[1], content[2], content[3])


    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(simSpeed)  # limits FPS to 60

pygame.quit()

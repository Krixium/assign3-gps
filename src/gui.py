# Only works with 1024 x 512 for some reason
# x = ((height / 2) / pi)(2 ^ zoom)(longitude + pi)
# y = ((height / 2) / pi)(2 ^ zoom)(pi - ln(tan(pi / 4 + latitude / 2)))
import numpy as np
import pygame
from src.res import Meta, GuiProperties


def mercPorjection(lat, lon):
    mLon = np.deg2rad(lon)
    mLat = np.deg2rad(lat)

    a = (Meta.HEIGHT / 2 / np.pi) * np.power(2, Meta.ZOOM)
    b = mLon + np.pi
    x = int(a * b)

    a = (Meta.HEIGHT / 2 / np.pi) * np.power(2, Meta.ZOOM)
    b = np.tan(np.pi / 4 + mLat / 2)
    c = np.pi - np.log(b)
    y = int(a * c)

    # might be needed later
    # if x < -Meta.WIDTH / 2:
    #     x += Meta.WIDTH
    # elif x > Meta.WIDTH / 2:
    #     x -= Meta.WIDTH

    return x, y


def plotCoordinate(surface, color, lat, lon):
    pos = mercPorjection(lat, lon)
    mc = mercPorjection(0, 0)
    adjustedPos = int(pos[0] - mc[0] + Meta.CENTER[0]), int(pos[1] - mc[1] + Meta.CENTER[1])
    print(adjustedPos)
    pygame.draw.circle(surface, color, adjustedPos, GuiProperties.DOT_RADIUS)

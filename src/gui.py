# Only works with 1024 x 512 for some reason
# x = ((height / 2) / pi)(2 ^ zoom)(longitude + pi)
# y = ((height / 2) / pi)(2 ^ zoom)(pi - ln(tan(pi / 4 + latitude / 2)))
import collections
import numpy as np
import pygame
from src.res import Meta, GuiProperties

gps_object = collections.namedtuple("gps_socket", "data_stream")


def dispaly_data(gps_object):
    merc_projection(gps_object.data_steram.TPV["lat"], gps_object.data_steram.TPV["lon"])
    #print_data(gps_object.data_steram.TPV)


def merc_projection(lat, lon):
    m_lon = np.deg2rad(lon)
    m_lat = np.deg2rad(lat)

    a = (Meta.HEIGHT / 2 / np.pi) * np.power(2, Meta.ZOOM)
    b = m_lon + np.pi
    x = int(a * b)

    a = (Meta.HEIGHT / 2 / np.pi) * np.power(2, Meta.ZOOM)
    b = np.tan(np.pi / 4 + m_lat / 2)
    c = np.pi - np.log(b)
    y = int(a * c)

    # might be needed later
    # if x < -Meta.WIDTH / 2:
    #     x += Meta.WIDTH
    # elif x > Meta.WIDTH / 2:
    #     x -= Meta.WIDTH

    return x, y


def plot_coord(surface, color, lat, lon):
    pos = merc_projection(lat, lon)
    mc = merc_projection(0, 0)
    adjusted_pos = int(pos[0] - mc[0] + Meta.CENTER[0]), int(pos[1] - mc[1] + Meta.CENTER[1])
    print(adjusted_pos)
    pygame.draw.circle(surface, color, adjusted_pos, GuiProperties.DOT_RADIUS)

'''
def print_data(gps_json):
'''
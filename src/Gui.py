import numpy as np
import pygame as pg


class Dms:
    def __init__(self, coord):
        degrees = np.floor(coord)
        minutes = np.floor(60 * (coord - degrees))
        seconds = np.floor(3600 * (coord - degrees) - 60 * minutes)

        self.deg = str(int(degrees))
        self.min = str(int(minutes))
        self.sec = str(int(seconds))

    def __repr__(self):
        return self.deg + " deg : " + self.min + " min : " + self.sec + " sec"


class Gui:
    WORLD_MAP = "img/world-1024x512.png"
    IMG_WIDTH = 1024
    IMG_HEIGHT = 512
    CENTER = int(IMG_WIDTH / 2), int(IMG_HEIGHT / 2)
    ZOOM = 1
    DOT_RADIUS = 5

    class Window:
        WIDTH = 1024
        HEIGHT = 680

    class Colors:
        BLACK = 0, 0, 0
        WHITE = 255, 255, 255
        RED = 256, 0, 0
        BLUE = 0, 0, 255

    def __init__(self):
        pg.init()
        pg.display.set_mode((Gui.Window.WIDTH, Gui.Window.HEIGHT))

        self.font = pg.font.SysFont("Courier New", 16)

        self.screen = pg.display.get_surface()
        self.background = pg.image.load(Gui.WORLD_MAP)
        self.background_rect = self.background.get_rect()
        self.paint_background()
        pg.display.flip()

    def paint_background(self):
        self.screen.fill(Gui.Colors.BLACK)
        self.screen.blit(self.background, self.background_rect)

    @staticmethod
    def mercator_projection(lat, lon):
        m_lon = np.deg2rad(lon)
        m_lat = np.deg2rad(lat)

        a = (Gui.IMG_HEIGHT / 2 / np.pi) * np.power(2, Gui.ZOOM)
        b = m_lon + np.pi
        x = int(a * b)

        a = (Gui.IMG_HEIGHT / 2 / np.pi) * np.power(2, Gui.ZOOM)
        b = np.tan(np.pi / 4 + m_lat / 2)
        c = np.pi - np.log(b)
        y = int(a * c)

        # might be needed later
        # if x < -Meta.WIDTH / 2:
        #     x += Meta.WIDTH
        # elif x > Meta.WIDTH / 2:
        #     x -= Meta.WIDTH

        return x, y

    @staticmethod
    def parse_timestamp(tpv):
        return str(tpv["time"][12:19])

    @staticmethod
    def get_dms(coord):
        return Dms(coord)

    @staticmethod
    def parse_satellite(satellite):
        prn = "PRN: " + str(satellite["PRN"])
        azimuth = "Azimuth: " + str(satellite["az"])
        snr = "SNR: " + str(satellite["ss"])
        used = "Used: "
        if satellite["used"]:
            used += "Y"
        else:
            used += "N"
        return prn + " " + azimuth + " " + snr + " " + used

    def plot_location(self, lat, lon):
        pos = Gui.mercator_projection(lat, lon)
        m_center = Gui.mercator_projection(0, 0)
        adjusted_pos = int(pos[0] - m_center[0] + Gui.CENTER[0]), int(pos[1] - m_center[1] + Gui.CENTER[1])
        pg.draw.circle(self.screen, Gui.Colors.WHITE, adjusted_pos, Gui.DOT_RADIUS)

    def print_location(self, lat, lon):
        loc_label = "lat: " + str(Gui.get_dms(lat)) + "     lon: " + str(Gui.get_dms(lon))
        loc_label = self.font.render(loc_label, 1, Gui.Colors.WHITE)
        self.screen.blit(loc_label, (20, Gui.IMG_HEIGHT))

    def print_satellite(self, satellite, pos):
        sat_info = Gui.parse_satellite(satellite)
        sat_label = self.font.render(sat_info, 1, Gui.Colors.WHITE)
        self.screen.blit(sat_label, pos)

    def draw_screen(self, data_stream):
        lat = data_stream.TPV["lat"]
        lon = data_stream.TPV["lon"]

        self.paint_background()

        if lat != "n/a" and lon != "n/a":
            self.plot_location(lat, lon)
            self.print_location(lat, lon)

        y_pos = Gui.IMG_HEIGHT + 15
        if data_stream.SKY["satellites"] != "n/a":
            for sat in data_stream.SKY["satellites"]:
                self.print_satellite(sat, (20, y_pos))
                y_pos += 15
        else:
            label = self.font.render("No signal", 1, Gui.Colors.WHITE)
            self.screen.blit(label, (20, y_pos))

        pg.display.flip()



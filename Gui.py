import pygame as pg


# ------------------------------------------------------------------------------------------------------------------
# Class:        Dms
#
# Date:         Nov 3, 2017
#
# Revisions:    N/A
#
# Designer:     Benny Wang
#
# Programmer:   Benny Wang
#
# Notes:        The Dms(degrees-minutes-seconds) class is a data structure that takes in a coordinate of latitude or
#               longitude and stores it degrees, minute, seconds format
# ------------------------------------------------------------------------------------------------------------------
class Dms:
    # ------------------------------------------------------------------------------------------------------------------
    # Function:     __init__
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    Dms(coord)
    #                   coord: The coordinate that will be converted to degrees, minutes, seconds.
    #
    # Returns:      A Dms object.
    #
    # Notes:        The constructor for Dms. Takes in latitude or longitude in coordinates, converts it to degrees,
    #               minutes, seconds and stores it.
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, coord):
        degrees = np.floor(coord)
        minutes = np.floor(60 * (coord - degrees))
        seconds = np.floor(3600 * (coord - degrees) - 60 * minutes)

        self.deg = str(int(degrees))
        self.min = str(int(minutes))
        self.sec = str(int(seconds))

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     __repr__
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    __repr__()
    #
    # Returns:      A string representation of the Dms object.
    #
    # Notes:        __repr__ is a double underscore function that is executed whenever str() is called on the object.
    #
    #               The current implementation will return "##.## deg : ## min : ## sec"
    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return self.deg + " deg : " + self.min + " min : " + self.sec + " sec"


# ------------------------------------------------------------------------------------------------------------------
# Class:        Gui
#
# Date:         Nov 3, 2017
#
# Revisions:    N/A
#
# Designer:     Benny Wang
#               Juliana French
#
# Programmer:   Benny Wang
#
# Notes:        Gui is an object handles all of the drawing of the gui and parsing the gpsd data.
#
#               Only one Gui object should be instantiated at any time.
# ------------------------------------------------------------------------------------------------------------------
class Gui:
    WORLD_MAP = "img/world-1024x512.png"
    IMG_WIDTH = 1024
    IMG_HEIGHT = 512
    CENTER = int(IMG_WIDTH / 2), int(IMG_HEIGHT / 2)
    ZOOM = 1
    DOT_RADIUS = 5

    # ------------------------------------------------------------------------------------------------------------------
    # Class:        Window
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Notes:        This is a private static class inside of Gui that stores constant values that are used by pygame to
    #               display the application window.
    # ------------------------------------------------------------------------------------------------------------------
    class Window:
        WIDTH = 1024
        HEIGHT = 680

    # ------------------------------------------------------------------------------------------------------------------
    # Class:        Colors
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Notes:        This is a private static class inside of Gui that stores commonly used colors in the gui.
    # ------------------------------------------------------------------------------------------------------------------
    class Colors:
        WHITE = 255, 255, 255
        BLACK = 0, 0, 0

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     __init__
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    Gui()
    #
    # Returns:      A Gui object.
    #
    # Notes:        The constructor for the Gui class. In the constructor, pygame and related variables are initialized,
    #               the application window is created and displayed, and the background image is loaded and drawn.
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pg.init()
        pg.display.set_mode((Gui.Window.WIDTH, Gui.Window.HEIGHT))

        self.font = pg.font.SysFont("Courier New", 16)

        self.surface = pg.display.get_surface()
        self.background = pg.image.load(Gui.WORLD_MAP)
        self.background_rect = self.background.get_rect()
        self.paint_background()
        pg.display.flip()

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     paint_background
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    paint_background()
    #
    # Returns:      Void.
    #
    # Notes:        This function is used to clear the next surface to be drawn.
    #               The surface is cleared by painting the whole surface black and then placing the background image
    #               at 0, 0.
    # ------------------------------------------------------------------------------------------------------------------
    def paint_background(self):
        self.surface.fill(Gui.Colors.BLACK)
        self.surface.blit(self.background, self.background_rect)

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     mercator_projection
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    mercator_projection(lat, lon)
    #                   lat: Latitude of the point in coordinate form to be projected on a 2D map using a web mercator
    #                        projection.
    #                   lon: Longitude of the point in coordinate form to be projected on a 2D map using a web mercator
    #                        projection.
    #
    # Returns:      A tuple that contains the x and y of the resulting projection.
    #
    # Notes:        Projects latitude and longitude given in coordinate form onto a 2D map of the world.
    #
    #               The tuple returned from this function is relative to an origin (0, 0) which is located in the top
    #               right of the plane where x grows to right and y grows downwards.
    # ------------------------------------------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     parse_timestamp
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    parse_timestamp(tpv)
    #                   tpv: The time-position-velocity json object from gpsd.
    #
    # Returns:      The time of the current tpv object in a format that is readable to a human.
    #
    # Notes:        Pulls the timestamp from the time-position-veloctiy object of gpsd, trims it to a more readable
    #               format and returns it as a string.
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_timestamp(tpv):
        return str(tpv["time"][12:19])

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     get_dms
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    get_dms(coord)
    #                   coord: Coordinates(longitude or latitude) that will get converted a Dms object.
    #
    # Returns:      A Dms object that when printed will display the coordinate as degrees, minutes, seconds
    #
    # Notes:        This function converts the latitude or longitude in coordinate form into a Dms object that stores
    #               latitude or longitude in degrees, minutes, seconds form.
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_dms(coord):
        return Dms(coord)

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     parse_satellite
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    Nov 5, 2017; Added elevation (Juliana French).
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    parse_satellite(satellite)
    #                   satellite: The satellite object stored in the satellites array of the SKY object in gpsd.
    #
    # Returns:      A human friendly string representation of the satellite that shows PRN, azimuth, SNR and the used
    #               flag.
    #
    # Notes:        This function parses a json object containing information of a gps satellite to a human readable
    #               string. The resulting string will contain the PRN, Azimuth, SNR and the Used flag showing whether
    #               or not the satellite is being used in calculating your current gps location.
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_satellite(satellite):
        prn = "PRN: " + str(satellite["PRN"])
        elevation = "Elevation: " + str(satellite["el"])
        azimuth = "Azimuth: " + str(satellite["az"])
        snr = "SNR: " + str(satellite["ss"])
        used = "Used: "
        if satellite["used"]:
            used += "Y"
        else:
            used += "N"
        return prn + " " + elevation + " " + azimuth + " " + snr + " " + used

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     plot_location
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    plot_location(lat, lon)
    #                   lat: The latitude of the coordinate to be plotted on a 2D map.
    #                   lon: The longitude of the coordinate to be plotted on a 2D map.
    #
    # Returns:      Void.
    #
    # Notes:        When given latitude and longitude in coordinate form, this function will plot it on a 2D map of the
    #               world using a web mercator projection.
    # ------------------------------------------------------------------------------------------------------------------
    def plot_location(self, lat, lon):
        pos = Gui.mercator_projection(lat, lon)
        m_center = Gui.mercator_projection(0, 0)
        adjusted_pos = int(pos[0] - m_center[0] + Gui.CENTER[0]), int(pos[1] - m_center[1] + Gui.CENTER[1])
        pg.draw.circle(self.surface, Gui.Colors.WHITE, adjusted_pos, Gui.DOT_RADIUS)

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     print_location
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    Nov 5, 2017; Juliana French
    #               Created logic to determine direction and display in label.
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    print_location(lat, lon)
    #                   lat: The latitude of the coordinate to be drawn on screen.
    #                   lon: The longitude of the coordinate to be drawn on screen.
    #
    # Returns:      Void.
    #
    # Notes:        When given latitude and longitude in coordinate form, this function will convert the latitude and
    #               longitude from coordinate form to degree, minutes, seconds form and draw it on screen. The
    #               location will be drawn under the bottom left corner of the world map.
    # ------------------------------------------------------------------------------------------------------------------
    def print_location(self, lat, lon):
        loc_label = "lat: " + str(Gui.get_dms(lat))
        if lat < 0:
            loc_label += " S"
        else:
            loc_label += " N"

        loc_label += "     lon: " + str(Gui.get_dms(lon))
        if lon < 0:
            loc_label += " W"
        else:
            loc_label += " E"

        loc_label = self.font.render(loc_label, 1, Gui.Colors.WHITE)
        self.surface.blit(loc_label, (20, Gui.IMG_HEIGHT))

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     print_satellite
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    print_satellite(satellite, pos)
    #                   satellite: The satellite json object from gpsd that will be drawn on screen.
    #                   pos: The position of the top left corner where the satellite information will be drawn.
    #
    # Returns:      Void.
    #
    # Notes:        When given a satellite json object and position on screen, this function will parse the json to a
    #               string and draw it on screen where the top right corner of the string will be at the given position.
    # ------------------------------------------------------------------------------------------------------------------
    def print_satellite(self, satellite, pos):
        sat_info = Gui.parse_satellite(satellite)
        sat_label = self.font.render(sat_info, 1, Gui.Colors.WHITE)
        self.surface.blit(sat_label, pos)

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     draw_screen
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Benny Wang
    #
    # Programmer:   Benny Wang
    #
    # Interface:    draw_screen(data_stream)
    #                   data_stream: The data stream coming from gpsd.
    #
    # Returns:      Void.
    #
    # Notes:        This function will parse all necessary information contained in the data stream object and display
    #               it on the Gui. This function also checks all of the json objects for errors before it passes the
    #               data along to have it parsed.
    # ------------------------------------------------------------------------------------------------------------------
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
            self.surface.blit(label, (20, y_pos))

        pg.display.flip()

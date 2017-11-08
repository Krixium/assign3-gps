# ---------------------------------------------------------------------------------------------
# Source File:  __main__.py     An application to display GPS location data.
#
# Program:      dcgps
#
# Functions:    void __main__(void)
#
# Date:         Nov 3, 2017
#
# Revisions:    Nov 6, 2017; Michaela Yoon
#                   Moved GpsThread class to separate file.
#
# Designer:     Juliana French
#               Benny Wang
#               Michaela Yoon
#
# Programmer:   Juliana French
#               Benny Wang
#               Michaela Yoon
#
# Notes:
# This program continuously reads and displays data from GPS satellites.
# ---------------------------------------------------------------------------------------------
if __name__ == "__main__":
    import pygame
    import sys
    import time

    from Gui import Gui
    from GpsThread import GpsThread

    # Initialize GUI
    gui = Gui()

    # Initialize GPS3
    gps_thread = GpsThread(gui)
    gps_thread.start()

    # Listen for when the user closes the window
    while gps_thread.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gps_thread.stop()
        time.sleep(1)

    sys.exit(0)
else:
    print("Please run, do not import")

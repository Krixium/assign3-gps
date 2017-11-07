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

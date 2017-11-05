if __name__ == "__main__":
    import pygame
    import sys
    import time

    from gps3 import gps3
    from Gui import Gui
    from threading import Thread

    class GpsThread(Thread):
        def __init__(self, interface):
            Thread.__init__(self)
            self.isRunning = True
            self.gui = interface
            self.socket = gps3.GPSDSocket()
            self.stream = gps3.DataStream()

        def run(self):
            self.socket.connect()
            self.socket.watch()

            for new_data in self.socket:
                if not self.isRunning:
                    break
                if new_data:
                    self.stream.unpack(new_data)
                    self.gui.draw_screen(self.stream)
                time.sleep(1)

        def is_alive(self):
            return self.isRunning

        def stop(self):
            self.isRunning = False

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

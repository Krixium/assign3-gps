import time
from gps3 import gps3
from threading import Thread


# ----------------------------------------------------------------------------------------------------------------------
# Source File:  GpsThread
#
# Program:      dcgps
#
# Functions:
#               GpsThread __init__(self, interface)
#               void run(self)
#               Boolean is_alive(self)
#               void stop(self)
#
# Date:         Nov 3, 2017
#
# Revisions:    N/A
#
# Designer:     Juliana French
#               Michaela Yoon
#
# Programmer:   Juliana French
#               Michaela Yoon
#
# Notes:
# Defines a simple thread to continuously gather data from the satellites.
# ----------------------------------------------------------------------------------------------------------------------
class GpsThread(Thread):
    # ------------------------------------------------------------------------------------------------------------------
    # Function:     __init__
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Juliana French
    #
    # Programmer:   Juliana French
    #
    # Interface:    __init__(self, interface)
    #
    # Returns:      A thread.
    #
    # Notes:        The constructor for GpsThread class. Initializes a thread, sets up the interface, and links socket
    #               and stream to gps 3.
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, interface):
        Thread.__init__(self)
        self.isRunning = True
        self.gui = interface
        self.socket = gps3.GPSDSocket()
        self.stream = gps3.DataStream()

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     run
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Michaela Yoon
    #
    # Programmer:   Michaela Yoon
    #
    # Interface:    run(self)
    #
    # Returns:      Void.
    #
    # Notes:
    # Monitors the socket and streams to GUI when presented with new data.
    # ------------------------------------------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     is_alive
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Juliana French
    #
    # Programmer:   Juliana French
    #
    # Interface:    is_alive(self)
    #
    # Returns:      Whether the thread is alive.
    #
    # Notes:        Checks whether thread is running or not.
    # ------------------------------------------------------------------------------------------------------------------
    def is_alive(self):
        return self.isRunning

    # ------------------------------------------------------------------------------------------------------------------
    # Function:     stop
    #
    # Date:         Nov 3, 2017
    #
    # Revisions:    N/A
    #
    # Designer:     Juliana French
    #
    # Programmer:   Juliana French
    #
    # Interface:    stop(self)
    #
    # Returns:      void.
    #
    # Notes:        Sets Thread isRunning() to false.
    # ------------------------------------------------------------------------------------------------------------------
    def stop(self):
        self.isRunning = False

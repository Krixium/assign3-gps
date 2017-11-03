if __name__ == "__main__":
    from gps3 import gps3
    from src.Gui import Gui

    # Initialize GUI
    gui = Gui()

    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()

    gps_socket.connect()
    gps_socket.watch()

    for new_data in gps_socket:
        if new_data:
            data_stream.unpack(new_data)

            # pass data_stream object to gui to handle displaying information
            gui.draw_screen(data_stream)

else:
    print("Please run, do not import")

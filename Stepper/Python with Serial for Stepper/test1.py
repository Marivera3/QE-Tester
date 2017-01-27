import serial
import time
import threading


try:

    ser = serial.Serial('COM4', baudrate=9600, timeout=1)
    ser.writeTimeout = 2
    connected = False

except serial.SerialException as err:
    print("[ERROR] {0}".format(err))

else:
    if ser.isOpen():

        try:
            ser.flushInput()  # flush input buffer, discarding all its contents
            ser.flushOutput()  # flush output buffer, aborting current output
            # and discard all that is in buffer
            time.sleep(1)  # give the serial port sometime to receive the data

            def handle_data(data):
                with open("test1.txt", "a") as fil:
                    if data:
                        fil.write(data)

            def read_from_port(ser):
                while True:
                    if ser.isOpen():
                        try:
                            reading = ser.readline().decode()
                            handle_data(reading)
                        except AttributeError as err1:
                            # print("[ERROR] {0}".format(err1))
                            break

            thread = threading.Thread(target=read_from_port, args=(ser,))
            thread.setDaemon = True
            thread.start()

            # def write_to_port()

            while True:
                string = input("Comando: ")
                if string == "exit":
                    break

                ser.write(string.encode())
                time.sleep(1)
            ser.close()
        except Exception as e1:
            print("error communicating...: " + str(e1))

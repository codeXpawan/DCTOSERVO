import serial
import time
import csv

# Set up the serial connection
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace 'COM3' with the correct port for your Arduino

time.sleep(2)  # Wait for the connection to be established

def send_command(command, value):
            command_str = f"{command}{value}\n"  # Assuming commands are single characters (e.g., 'L', 'R')
            ser.write(command_str.encode())

exit = True
while(exit):
    cmd = input("Input Command (V:Speed, F: forward, B: backward, P: Position): ")
    if(cmd == 'V' or cmd == 'P'):
        val = int(input("Input Value: "))
        send_command(cmd,val)
    else:
        exit = False
        val = ''
# Open a CSV file to write data
with open('pot_data_with_motor_s_1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Motor_Position', 'Potentiometer_Data'])  # Write CSV header

    try:
        send_command(cmd,val)
        while(True):
            try:
                line = ser.readline()
                line = line.decode('utf-8')
                if line:
                    values = line.split(',')

                    # Check if there are enough values
                    if len(values) == 2:
                        position, potentiometer_data = values
                        # Check if the values are not empty before attempting conversion
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Get the current timestamp
                        print(f"{timestamp}, {position}, {potentiometer_data}")
                        writer.writerow([timestamp, position, potentiometer_data])  # Write data to CSV file
                    else:
                        print("Error: Invalid number of values in the line")
                else:
                    print("Error: Empty line received")

                # file.writerow([distance,degree,time])
            except UnicodeDecodeError:
                print("Error decoding line.")
    except KeyboardInterrupt:
        send_command('S','')
        print("Program terminated")
    finally:
        ser.close()  # Close the serial connection

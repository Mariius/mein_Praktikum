import time
import serial

def send_commands_to_arduino(commands, output_file):
    # Öffne die serielle Verbindung zur Arduino-Platine
    ser = serial.Serial('COM5', 9600)  # Passe den COM-Port und die Baudrate an deine Konfiguration an
    
    # Öffne die Ausgabedatei im Schreibmodus
    with open(output_file, 'w') as file:
        for command in commands:
            # Sende den Befehl an die Arduino-Platine
            ser.write(command.encode())
            time.sleep(0.5)
            
            # Warte auf die Antwort der Arduino-Platine
            while True:
                response = ser.readline().decode().strip()
                
                # Schreibe die Antwort in die Ausgabedatei
                file.write(response + '\n')
                break
        
    # Schließe die serielle Verbindung zur Arduino-Platine
    ser.close()

# Beispielaufruf der Funktion
commands = ['read memory', '0', '16']
output_file = 'antworten.txt'
send_commands_to_arduino(commands, output_file)

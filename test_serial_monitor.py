import subprocess
import threading

def upload_sketch(sketch_path, port):
    
        compile=["aduino-cli.exe", "compile", "--fqbn", "arduino:avr:nano", sketch_path]
        subprocess.run(compile)
    
        upload=["aduino-cli.exe", "upload","--port",port, "--fqbn", "arduino:avr:nano",sketch_path] 
        subprocess.run(upload)

        # Seriellen Monitor öffnen
        monitor_thread = threading.Thread(target=open_serial_monitor, args=(port,))
        monitor_thread.start()
    

def open_serial_monitor(port):
    try:
        monitor_cmd = f"arduino-cli serial monitor --port {port}"
        subprocess.run(monitor_cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Öffnen des seriellen Monitors: {e}")

# Beispielaufruf
sketch_path = "Blink\Blink.ino"
board_type = "arduino:avr:nano"  # Boardtyp entsprechend deinem Arduino-Modell anpassen
port = "COM6"  # Port entsprechend deiner Konfiguration anpassen
upload_sketch(sketch_path, port)
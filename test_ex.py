import os
import subprocess
import pytest

@pytest.fixture(scope="module")
def test_data_dir():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(test_dir, "test_data")
    os.makedirs(data_dir, exist_ok=True)
    yield data_dir
    # Clean up the test data directory after the tests
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        os.remove(file_path)
    os.rmdir(data_dir)

def test_compile_and_upload(test_data_dir):
    program = "arduino-cli"
    sketch_path = os.path.join(test_data_dir, "test_sketch.ino")
    port = "COM1"
    fqbn = "arduino:avr:uno"

    with open(sketch_path, "w") as sketch_file:
        sketch_file.write("#include <Arduino.h>\n\nvoid setup() {}\n\nvoid loop() {}")

    compile_command = [program, "compile", "--fqbn", fqbn, sketch_path]
    upload_command = [program, "upload", "--port", port, "--fqbn", fqbn, sketch_path]

    # Run the compile command
    subprocess.run(compile_command, check=True)

    # Run the upload command
    subprocess.run(upload_command, check=True)

def test_read_memory(test_data_dir):
    program = "arduino-cli"
    port = "COM1"
    position = "7A"
    length = "06"

    read_command = [program, "read-memory", "--port", port, "--position", position, "--length", length]

    # Run the read-memory command
    subprocess.run(read_command, check=True)

    # Check if the output file was created
    output_file = os.path.join(test_data_dir, "data.txt")
    assert os.path.isfile(output_file)

def test_write_memory(test_data_dir):
    program = "arduino-cli"
    port = "COM1"
    position = "00"
    length = "20"
    content = "0D 10 8C B0 57 4D 74 67 2E EE 3E 15 42 A3 1 CB 41 42 43 44 30 36 0 0 44 65 66 61 75"

    write_command = [program, "write-memory", "--port", port, "--position", position, "--length", length, "--content", content]

    # Run the write-memory command
    subprocess.run(write_command, check=True)

    # Check if the output file was created
    output_file = os.path.join(test_data_dir, "write_report.txt")
    assert os.path.isfile(output_file)

def test_clear_memory(test_data_dir):
    program = "arduino-cli"
    port = "COM1"

    clear_command = [program, "clear-memory", "--port", port]

    # Run the clear-memory command
    subprocess.run(clear_command, check=True)

    # Check if the output file was created
    output_file = os.path.join(test_data_dir, "clear_report.txt")
    assert os.path.isfile(output_file)


import subprocess
import signal
import os
import sys

# Function to start a process
def start_process(name, script_path):
    process = subprocess.Popen([sys.executable, script_path])
    print(f"{name} started with PID {process.pid}")
    return process

# Start Kafka Producer (Data Ingestion)
producer_process = start_process("Kafka Producer (Data Ingestion)", "./data_ingestion.py")

# Start Kafka Consumer (Preprocessing)
preprocessing_process = start_process("Kafka Consumer (Preprocessing)", "./data_preprocessing.py")

# Start Kafka Consumer (Wake-Up Logic)
wake_up_process = start_process("Kafka Consumer (Wake-Up Logic)", "./wake_up_consumer.py")

# Function to handle graceful shutdown
def graceful_shutdown(signum, frame):
    print("Shutting down...")
    producer_process.terminate()
    preprocessing_process.terminate()
    wake_up_process.terminate()
    producer_process.wait()
    preprocessing_process.wait()
    wake_up_process.wait()
    print("All processes terminated.")
    sys.exit(0)

# Set up signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Wait for all processes to complete
producer_process.wait()
preprocessing_process.wait()
wake_up_process.wait()

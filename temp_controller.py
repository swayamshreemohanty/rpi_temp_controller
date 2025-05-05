import RPi.GPIO as GPIO
import time

# GPIO setup
FAN_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

def get_cpu_temperature():
    """Reads the CPU temperature from the system file."""
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temp_str = file.read().strip()
    return int(temp_str) / 1000.0  # Convert millidegree Celsius to degree Celsius

def control_fan(cold_temp, hot_temp):
    """Controls the fan based on the cold and hot target temperatures."""
    try:
        while True:
            current_temp = get_cpu_temperature()
            print(f"Current Temperature: {current_temp}°C")

            if current_temp > hot_temp:
                GPIO.output(FAN_PIN, GPIO.HIGH)  # Turn fan on
                print("Fan ON")
            elif current_temp < cold_temp:
                GPIO.output(FAN_PIN, GPIO.LOW)  # Turn fan off
                print("Fan OFF")

            time.sleep(5)  # Check temperature every 5 seconds
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    cold_target_temperature = 35.0  # Temperature to stop the fan
    hot_target_temperature = 45.0  # Temperature to start the fan
    control_fan(cold_target_temperature, hot_target_temperature)

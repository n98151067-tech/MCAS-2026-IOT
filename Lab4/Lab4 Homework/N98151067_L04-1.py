
import time
import adafruit_dht
import board

# Lab 4-1: DHT11 溫濕度感測器
# Raspberry Pi 實體 PIN 8 = BCM GPIO14
# 注意：執行前必須確認 DATA 電壓不超過 3.3V

student_id = "n98151067"

dht_device = adafruit_dht.DHT11(board.D14)

print("Student ID:", student_id)
print("Lab 4-1: DHT11 Temperature and Humidity")
print("---------------------------------------")

try:
    while True:
        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                temperature_f = temperature_c * 9 / 5 + 32

                print(
                    "Temp: {:.1f} C / {:.1f} F    Humidity: {}%".format(
                        temperature_c,
                        temperature_f,
                        humidity
                    )
                )

        except RuntimeError as err:
            print("Sensor reading error:", err)

        time.sleep(2.0)

except KeyboardInterrupt:
    print("\nProgram stopped.")

finally:
    dht_device.exit()

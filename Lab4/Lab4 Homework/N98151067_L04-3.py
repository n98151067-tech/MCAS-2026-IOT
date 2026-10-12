
import serial
import time

# UART 設定
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=1
)

# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write(data.encode('utf-8'))
        print(f"已傳送：{data.strip()}")

# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode(
            'utf-8', errors='replace'
        ).strip()

        if incoming:
            print(f"收到資料：{incoming}")

        return incoming

# 主程式
try:
    print("學號：N98151067")
    print("Lab 4-3 UART 自傳自收測試")
    print("------------------------")

    number = 0

    while True:
        message = f"{number}\n"

        send_data(message)
        time.sleep(0.1)
        receive_data()

        number = (number + 1) % 10
        time.sleep(1)

except KeyboardInterrupt:
    print("\n程式中斷")

finally:
    if ser.is_open:
        ser.close()
        print("串列埠已關閉")

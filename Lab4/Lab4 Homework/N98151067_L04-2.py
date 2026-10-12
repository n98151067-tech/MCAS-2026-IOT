
import RPi.GPIO as GPIO
import time

# 學號
student_id = "n98151067"

# 設定使用 BCM 編號系統
GPIO.setmode(GPIO.BCM)

# HC-SR04 接腳設定
# 實體 PIN 8 = GPIO14
# 實體 PIN 10 = GPIO15
TRIG_y = 14
ECHO_r = 15

# 注意：ECHO 必須先降壓至 3.3V 以下
GPIO.setup(TRIG_y, GPIO.OUT)
GPIO.setup(ECHO_r, GPIO.IN)


def measure_distance():
    # 確保發射端關閉
    GPIO.output(TRIG_y, False)
    time.sleep(0.5)

    # 發送 10 微秒高電位脈衝
    GPIO.output(TRIG_y, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_y, False)

    # 等待 ECHO 變成高電位
    timeout = time.monotonic() + 0.05

    while GPIO.input(ECHO_r) == 0:
        if time.monotonic() > timeout:
            return None

    pulse_start = time.monotonic()

    # 等待 ECHO 變回低電位
    timeout = pulse_start + 0.05

    while GPIO.input(ECHO_r) == 1:
        if time.monotonic() > timeout:
            return None

    pulse_end = time.monotonic()

    # 計算距離（公分）
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    return round(distance, 2)


try:
    print("Student ID:", student_id)
    print("Lab 4-2: HC-SR04")
    print("程式啟動，按 Ctrl+C 停止測試...")
    print("--------------------------------")

    while True:

        # LAB4-2：讀取距離
        distance = measure_distance()

        if distance is None:
            print("測量失敗，請檢查感測器")
        else:
            print("目前距離：{:.2f} cm".format(distance))
            
            if distance < 20:
                print("注意！！！")
            
            else:
                print("沒事")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n停止測量中...")

finally:
    GPIO.cleanup()
    print("GPIO 已清理，程式結束。")

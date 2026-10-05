import tm1637
import datetime
import time

# TM1637 pin setting (BCM)
CLK = 17
DIO = 27

# Create TM1637 display
display = tm1637.TM1637(clk=CLK, dio=DIO)

try:
    while True:
        # Get current time
        now = datetime.datetime.now()

        # Colon ON
        display.time(now, colon=True)
        time.sleep(1)

        # Get current time again
        now = datetime.datetime.now()

        # Colon OFF
        display.time(now, colon=False)
        time.sleep(1)

except KeyboardInterrupt:
    pass
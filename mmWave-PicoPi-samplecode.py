from machine import UART, Pin
import time

# UART1: TX=GP4, RX=GP5
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))

hand_present_flag = 0
last_detected_time = time.ticks_ms()

# Buffer to hold incomplete UART lines
line_buffer = b""

while True:
    if uart.any():
        line_buffer += uart.read()
        while b'\n' in line_buffer:
            line, line_buffer = line_buffer.split(b'\n', 1)
            line = line.strip().decode('utf-8')

            if line == "ON":
                # Set flag tentatively, distance check comes later
                last_detected_time = time.ticks_ms()

            elif line.startswith("Range "):
                try:
                    range_mm = int(line.split()[1])
                    if range_mm <= 100:
                        hand_present_flag = 1
                        print("HAND PRESENT at ", range_mm, "mm")
                        last_detected_time = time.ticks_ms()
                    else:
                        print("NIL")
                        # Object detected but too far
                        pass
                except:
                    pass  # Handle parse errors gracefully

    # If no valid detection in last 0.5s, reset flag
    if hand_present_flag == 1:
        if time.ticks_diff(time.ticks_ms(), last_detected_time) > 500:
            hand_present_flag = 0
            print("HAND NOT PRESENT")

    time.sleep(0.05)

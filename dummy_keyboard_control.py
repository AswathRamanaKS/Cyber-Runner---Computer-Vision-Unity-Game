"""
Dummy keyboard controller for Train IT.

Sends the exact same UDP packets HANDDETECTION.ipynb sends, but driven by
keyboard keys instead of webcam + MediaPipe hand tracking. Use this to test
the game without needing the camera at all.

Controls:
    W / Up arrow      -> right-hand direction: Forward
    S / Down arrow    -> right-hand direction: Backward
    A / Left arrow    -> right-hand direction: Left
    D / Right arrow   -> right-hand direction: Right
    Q                 -> left-hand direction: Left
    E                 -> left-hand direction: Right
    Esc               -> quit

Requires: pip install keyboard
(On Windows the keyboard library sometimes needs the terminal running
as Administrator to see global key presses.)
"""

import socket
import time
import keyboard

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

print("Dummy keyboard controller running. Press Esc to quit.")

last_printed = None

try:
    while True:
        if keyboard.is_pressed("esc"):
            break

        # Right-hand direction (WASD or arrow keys) - mirrors the thumb up/down/left/right logic
        if keyboard.is_pressed("w") or keyboard.is_pressed("up"):
            right_direction = "Forward"
        elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
            right_direction = "Backward"
        elif keyboard.is_pressed("d") or keyboard.is_pressed("right"):
            right_direction = "Right"
        elif keyboard.is_pressed("a") or keyboard.is_pressed("left"):
            right_direction = "Left"
        else:
            right_direction = "None"

        # Left-hand direction (Q/E) - mirrors the left/right-only logic
        if keyboard.is_pressed("e"):
            left_direction = "Right"
        elif keyboard.is_pressed("q"):
            left_direction = "Left"
        else:
            left_direction = "None"

        udp_data = f"[{right_direction},{left_direction}]"
        sock.sendto(str.encode(udp_data), serverAddressPort)

        if udp_data != last_printed:
            print(udp_data)
            last_printed = udp_data

        time.sleep(0.005)  # ~200 packets/sec for low input latency

finally:
    sock.close()
    print("\nStopped.")

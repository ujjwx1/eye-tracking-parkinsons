import cv2
import numpy as np
import time
import math

# --- Blink Detection Setup ---
BLINK_AREA_THRESHOLD = 200  # Adjust based on your eye size and lighting
blink_count = 0
blink_in_progress = False

# --- Saccade Detection Setup ---
prev_x, prev_y = None, None
saccade_threshold_speed = 30  # Pixels per frame — adjust this based on camera resolution/speed
saccade_count = 0

# --- Time Tracking for Blink Rate ---
start_time = time.time()

# --- OpenCV Webcam Setup ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Webcam not accessible")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        if area > 100:  # Ignore noise
            ellipse = cv2.fitEllipse(largest_contour)
            (x, y), (MA, ma), angle = ellipse
            center = (int(x), int(y))

            # Draw results
            cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)

            # --- Blink Detection Logic ---
            if area < BLINK_AREA_THRESHOLD and not blink_in_progress:
                blink_count += 1
                blink_in_progress = True
            elif area >= BLINK_AREA_THRESHOLD:
                blink_in_progress = False

            # --- Saccade Detection Logic ---
            if prev_x is not None and prev_y is not None:
                dx = x - prev_x
                dy = y - prev_y
                speed = math.sqrt(dx**2 + dy**2)

                if speed > saccade_threshold_speed:
                    saccade_count += 1
                    cv2.putText(frame, "SACCADE!", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            prev_x, prev_y = x, y

            # --- Blink Rate ---
            elapsed_time = time.time() - start_time
            blink_rate_per_min = blink_count / (elapsed_time / 60)

            # --- Display All Metrics ---
            cv2.putText(frame, f"Pupil: ({int(x)}, {int(y)})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Area: {int(area)}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Blinks: {blink_count}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Blink Rate: {blink_rate_per_min:.2f} blinks/min", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Saccades: {saccade_count}", (10, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

            # --- Console Print ---
            print(f"Pupil x: {int(x)}, y: {int(y)}, Area: {int(area)}, Major: {int(MA)}, Minor: {int(ma)}, "
                  f"Blinks: {blink_count}, Blink Rate: {blink_rate_per_min:.2f} blinks/min, Saccades: {saccade_count}")

    # --- Show Result Windows ---
    cv2.imshow("Eye Tracker", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()

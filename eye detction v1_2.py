import cv2
import numpy as np
import time

# --- Blink Detection Setup ---
BLINK_AREA_THRESHOLD = 200  # Adjust based on your own eye size
blink_count = 0
blink_in_progress = False

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

        if area > 100:  # Ignore small noise
            ellipse = cv2.fitEllipse(largest_contour)
            (x, y), (MA, ma), angle = ellipse
            center = (int(x), int(y))

            # Draw pupil and center
            cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)

            # --- Blink Detection Logic ---
            if area < BLINK_AREA_THRESHOLD and not blink_in_progress:
                blink_count += 1
                blink_in_progress = True
            elif area >= BLINK_AREA_THRESHOLD:
                blink_in_progress = False

            # --- Calculate Blink Rate ---
            elapsed_time = time.time() - start_time
            blink_rate_per_min = blink_count / (elapsed_time / 60)

            # --- Display Data ---
            cv2.putText(frame, f"Pupil: ({int(x)}, {int(y)})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Area: {int(area)}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Blinks: {blink_count}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            cv2.putText(frame, f"Blink Rate: {blink_rate_per_min:.2f} blinks/min", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            # Print to terminal too
            print(f"Pupil x: {int(x)}, y: {int(y)}, Area: {int(area)}, Major: {int(MA)}, Minor: {int(ma)}, "
                  f"Blinks: {blink_count}, Blink Rate: {blink_rate_per_min:.2f} blinks/min")

    # --- Show Result Windows ---
    cv2.imshow("Eye Tracker", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()

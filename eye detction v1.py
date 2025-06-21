import cv2
import numpy as np

# --- Blink Detection Setup ---
BLINK_AREA_THRESHOLD = 200  # Adjust based on your lighting and eye size
blink_count = 0
blink_in_progress = False

# --- OpenCV Webcam ---
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

    # Find largest dark blob (likely the pupil)
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

            # Blink detection logic
            if area < BLINK_AREA_THRESHOLD and not blink_in_progress:
                blink_count += 1
                blink_in_progress = True
            elif area >= BLINK_AREA_THRESHOLD:
                blink_in_progress = False

            # Print extracted data
            print(f"Pupil x: {int(x)}, y: {int(y)}, Area: {int(area)}, Major: {int(MA)}, Minor: {int(ma)}, Blinks: {blink_count}")

    # Display
    cv2.imshow("Eye Tracker", frame)
    cv2.imshow("Threshold", thresh)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

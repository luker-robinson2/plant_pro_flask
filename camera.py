import cv2
import time
initial = (time.time() * 1000) #get milliseconds
first = True
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Failed to open the camera!")
    exit()
for _ in range(10):
    ret, frame = cap.read()
    time.sleep(0.05)  # Small delay between frames

while True:
    ret, frame = cap.read()

    if ret:
        file_name = "captured_photo.jpg"
        cv2.imwrite(file_name, frame)
        if first:
            print(f"time to first saved photo:{(time.time()*1000) - initial}")
            break
        print(f"Photo saved as {file_name}")
    else:
        print("Failed to capture the frame!")
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
from pyzbar.pyzbar import decode

def start_camera():
    # Open the default camera (usually camera index 0)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale for QR code decoding
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Decode QR codes in the frame
        decoded_objects = decode(gray)

        # Display the frame
        cv2.imshow('Camera', frame)

        # Check for QR code detection
        if decoded_objects:
            for obj in decoded_objects:
                # Extract and print the QR code value
                qr_data = obj.data.decode('utf-8')
                print("QR Code Value:", qr_data)

                # Stop the camera and break out of the loop
                cap.release()
                cv2.destroyAllWindows()
                return

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window if 'q' key is pressed
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera()

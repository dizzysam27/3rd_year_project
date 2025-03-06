import cv2
import threading
import time

class VideoCaptureThread:
    def __init__(self, source=0, width=1280, height=720, fps=60):
        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        self.frame = None
        self.running = True

        # Open video source
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        
        # Start the thread
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame  # Store the latest frame
            time.sleep(1 / self.fps)  # Control the frame rate

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()

# -------------------------------
# Main program
# -------------------------------
def main():
    video = VideoCaptureThread(fps=60)

    while True:
        frame = video.get_frame()
        if frame is not None:
            cv2.imshow("60 FPS Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

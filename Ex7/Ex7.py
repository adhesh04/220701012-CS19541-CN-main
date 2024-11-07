import time
import threading
import random

# Constants
WINDOW_SIZE = int(input("Enter Window Size: "))
input_string = input("Enter Data String: ")
FRAME_COUNT = len(input_string)
TIMEOUT = 2  # seconds
LOSS_PROBABILITY = 0.2  # Probability of a frame being lost

class Sender:
    def __init__(self):
        self.base = 0
        self.next_frame = 0
        self.frames = list(input_string)  # Convert string to list of characters (frames)
        self.lock = threading.Lock()
        self.window = []

    def send_frames(self):
        while self.base < FRAME_COUNT:
            self.lock.acquire()
            if self.next_frame < self.base + WINDOW_SIZE and self.next_frame < FRAME_COUNT:
                # Simulate frame loss
                if random.random() < LOSS_PROBABILITY:
                    print(f"Sender: Frame '{self.frames[self.next_frame]}' is lost.\n")
                    self.window.append(self.next_frame)  # Frame is lost and remains in the window
                else:
                    print(f"Sender: Sending frame '{self.frames[self.next_frame]}'\n")
                    self.window.append(self.next_frame)
                    threading.Thread(target=self.timeout_thread, args=(self.window[-1],)).start()
                self.next_frame += 1
            self.lock.release()
            time.sleep(1)  # Simulate time between sending frames

    def timeout_thread(self, frame_index):
        time.sleep(TIMEOUT)
        self.lock.acquire()
        if frame_index in self.window:
            print(f"Sender: Frame '{self.frames[frame_index]}' timed out, resending...\n")
            # The frame was lost, so remove it from window and reset next_frame to resend it
            self.window.remove(frame_index)
            self.next_frame = frame_index
        self.lock.release()

    def receive_ack(self, ack_index):
        self.lock.acquire()
        if ack_index >= self.base:
            print(f"Sender: Received ACK for frame '{self.frames[ack_index]}'\n")
            self.base = ack_index + 1
            self.window = [f for f in self.window if f > ack_index]
        self.lock.release()

class Receiver:
    def __init__(self, sender):
        self.sender = sender
        self.expected_frame = 0

    def receive_frames(self):
        while self.sender.base < FRAME_COUNT:
            time.sleep(1.5)  # Simulate time to receive a frame
            if self.expected_frame < FRAME_COUNT:
                print(f"Receiver: Received frame '{self.sender.frames[self.expected_frame]}'\n")
                self.send_ack(self.expected_frame)
                self.expected_frame += 1

    def send_ack(self, frame_index):
        print(f"Receiver: Sending ACK for frame '{self.sender.frames[frame_index]}'\n")
        self.sender.receive_ack(frame_index)

def main():
    sender = Sender()
    receiver = Receiver(sender)

    sender_thread = threading.Thread(target=sender.send_frames)
    receiver_thread = threading.Thread(target=receiver.receive_frames)

    sender_thread.start()
    receiver_thread.start()

    sender_thread.join()
    receiver_thread.join()

if __name__ == "__main__":
    main()

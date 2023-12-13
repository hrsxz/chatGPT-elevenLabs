import time
import logging

from multiprocessing import Process, Queue
from src.chatGPT import gpt_utils
from src.camera import capture_pics
from src.elevenLabs import elevenLabs_utils


logging.basicConfig(level=logging.DEBUG, filename='app.log')


class Capture_Pics(Process):
    """This class use for capturing pics from webcam
    """
    def __init__(self):
        super(Capture_Pics, self).__init__()

    def run(self):
        logging.info("Capture Pics process started")
        capture_image = capture_pics.Capture_Pics()
        # capture one picture
        capture_image.capture_one_pic()


class Analytic_Process(Process):
    """This class summarize the utility methods for chatGPT
    """
    def __init__(self, queue):
        super(Analytic_Process, self).__init__()
        self.queue = queue
        self.base64_image_path = "./artifacts/frames/frame.jpg"

    def run(self):
        self.client = gpt_utils.client_chatGPT()
        self.base64_image = self.client.load_image(path=self.base64_image_path)
        try:
            logging.info("GPT client process started")
            response_text = self.client.analyze_image_with_GPT(self.base64_image, [])
            print(response_text)
            self.queue.put(response_text)
        except Exception as e:
            logging.exception(f"Error in the child process: {e}")


class Read_Texts(Process):
    """This class is using elevenlabs model to read texts.
    """
    def __init__(self, queue):
        super(Read_Texts, self).__init__()
        self.queue = queue

    def run(self):
        self.client = elevenLabs_utils.client_elevenlabs()
        while True:
            if self.queue.empty():
                time.sleep(0.01)
            else:
                try:
                    logging.info("Elevenlabs process started")
                    response_text = self.queue.get()
                    self.client.play_audio(response_text)
                except Exception as e:
                    logging.exception(f"Error in the child process: {e}")


if __name__ == "__main__":
    # Create queue to transfer data from analytic process to read text process
    response_text_queue = Queue()

    # Create processes
    capture_images = Capture_Pics()
    analytic_process = Analytic_Process(response_text_queue)
    read_texts = Read_Texts(response_text_queue)

    # Properly start your clients with all required arguments
    try:
        capture_images.start()
        analytic_process.start()
        read_texts.start()
    except Exception as e:
        logging.exception(f"Failed to start processes {e}")

    capture_images.join()
    analytic_process.join()
    read_texts.join()

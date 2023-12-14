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
    def __init__(self, image_queue):
        super(Capture_Pics, self).__init__()
        self.queue = image_queue

    def run(self):
        logging.info("Capture Pics process started")
        capture_image = capture_pics.Capture_Pics()
        while True:
            time.sleep(0.1)
            if self.queue.empty():
                # capture one picture
                frame = capture_image.capture_one_pic()
                # put image into queue only if queue is empty
                # we need to wait chatGPT get the image and process it.
                if frame is not None:
                    base64_image = capture_image.frame_to_base64(frame)
                    self.queue.put(base64_image)


class Analytic_Process(Process):
    """This class summarize the utility methods for chatGPT
    """
    def __init__(self, response_queue, image_queue):
        super(Analytic_Process, self).__init__()
        self.response_queue = response_queue
        self.image_queue = image_queue
        # self.base64_image_path = "./artifacts/frames/frame.jpg"

    def run(self):
        self.client = gpt_utils.client_chatGPT()
        # self.base64_image = self.client.load_image(path=self.base64_image_path)
        while True:
            try:
                logging.info("GPT client process started")
                if self.image_queue.empty():
                    time.sleep(0.05)
                else:
                    self.base64_image = self.image_queue.get()
                    response_text = self.client.analyze_image_with_GPT(self.base64_image, [])
                    print(response_text)
                    self.response_queue.put(response_text)
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
                time.sleep(0.05)
            else:
                try:
                    logging.info("Elevenlabs process started")
                    response_text = self.queue.get()
                    self.client.play_audio(response_text)
                except Exception as e:
                    logging.exception(f"Error in the child process: {e}")


if __name__ == "__main__":
    # Create queue to transfer data from analytic process to read text process
    image_queue = Queue()
    response_text_queue = Queue()

    # Create processes
    capture_images = Capture_Pics(image_queue)
    analytic_process = Analytic_Process(response_text_queue, image_queue)
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

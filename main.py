import time
import logging
import ctypes

from multiprocessing import Process, Queue, Value
from src.chatGPT import gpt_utils
from src.camera import capture_pics
from src.elevenLabs import elevenLabs_utils
from pathlib import Path


# Calculate the project root path directly
project_root_path = Path(__file__).resolve().parent


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./logs/app.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


setup_logging()


class Capture_Pics(Process):
    """This class use for capturing pics from webcam
    """
    def __init__(self, image_queue, event_done):
        super(Capture_Pics, self).__init__()
        self.queue = image_queue
        self.event_done = event_done

    def run(self):
        logging.info("Capture Pics process started")
        while True:
            time.sleep(0.1)
            # Need to wait until audio is done
            if self.event_done.value:
                capture_image = capture_pics.Capture_Pics()
                # capture one picture
                frame = capture_image.capture_one_pic("frame")
                # put image into queue only if queue is empty
                # we need to wait chatGPT get the image and process it.
                if frame is not None:
                    base64_image = capture_image.frame_to_base64(frame)
                    self.queue.put(base64_image)
                    self.event_done.value = False
            else:
                time.sleep(0.1)
                capture_image = capture_pics.Capture_Pics()
                # capture one picture
                frame = capture_image.capture_one_pic("live")


class Analytic_Process(Process):
    """This class summarize the utility methods for chatGPT
    """
    def __init__(self, response_queue, image_queue):
        super(Analytic_Process, self).__init__()
        self.response_queue = response_queue
        self.image_queue = image_queue
        # self.base64_image_path = "./artifacts/frames/frame.jpg"

    def run(self):
        logging.info("GPT client process started")
        self.client = gpt_utils.client_chatGPT()
        # self.base64_image = self.client.load_image(path=self.base64_image_path)
        while True:
            try:
                if not self.response_queue.empty():
                    # playing audio is not done yet
                    time.sleep(1)
                else:
                    if self.image_queue.empty():
                        time.sleep(0.1)
                    else:
                        self.base64_image = self.image_queue.get()
                        if True:
                            user_script = [{"role": "user",
                                            "content": "Limit reply to 100 words."}]
                        response_text = self.client.analyze_image_with_GPT(
                            self.base64_image, user_script
                        )
                        print(response_text)
                        path = project_root_path / "artifacts/response_text/response_text.txt"
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(response_text)
                        self.response_queue.put(response_text)
            except Exception as e:
                logging.exception(f"Error in the child process: {e}")


class Read_Texts(Process):
    """This class is using elevenlabs model to read texts.
    """
    def __init__(self, queue, event_done):
        super(Read_Texts, self).__init__()
        self.queue = queue
        self.event_done = event_done

    def run(self):
        logging.info("Elevenlabs process started")
        self.client = elevenLabs_utils.client_elevenlabs()
        while True:
            if self.queue.empty():
                time.sleep(0.05)
            else:
                try:
                    response_text = self.queue.get()
                    self.client.play_audio(response_text)
                    self.event_done.value = True
                except Exception as e:
                    logging.exception(f"Error in the child process: {e}")


if __name__ == "__main__":
    logging.info("Starting and configuring application...")
    # Create queue to transfer data from analytic process to read text process
    image_queue = Queue()
    response_text_queue = Queue()

    # Create a shared value to inform to capture a new image
    event_done = Value(ctypes.c_bool, True)

    # Create processes
    capture_images = Capture_Pics(image_queue, event_done)
    analytic_process = Analytic_Process(response_text_queue, image_queue)
    read_texts = Read_Texts(response_text_queue, event_done)

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

import streamlit as st
import os
import sys
import time
import logging
import logging_config

from PIL import Image
from pathlib import Path


# Calculate the project root path directly
project_root_path = Path(__file__).resolve().parent.parent
# Add the project root to sys.path
sys.path.append(str(project_root_path))
# Configure logging
filename = project_root_path / "logs/ui.log"
logging_config.config_logging(filename)
logging.info("------------------------Start logging for ui.py -------------------------------")

# Set page title and favicon.
st.set_page_config(page_title="chatGPT + ElevenLabs", page_icon="💥")

# show title
st.markdown('# chatGPT + ElevenLabs')

# Initialize session state.
width, height = 100, 100
if 'last_image' not in st.session_state:
    st.session_state['last_image'] = Image.new('RGB', (width, height), 'grey')
    logging.info("Default gray image created.")
    st.session_state['last_modified_time'] = 0

image_path = project_root_path / "artifacts/frames/frame.jpg"
analysis_results_path = project_root_path / "artifacts/response_text/response_text.txt"

# show the current image and the last image in two columns
col1, col2 = st.columns([3, 1])
placeholder1 = col1.empty()
placeholder2 = col2.empty()

with placeholder1:
    st.markdown('## Current Image')
    # get picture from artifacts/frames/frame.jpg
    if os.path.exists(image_path):
        logging.info("Loading image from artifacts/frames/frame.jpg.")
        # if the image exists, show the image
        current_image = Image.open(image_path)
    else:
        # if the image does not exist, show the default image
        current_image = st.session_state['last_image']

    width, height = current_image.size
    st.image(current_image, caption='Captured Image', use_column_width=True)

with placeholder2:
    st.markdown('## Last Image')
    resized_image = st.session_state['last_image'].resize(
        (int(width * 0.5), int(height * 0.5)))
    # # This will create a lot of empty space on top, pushing the image to the bottom
    # # You may need to adjust the number of empty spaces based on your layout
    # for _ in range(int(height / 40)):
    #     st.write(" ")
    # show the last image
    st.image(resized_image, caption='Last Captured Image', use_column_width=True)

# show the analysis results
st.markdown('## Analysis Results')
# Read the analysis results from the file
with open(analysis_results_path, 'r', encoding='utf-8') as file:
    analysis_result = file.read()
st.write(analysis_result)


def check_for_updates():
    try:
        if os.path.exists(analysis_results_path):
            modification_time = os.path.getmtime(analysis_results_path)
            if modification_time != st.session_state['last_modified_time']:
                logging.info("Loading new analysis results and image.")
                st.session_state['last_modified_time'] = modification_time
                st.session_state['last_image'] = current_image
                st.experimental_rerun()
    except Exception as e:
        st.error(f"Error checking file update: {e}")


if st.button('check updates'):
    check_for_updates()

# # Check for file update periodically
# while True:
#     # Be cautious with the sleep duration; too short may cause performance issues
#     time.sleep(1)
#     check_for_updates()

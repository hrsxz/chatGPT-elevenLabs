# ChatGPT with ElevenLabs

📂 Project Organization
------------
    ├── 📂 src                <- Main code base
    │   ├── 📂 chatGPT     
    │   ├── 📂 elevenLabs
    ├── 📂 venv               <- Virtual environment
    ├── 📃 main.py            <- Project configuration - contains 
    ├── 📃 README.md          <- The top-level README for info about this project.
    ├── 📃 requirments.txt    <- Requirements file for this project

## Install Tesseract-OCR

- If you haven't already installed Tesseract-OCR, you need to download and install it from the official [Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract) or use a precompiled binary suitable for your system.
- download windows install package and save in micellaneous:
  [Tesseract GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki)

### Add Tesseract to PATH

  1. Find the installation directory of Tesseract-OCR. It's usually something like `C:\Program Files\Tesseract-OCR` where the `tesseract.exe` is located.
  2. Open the Start Search, type in "env", and choose "Edit the system environment variables".
  3. In the Edit Environment Variables window, click New and paste the path to the Tesseract-OCR directory.
  4. Click OK in all windows to apply the changes.

  5. After you have installed Tesseract and added it to your PATH, restart your PowerShell session to ensure that the new PATH is loaded. Also, restart any IDE or editor where you are running the Python script to recognize the changes to the environment variables.

### Verify Installation

- To verify that Tesseract is correctly installed and accessible from your PATH, run the following command in your PowerShell:

  ```powershell
  tesseract --version
  ```

## Import file from source code directory

In this project, we are adding __init__.py in order to package the source code in one package inorder to import it easily at any other py file.

### Step 1: Modify the Project Structure

You need to add an `__init__.py` file to the `src` directory so that Python will treat it as a package.

### Step 2: Modify the Import Statements

```python
from chatGPT import gpt_utils

gpt_utils.test_connection()
```

## Install ffmpeg for play audio function from eleven labs

```python
from elevenlabs import generate, play

audio = generate(text, voice="DPsqCHWEBVTyO9962K8u")
play(audio)
```

### Download ffmpeg (Window version)

1. Download the appropriate version for Windows ([Go to the FFmpeg Download Page](https://github.com/BtbN/FFmpeg-Builds/releases)
).

2. Extract the files to a directory (e.g., C:\ffmpeg). And add ffmpeg to the System Path.

3. Verify Installation:

    ```powershell
    tesseract --version
    ```

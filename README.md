# Virtual-Try-on-and-Apparel-Recommendation

# Virtual-Try-on-and-Apparel-Recommendation

Virtual Try-On System with Apparel Recommendation Engine
Overview
This project is a Virtual Try-On System with Apparel Recommendation Engine that allows users to upload a clothing image to receive recommendations for similar apparel and perform virtual try-on by overlaying selected apparel onto a person’s image. The system consists of two main components:

Backend (main.py): A Flask server that uses:
FashionCLIP (patrickjohncyh/fashion-clip) for generating apparel recommendations based on visual similarity.
Stable Diffusion Img2Img Pipeline (runwayml/stable-diffusion-v1-5) as a placeholder for virtual try-on (replaceable with IDM-VTON for better results).


Frontend (frontend.py): A Streamlit web interface for uploading images, displaying recommendations, and showing try-on results.

The system uses a local folder (backend/apparel_images/) as a database of clothing images for recommendations, populated with images from the Fashion Product Images Dataset (Small) or similar sources.
Project Structure
root/
├── backend/
│   ├── apparel_images/  # Clothing images for recommendations (e.g., 10001.jpg, red_shirt_1.jpg)
│   ├── main.py         # Flask backend (recommendation and try-on APIs)
├── frontend/
│   ├── frontend.py     # Streamlit frontend (user interface)
│   ├── requirements.txt # Frontend dependencies
├── venv/               # Virtual environment
├── README.md           # This file

Prerequisites

Python: Version 3.13.7 (or 3.12.x if compatibility issues arise).
Hardware: A GPU (NVIDIA with CUDA 11.8 or 12.1) is recommended for faster model inference, but CPU works.
Disk Space: ~5GB for model weights (FashionCLIP, Stable Diffusion) and ~600MB for the Kaggle dataset.
Internet: Required for downloading models and dataset on first run.
Kaggle Account: For downloading the dataset.
ngrok Account (optional for Colab): For exposing the Streamlit app publicly.

Setup Instructions
1. Clone or Set Up the Project

Create a project folder: C:\Users\YourUsername\Virtual Try On and Apparel Recommendation-Engine\root\.
Place main.py in root\backend\ and frontend.py in root\frontend\.
Alternatively, download the project files from your repository (if applicable).

2. Create and Activate Virtual Environment

Open a terminal in VSCode (Terminal > New Terminal) or Command Prompt.
Create a virtual environment:python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS


Verify Python version:python --version  # Should show 3.13.7



3. Install Dependencies

Backend Dependencies:
Install required packages:pip install flask torch transformers diffusers pillow numpy scikit-learn


For GPU support (if you have an NVIDIA GPU):
Check CUDA version with nvidia-smi (e.g., CUDA 11.8).
Install PyTorch with CUDA:pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


For CUDA 12.1, use --index-url https://download.pytorch.org/whl/cu121.




Frontend Dependencies:
Navigate to root\frontend\:cd frontend


Create or use the requirements.txt:streamlit==1.38.0
requests==2.32.3
pillow==10.4.0


Install:pip install -r requirements.txt





4. Set Up apparel_images/ Folder

Purpose: This folder stores clothing images (e.g., .jpg, .png) for the recommendation engine.
Location: root\backend\apparel_images\ (as expected by main.py).
Steps:
Create the folder in VSCode:
Right-click root\backend\ > New Folder > Name it apparel_images.


Download the Fashion Product Images Dataset (Small) (~572MB, ~4,400 images):
Sign in to Kaggle, download fashion-product-images-small.zip.
Unzip to find the images/ folder with .jpg files (e.g., 10001.jpg).


Copy 50–100 images to root\backend\apparel_images\:
In File Explorer, select images from images/.
Drag-and-drop into root\backend\apparel_images\ in VSCode.


Alternative: Download free clothing images from Unsplash (search "clothing flat lay") and save as .jpg in apparel_images/.



5. Run the Application

Start the Backend:
Open a terminal in VSCode, activate venv:.\venv\Scripts\activate
cd backend
python main.py


The Flask server starts on http://localhost:5000. Keep this terminal open.
Note: First run downloads ~5GB of model weights (FashionCLIP, Stable Diffusion).


Start the Frontend:
Open a new terminal tab (Terminal > New Terminal), activate venv:.\venv\Scripts\activate
cd frontend
streamlit run frontend.py


The Streamlit app opens in your browser at http://localhost:8501.



6. Usage

Apparel Recommendation:
Upload a clothing image (.jpg or .png) in the "Apparel Recommendation" section.
Click "Get Recommendations" to see up to 5 similar items from apparel_images/.


Virtual Try-On:
Upload a person image and an apparel image (or select from recommendations).
Click "Try On" to generate a virtual try-on image (currently uses Stable Diffusion; replace with IDM-VTON for better results).



Running on Google Colab
To run in Google Colab (useful for free GPU access):

Create a new notebook at colab.research.google.com.
Set runtime to GPU: Runtime > Change runtime type > GPU.
Copy-paste and run the following cells (requires a free ngrok account for public access):

# Install dependencies
!pip install -q flask streamlit pyngrok torch transformers diffusers pillow numpy scikit-learn requests

# Download Kaggle dataset
from google.colab import files
uploaded = files.upload()  # Upload kaggle.json
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d paramaggarwal/fashion-product-images-small
!unzip -q fashion-product-images-small.zip

# Create apparel_images and copy 100 images
import os
import shutil
os.makedirs('apparel_images', exist_ok=True)
source_dir = 'images'
image_files = [f for f in os.listdir(source_dir) if f.endswith('.jpg')][:100]
for file in image_files:
    shutil.copy(os.path.join(source_dir, file), 'apparel_images')

# Create backend.py
%%writefile backend.py
# [Insert your main.py code here, with BASE_DIR = Path("/content") and apparel_dir = BASE_DIR / "apparel_images"]

# Create frontend.py
%%writefile frontend.py
# [Insert your frontend.py code here, with rec_img = Image.open(f"apparel_images/{rec}")]

# Run Flask in background
import subprocess
subprocess.Popen(["python", "backend.py"])
import time
time.sleep(5)

# Set up ngrok and run Streamlit
from pyngrok import ngrok
!ngrok authtoken YOUR_NGROK_AUTHTOKEN  # Replace with your token
ngrok.kill()
get_ipython().system_raw('streamlit run frontend.py &')
public_url = ngrok.connect(8501, "http")
print(f"Streamlit app at: {public_url}")


Access the app via the ngrok URL (e.g., https://xxxx.ngrok-free.app).

Troubleshooting

ModuleNotFoundError: Ensure venv is activated and dependencies are installed (pip install -r frontend/requirements.txt for frontend, additional packages for backend).
FileNotFoundError for apparel_images/: Verify root\backend\apparel_images\ exists with .jpg or .png files. Move images there or update paths in main.py and frontend.py.
Model Loading Errors: Ensure ~5GB disk space and stable internet for downloading FashionCLIP/Stable Diffusion. Use CPU if GPU memory is low (device = "cpu" in main.py).
Port Conflicts: If localhost:5000 is in use, change to port=5001 in main.py and update frontend.py URLs.
Colab Timeouts: Sessions reset after ~12 hours. Save apparel_images/ to Google Drive for persistence.

Future Improvements

Replace Stable Diffusion with IDM-VTON for realistic try-on.
Cache apparel_images/ embeddings to disk to speed up backend startup.
Add category filtering (e.g., using styles.csv from Kaggle dataset).
Deploy to a cloud platform (e.g., Heroku, AWS) for production use.

License
MIT License (or specify your preferred license).

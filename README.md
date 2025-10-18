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




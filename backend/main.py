from flask import Flask, request, jsonify
import torch
from transformers import AutoProcessor, AutoModel
from diffusers import StableDiffusionPipeline  # For try-on (adapt IDM-VTON)
from PIL import Image
import numpy as np
import base64
import io
import os
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load recommendation model: FashionCLIP for fashion-specific embeddings
rec_processor = AutoProcessor.from_pretrained("patrickjohncyh/fashion-clip")
rec_model = AutoModel.from_pretrained("patrickjohncyh/fashion-clip")
rec_model.eval()

# Precompute embeddings for apparel database (run once)
apparel_dir = os.path.join(os.path.dirname(__file__), 'backend', 'apparel_images')  # Folder with apparel JPGs from dataset
apparel_files = [f for f in os.listdir(apparel_dir) if f.endswith('.jpg')]
apparel_embeddings = []
for file in apparel_files:
    img = Image.open(os.path.join(apparel_dir, file)).convert('RGB')
    inputs = rec_processor(images=img, return_tensors="pt")
    with torch.no_grad():
        embeds = rec_model.get_image_features(**inputs).numpy()
    apparel_embeddings.append(embeds.flatten())
apparel_embeddings = np.array(apparel_embeddings)

# Load try-on model: Use IDM-VTON (requires diffusers; adapt from HF repo)
# Note: For full IDM-VTON, clone https://github.com/yisol/IDM-VTON and integrate.
# Here, placeholder with StableDiffusion for simplicity (replace with actual inference).
tryon_pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
tryon_pipe = tryon_pipe.to("cuda" if torch.cuda.is_available() else "cpu")

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    user_image_base64 = data['user_image']  # Base64 encoded image
    user_img = Image.open(io.BytesIO(base64.b64decode(user_image_base64))).convert('RGB')
    
    # Get user image embedding
    inputs = rec_processor(images=user_img, return_tensors="pt")
    with torch.no_grad():
        user_embed = rec_model.get_image_features(**inputs).numpy().flatten()
    
    # Find top 5 similar apparel
    similarities = cosine_similarity([user_embed], apparel_embeddings)[0]
    top_indices = np.argsort(similarities)[-5:][::-1]
    recommendations = [apparel_files[i] for i in top_indices]
    
    return jsonify({'recommendations': recommendations})

@app.route('/tryon', methods=['POST'])
def tryon():
    data = request.json
    person_base64 = data['person_image']
    apparel_base64 = data['apparel_image']
    
    person_img = Image.open(io.BytesIO(base64.b64decode(person_base64)))
    apparel_img = Image.open(io.BytesIO(base64.b64decode(apparel_base64)))
    
    # Placeholder try-on logic (replace with IDM-VTON inference)
    # Example prompt-based diffusion: "Person wearing this apparel"
    prompt = "A person wearing the given apparel, high detail"
    tried_on_img = tryon_pipe(prompt, init_image=person_img, strength=0.75).images[0]
    
    # Encode result as base64
    buffered = io.BytesIO()
    tried_on_img.save(buffered, format="PNG")
    tried_on_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({'tried_on_image': tried_on_base64})

if __name__ == '__main__':
    app.run(port=5000)
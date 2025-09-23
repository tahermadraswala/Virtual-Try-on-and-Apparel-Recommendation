import streamlit as st
import requests
import base64
from PIL import Image
import io

st.title("Virtual Try-On System with Apparel Recommendations")

# Section 1: Recommendation
st.header("Apparel Recommendation")
user_image = st.file_uploader("Upload an image for recommendations", type=['jpg', 'png'])
if user_image:
    img = Image.open(user_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    # Encode to base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    if st.button("Get Recommendations"):
        response = requests.post("http://localhost:5000/recommend", json={'user_image': img_base64})
        recs = response.json()['recommendations']
        st.subheader("Recommended Apparel:")
        for rec in recs:
            rec_img = Image.open(f"apparel_images/{rec}")
            st.image(rec_img, width=150)

# Section 2: Virtual Try-On
st.header("Virtual Try-On")
person_image = st.file_uploader("Upload person image", type=['jpg', 'png'], key="person")
apparel_image = st.file_uploader("Upload apparel image (or select from recommendations)", type=['jpg', 'png'], key="apparel")

if person_image and apparel_image:
    person_img = Image.open(person_image)
    apparel_img = Image.open(apparel_image)
    col1, col2 = st.columns(2)
    col1.image(person_img, caption="Person", use_column_width=True)
    col2.image(apparel_img, caption="Apparel", use_column_width=True)
    
    # Encode to base64
    person_buffered = io.BytesIO()
    person_img.save(person_buffered, format="JPEG")
    person_base64 = base64.b64encode(person_buffered.getvalue()).decode()
    
    apparel_buffered = io.BytesIO()
    apparel_img.save(apparel_buffered, format="JPEG")
    apparel_base64 = base64.b64encode(apparel_buffered.getvalue()).decode()
    
    if st.button("Try On"):
        response = requests.post("http://localhost:5000/tryon", json={
            'person_image': person_base64,
            'apparel_image': apparel_base64
        })
        tried_on_base64 = response.json()['tried_on_image']
        tried_on_img = Image.open(io.BytesIO(base64.b64decode(tried_on_base64)))
        st.image(tried_on_img, caption="Virtual Try-On Result", use_column_width=True)
import streamlit as st
import os
from PIL import Image
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import GlobalMaxPooling2D
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.neighbors import NearestNeighbors
from numpy.linalg import norm

# Set Streamlit Theme to Light
st.set_page_config(layout='wide')

# Load data and model
feature_list = np.array(pickle.load(open('embeddings.pkl', 'rb')))
filenames = pickle.load(open('filenames.pkl', 'rb'))

model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
model.trainable = False

model = tf.keras.Sequential([
    model,
    GlobalMaxPooling2D()
])

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.error("An error occurred while saving the file.")
        return False

# Function for feature extraction
def feature_extraction(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result

# Function for recommendation
def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])
    return indices

import streamlit as st
import os
from PIL import Image

# Header and File Upload Section
st.title('👗 Fashion Recommender System')

# Upload section
st.subheader("Upload Your Image")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

paths = [
    "E:\Projects\EY\IMGSS\Screenshot 2024-01-08 004553.png",
    "E:\Projects\EY\IMGSS\Screenshot 2024-01-08 004629.png",
    "E:\Projects\EY\IMGSS\Screenshot 2024-01-08 004636.png",
    "E:\Projects\EY\IMGSS\Screenshot 2024-01-08 004646.png",
    "E:\Projects\EY\IMGSS\Screenshot 2024-01-08 004653.png"
]

if uploaded_file:
    if save_uploaded_file(uploaded_file):
        # Display the uploaded image
        st.subheader("Uploaded Image")
        display_image = Image.open(uploaded_file)
        st.image(display_image, caption='Uploaded Image', width=250)

        # Display recommended images from paths
        st.subheader("Similar Products")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        for idx, col in zip(paths, [col1, col2, col3, col4, col5]):
            recommended_image = Image.open(idx)
            col.image(recommended_image, caption='Recommended Product', width=250)
    else:
        st.error("An error occurred during file upload.")

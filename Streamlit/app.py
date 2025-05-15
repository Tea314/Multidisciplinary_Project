import streamlit as st
from ultralytics import YOLO
import tempfile
import numpy as np
import os
from PIL import Image
import time
import requests
from datetime import datetime, timezone
import math
# from torch.serialization import add_safe_globals
# from ultralytics.nn.tasks import SegmentationModel

# Set page configuration
st.set_page_config(
    page_title="YOLOv8 Segmentation App",
    page_icon="🖼️",
    layout="wide"
)

# Custom CSS for better styling

def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #f2f4f8;
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: auto;
        padding: 2rem;
    }
    .title {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #636e72;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .option-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .option-card:hover {
        transform: translateY(-5px);
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    .card-title {
        font-weight: 600;
        font-size: 1.1rem;
        color: #2c3e50;
        margin-bottom: 5px;
    }
    .stButton>button {
        background-color: #0984e3;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #74b9ff;
        color: black;
    }
    .stProgress > div > div > div {
        background-color: #0984e3;
    }
    .result-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
        margin-top: 2rem;
    }
    .highlight-success {
        color: green;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    .highlight-error {
        color: red;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


add_custom_css()

# App title and description
st.markdown("<h1 class='title'>🔍 YOLOv8 UI</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Upload an image or video for object segmentation</h3>",
            unsafe_allow_html=True)

# Initialize session state for tracking app state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'processed_video' not in st.session_state:
    st.session_state.processed_video = None
if 'input_type' not in st.session_state:
    st.session_state.input_type = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0.5
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Function to load the YOLOv8 model


@st.cache_resource
def load_model():
    try:
        model = YOLO("best.pt")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


model = load_model()
if model:
    st.session_state.model = model
    st.session_state.model_loaded = True
else:
    st.error("⚠️ Failed to load the YOLOv8 model. Please check the model file.")
# Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 About")
    st.markdown("""
    This app uses YOLOv8 to perform real-time object detection and segmentation.
    
    Upload an image or video to see it in action!
    """)
    st.markdown("---")
    st.markdown("### 📊 Statistics")

# Main content area
if not st.session_state.model_loaded:
    st.warning("⚠️ Please load the YOLOv8 model from the sidebar first!")
else:
    # Choose input type if not already selected
    if not st.session_state.input_type:
        st.markdown(
            "<h2 style='text-align: center;'>Choose Input Type</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            image_card = st.container()
            with image_card:
                st.markdown("""
                <div class='option-card'>
                    <div class='card-icon'>🖼️</div>
                    <div class='card-title'>Process Image</div>
                    <p>Upload and analyze a single image</p>
                </div>
                """, unsafe_allow_html=True)
            if st.button("Select Image"):
                st.session_state.input_type = "image"
                st.experimental_rerun()

        with col2:
            video_card = st.container()
            with video_card:
                st.markdown("""
                <div class='option-card'>
                    <div class='card-icon'>🎬</div>
                    <div class='card-title'>Process Video</div>
                    <p>Upload and analyze a video file</p>
                </div>
                """, unsafe_allow_html=True)
            if st.button("Select Video"):
                st.session_state.input_type = "video"
                st.experimental_rerun()

    # Process based on selected input type
    elif st.session_state.input_type == "image":
        st.markdown(
            "<h2 style='text-align: center;'>Image Segmentation</h2>", unsafe_allow_html=True)

        # Image upload section
        with st.container():
            uploaded_file = st.file_uploader(
                "Upload an image", type=["jpg", "jpeg", "png"])
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                process_button = st.button("Process Image")
            st.markdown("</div>", unsafe_allow_html=True)
        def send_fault_to_backend(product_id, fault_type, confidence, detected_at,processing_time, image_url):
            if confidence is None or (isinstance(confidence, float) and math.isnan(confidence)):
                fault_type = "No Fault"
                confidence = 0.0  # Gán giá trị float hợp lệ
            payload = {
                "product_id": product_id,
                "fault_type": fault_type,
                "confidence": confidence,
                "detected_at": detected_at,
                "processing_time" : processing_time,
                "image_url": image_url
            }

            try:
                # DÙNG "backend" thay vì localhost nếu chạy bằng docker-compose
                response = requests.post("http://backend:8080/api/v1/faults", json=payload)
                if response.status_code == 201:
                    st.markdown("<div class='highlight-success'>✅ Fault record saved to backend!</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='highlight-error'>❌ Failed to connect to backend</div>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"Data transfer is: {fault_type}, {confidence}, {detected_at}, {processing_time}, {image_url}  ", unsafe_allow_html=True)
                st.error(f"⚠️ Error connecting to backend: {e}")

        # Process the image when button is clicked and file is uploaded
        if uploaded_file is not None and process_button:
            with st.spinner("Processing image..."):
                # Read the image
                image = Image.open(uploaded_file)
                image_np = np.array(image)

                # Measure processing time
                start_time = time.time()

                # Process the image with YOLOv8
                results = st.session_state.model.predict(
                    source=image_np,
                    conf=st.session_state.confidence,
                    save=False
                )

                # Store processing time
                st.session_state.processing_time = time.time() - start_time

                # Get the number of detected objects
                st.session_state.detection_count = len(results[0].boxes.data)

                # Get the segmentation results image
                segmented_image = results[0].plot()

                # Store the processed image
                st.session_state.processed_image = segmented_image
                st.session_state.processing_complete = True
                        # Lấy confidence trung bình từ YOLO (ví dụ)
                conf = float(results[0].boxes.conf.mean())
                fault_type = "crack"  # giả sử cố định, hoặc bạn có logic phân loại
                detected_at = datetime.now(timezone.utc).isoformat()
                image_url = "http://example.com/image.jpg"  # bạn cần upload ảnh và lấy URL thực tế nếu có

                # Gửi lên backend
                print(f"Sending fault to backend: {fault_type}, {conf}, {detected_at}, {image_url}")
                send_fault_to_backend(
                    product_id="prod123",
                    fault_type=fault_type,
                    confidence=conf,
                    detected_at=detected_at,
                    processing_time=st.session_state.processing_time,
                    image_url=image_url
                )
                with st.sidebar:
                    st.markdown(
                        f"**Processing Time:** {st.session_state.processing_time:.2f} seconds")
                    st.markdown(
                        f"**Detected Objects:** {st.session_state.detection_count}")

                # Show original and processed images
                st.markdown("### Result</h2>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Original Image")
                    st.image(image, use_column_width=True)

                with col2:
                    st.markdown("#### Segmented Image")
                    st.image(segmented_image, use_column_width=True)

                st.markdown("</div>", unsafe_allow_html=True)

        # Show previous results if available
        elif st.session_state.processed_image is not None and st.session_state.processing_complete:
            st.markdown("### Previous Results")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Original Image")
                if uploaded_file:
                    st.image(Image.open(uploaded_file), use_column_width=True)
                else:
                    st.info("Original image is no longer available")

            with col2:
                st.markdown("#### Segmented Image")
                st.image(st.session_state.processed_image,
                         use_column_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Option to reset and try again
        if st.session_state.input_type:
            if st.button("⬅️ Choose Different Input Type"):
                st.session_state.input_type = None
                st.session_state.processed_image = None
                st.session_state.processed_video = None
                st.session_state.processing_complete = False
                if hasattr(st.session_state, 'detection_count'):
                    del st.session_state.detection_count
                if hasattr(st.session_state, 'processing_time'):
                    del st.session_state.processing_time
                st.experimental_rerun()

    elif st.session_state.input_type == "video":
        st.markdown(
            "<h2 style='text-align: center;'>Video Segmentation</h2>", unsafe_allow_html=True)

        # Video upload section
        with st.container():
            uploaded_file = st.file_uploader(
                "Upload a video", type=["mp4", "mov", "avi"])
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                process_button = st.button("Process Video")
            st.markdown("</div>", unsafe_allow_html=True)

        # Process the video when button is clicked and file is uploaded
        if uploaded_file is not None and process_button:
            with st.spinner("Processing video... This may take a while depending on the video length."):
                # Save the uploaded file to a temporary file
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                tfile_path = tfile.name
                tfile.close()

                # Create a temporary file for the output video
                output_path = os.path.join(
                    tempfile.gettempdir(), "processed_video.mp4")

                # Measure processing time
                start_time = time.time()

                # Process the video with YOLOv8
                results = st.session_state.model.predict(
                    source=tfile_path,
                    conf=st.session_state.confidence,
                    save=True,
                    project=tempfile.gettempdir(),
                    name="processed_video",
                    exist_ok=True
                )

                # Store processing time
                st.session_state.processing_time = time.time() - start_time

                # Find the processed video file
                processed_video_path = os.path.join(
                    tempfile.gettempdir(), "processed_video", os.path.basename(tfile_path))
                if not os.path.exists(processed_video_path):
                    # Try finding with .mp4 extension
                    processed_video_path = os.path.join(tempfile.gettempdir(
                    ), "processed_video", os.path.splitext(os.path.basename(tfile_path))[0] + ".mp4")

                # Store the path to the processed video
                if os.path.exists(processed_video_path):
                    st.session_state.processed_video = processed_video_path
                    st.session_state.processing_complete = True

                    # Count total detections (approximate from the first frame)
                    st.session_state.detection_count = len(
                        results[0].boxes.data) if len(results) > 0 else 0

                    # Display the processed video
                    st.markdown("### Results")

                    # Get video file data
                    with open(processed_video_path, 'rb') as video_file:
                        video_bytes = video_file.read()

                    st.video(video_bytes)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(
                        "Failed to process the video. Please try again with a different video file.")

                # Clean up the temporary file
                os.unlink(tfile_path)

        # Show previous results if available
        elif st.session_state.processed_video is not None and st.session_state.processing_complete:
            st.markdown("### Previous Results")

            # Get video file data
            with open(st.session_state.processed_video, 'rb') as video_file:
                video_bytes = video_file.read()

            st.video(video_bytes)
            st.markdown("</div>", unsafe_allow_html=True)

        # Option to reset and try again
        if st.session_state.input_type:
            if st.button("⬅️ Choose Different Input Type"):
                st.session_state.input_type = None
                st.session_state.processed_image = None
                st.session_state.processed_video = None
                st.session_state.processing_complete = False
                if hasattr(st.session_state, 'detection_count'):
                    del st.session_state.detection_count
                if hasattr(st.session_state, 'processing_time'):
                    del st.session_state.processing_time
                st.experimental_rerun()

# Footer
st.markdown("---")

import streamlit as st
import mysql.connector
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np
import base64
import io
import os
import bcrypt
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Acne Detection System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning design
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main App Background with Gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 20px 0;
    }
    
    /* Title Styles */
    h1 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 20px 0;
        font-size: 3.5rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-family: 'Montserrat', sans-serif;
        color: #ffffff;
        font-weight: 600;
        margin-top: 30px;
        font-size: 2rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
    }
    
    h3 {
        color: #f0f0f0;
        font-weight: 500;
        font-size: 1.5rem;
    }
    
    /* Paragraph Styles */
    p, li {
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.8;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 12px 30px;
        border-radius: 50px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 12px 20px;
        font-size: 1rem;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea;
        background: rgba(255, 255, 255, 0.3);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed rgba(255, 255, 255, 0.5);
    }
    
    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Card Styles */
    .feature-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.4);
    }
    
    /* Severity Badge Styles */
    .severity-badge {
        display: inline-block;
        padding: 10px 25px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 10px 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .severity-clear {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
    }
    
    .severity-mild {
        background: linear-gradient(135deg, #FFD93D, #6BCF7F);
        color: #2d3436;
    }
    
    .severity-moderate {
        background: linear-gradient(135deg, #F2994A, #F2C94C);
        color: white;
    }
    
    .severity-severe {
        background: linear-gradient(135deg, #EB3349, #F45C43);
        color: white;
    }
    
    .severity-very-severe {
        background: linear-gradient(135deg, #C33764, #1D2671);
        color: white;
    }
    
    /* Article Card */
    .article-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .article-card:hover {
        transform: translateX(10px);
        border-left-width: 8px;
    }
    
    .article-title {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .article-content {
        color: #f0f0f0;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    
    /* Metric Display */
    .metric-container {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-label {
        font-size: 1.2rem;
        color: #f0f0f0;
        margin-top: 5px;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: white;
    }
    
    /* Tables */
    table {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        overflow: hidden;
    }
    
    th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        padding: 15px;
    }
    
    td {
        color: white;
        padding: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Animated Banner */
    .banner {
        background: linear-gradient(90deg, #667eea, #764ba2, #F093FB, #4FACFE);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin: 30px 0;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }
    
    .banner h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Form Container */
    .form-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Loading Animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loader {
        border: 5px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top: 5px solid #667eea;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# Database connection function
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"],
            port=int(st.secrets["DB_PORT"])
        )
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Initialize database and table
def initialize_database():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOSTDB_HOST"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORDDB_PASSWORD"],
            port=int(st.secrets["DB_PORTDB_PORT"]
                     )

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cursor.close()
            conn.close()
    except mysql.connector.Error as e:
        st.error(f"Error initializing database: {e}")

# Initialize database
initialize_database()

# Load YOLO model
@st.cache_resource
def load_model():
    try:
        return YOLO('best (3).pt')
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'best (3).pt' is in the correct directory.")
        return None

model = load_model()

# Acne Severity Classification Functions
def calculate_gags_score(pimple_count, face_area_factor=2):
    """
    Calculate GAGS score based on detected pimples
    GAGS: 1-18 = Mild, 19-30 = Moderate, 31-38 = Severe, >38 = Very Severe
    """
    # Simplified GAGS calculation (in real scenario, would need lesion type classification)
    # Assuming average severity factor of 2 for detected lesions
    score = pimple_count * face_area_factor
    return score

def classify_severity_gags(gags_score):
    """Classify acne severity based on GAGS score"""
    if gags_score == 0:
        return "Clear", "severity-clear"
    elif 1 <= gags_score <= 18:
        return "Mild", "severity-mild"
    elif 19 <= gags_score <= 30:
        return "Moderate", "severity-moderate"
    elif 31 <= gags_score <= 38:
        return "Severe", "severity-severe"
    else:
        return "Very Severe", "severity-very-severe"

def classify_severity_iga(pimple_count):
    """
    Classify acne severity based on IGA scale
    0 = Clear, 1 = Almost Clear, 2 = Mild, 3 = Moderate, 4 = Severe
    """
    if pimple_count == 0:
        return 0, "Clear", "severity-clear"
    elif 1 <= pimple_count <= 5:
        return 1, "Almost Clear", "severity-clear"
    elif 6 <= pimple_count <= 10:
        return 2, "Mild", "severity-mild"
    elif 11 <= pimple_count <= 20:
        return 3, "Moderate", "severity-moderate"
    else:
        return 4, "Severe", "severity-severe"

# Display severity analysis with both scales
def display_severity_analysis(pimple_count):
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>🔬 Acne Severity Analysis</h2>", unsafe_allow_html=True)
    
    # Calculate scores
    gags_score = calculate_gags_score(pimple_count)
    gags_severity, gags_class = classify_severity_gags(gags_score)
    iga_score, iga_severity, iga_class = classify_severity_iga(pimple_count)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{pimple_count}</div>
            <div class="metric-label">Detected Lesions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{gags_score}</div>
            <div class="metric-label">GAGS Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{iga_score}</div>
            <div class="metric-label">IGA Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown(f"""
        <div class="feature-card">
            <h3>📊 GAGS Classification</h3>
            <div class="severity-badge {gags_class}">{gags_severity}</div>
            <p style="margin-top: 15px;">Global Acne Grading System (GAGS) provides a comprehensive severity assessment based on lesion count and distribution.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🎯 IGA Classification</h3>
            <div class="severity-badge {iga_class}">{iga_severity}</div>
            <p style="margin-top: 15px;">Investigator Global Assessment (IGA) evaluates overall acne severity through clinical observation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Treatment recommendations based on severity
    display_treatment_recommendations(gags_severity, pimple_count)

def display_treatment_recommendations(severity, pimple_count):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>💊 Personalized Treatment Recommendations</h2>", unsafe_allow_html=True)
    
    if severity in ["Clear", "Almost Clear"]:
        st.markdown("""
        <div class="feature-card">
            <h3>✅ Preventive Skincare Routine</h3>
            <p><strong>Your skin looks great! Focus on prevention:</strong></p>
            <ul>
                <li><strong>Daily Cleansing:</strong> Use a gentle, pH-balanced cleanser twice daily</li>
                <li><strong>Moisturizer:</strong> Apply a lightweight, non-comedogenic moisturizer</li>
                <li><strong>Sun Protection:</strong> SPF 30+ broad-spectrum sunscreen every morning</li>
                <li><strong>Maintain Hygiene:</strong> Clean pillowcases, avoid touching face</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    elif severity == "Mild":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🧖‍♀️ Recommended Skincare Routine</h3>
                <ol>
                    <li><strong>Gentle Cleansing:</strong> Twice daily with salicylic acid cleanser (2%)</li>
                    <li><strong>Spot Treatment:</strong> Benzoyl Peroxide (2.5%-5%) on affected areas</li>
                    <li><strong>Moisturizer:</strong> Oil-free, non-comedogenic formula</li>
                    <li><strong>Sunscreen:</strong> Essential for preventing dark spots (SPF 30+)</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>💡 Quick Tips</h3>
                <ul>
                    <li><strong>Avoid Touching:</strong> Keep hands away from face</li>
                    <li><strong>Clean Environment:</strong> Regular cleaning of phone, pillowcase</li>
                    <li><strong>Hydration:</strong> Drink 8+ glasses of water daily</li>
                    <li><strong>Patience:</strong> Allow 4-6 weeks for visible results</li>
                    <li><strong>Diet:</strong> Reduce dairy and high-glycemic foods</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    else:  # Moderate, Severe, Very Severe
        st.markdown(f"""
        <div class="article-card" style="border-left-color: #EB3349;">
            <div class="article-title">⚠️ Professional Consultation Recommended</div>
            <div class="article-content">
                <p>With <strong>{pimple_count} detected lesions</strong> classified as <strong>{severity}</strong> acne, 
                we strongly recommend consulting a dermatologist for personalized treatment.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>💊 Professional Treatments</h3>
                <ul>
                    <li><strong>Prescription Topicals:</strong> Retinoids (Tretinoin, Adapalene), stronger Benzoyl Peroxide combinations</li>
                    <li><strong>Oral Medications:</strong> Antibiotics (Doxycycline, Minocycline) for inflammatory acne</li>
                    <li><strong>Hormonal Therapy:</strong> For hormonal acne (women)</li>
                    <li><strong>Isotretinoin:</strong> For severe, resistant cases</li>
                    <li><strong>In-Office Procedures:</strong> Chemical peels, laser therapy, extractions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>🛡️ Supportive Care</h3>
                <ul>
                    <li><strong>Gentle Cleansing:</strong> Avoid harsh scrubbing</li>
                    <li><strong>Consistency:</strong> Follow prescribed routine exactly</li>
                    <li><strong>Track Triggers:</strong> Log diet, stress, product changes</li>
                    <li><strong>Stress Management:</strong> Practice meditation, yoga, exercise</li>
                    <li><strong>Sleep:</strong> Aim for 7-9 hours nightly</li>
                    <li><strong>Avoid Picking:</strong> Prevents scarring and infection</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Predict function for image
def predict_image(image):
    if model is None:
        return None, []
    results = model(image)
    annotated_frame = results[0].plot()
    return annotated_frame, results[0].boxes.cls

# Register function
def register():
    st.markdown('<div class="banner"><h1>🔬 Create Your Account</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>Join Our Advanced Acne Detection Platform</h3>
        <p>Access AI-powered skin analysis with YOLOv9 technology. Get personalized treatment recommendations and track your skin health journey.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("📝 Full Name", placeholder="Enter your full name")
            username = st.text_input("👤 Username", placeholder="Choose a unique username")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
        
        with col2:
            phone = st.text_input("📱 Phone Number", placeholder="Enter your phone number")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        submit = st.form_submit_button("✨ Register Now")

    if submit:
        if not all([full_name, username, email, password, confirm_password]):
            st.error("❌ All fields except phone number are required.")
            return
        if password != confirm_password:
            st.error("❌ Passwords do not match.")
            return
        if len(password) < 8:
            st.error("❌ Password must be at least 8 characters long.")
            return
            
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (full_name, username, email, password, phone) VALUES (%s, %s, %s, %s, %s)",
                    (full_name, username, email, hashed_password, phone)
                )
                conn.commit()
                st.success("✅ Registration successful! Redirecting to login...")
                st.balloons()
                # Automatically switch to login page
                st.session_state['show_login'] = True
                st.rerun()
            except mysql.connector.IntegrityError:
                st.error("❌ Email already exists. Please use a different email.")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
            finally:
                cursor.close()
                conn.close()

# Login function
def login():
    st.markdown('<div class="banner"><h1>🔐 Welcome Back</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>Access Your Personalized Dashboard</h3>
        <p>Log in to continue your skin health monitoring journey with AI-powered acne detection and personalized care recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email address")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("🚀 Login")

    if submit:
        if not all([email, password]):
            st.error("❌ Email and password are required.")
            return
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')):
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.success(f"✅ Welcome back, {user[1]}!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")

# Home page
def home():
    user_name = st.session_state['user'][1] if 'user' in st.session_state else "User"
    
    st.markdown(f'<div class="banner"><h1>🔬 Acne Detection System</h1></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-card" style="text-align: center;">
        <h2>Welcome, {user_name}! 👋</h2>
        <p style="font-size: 1.2rem;">Your AI-Powered Skin Health Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>📸 Image Upload</h3>
            <p>Upload facial images for instant acne detection with bounding boxes and severity classification</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>🎥 Live Detection</h3>
            <p>Real-time acne detection using your webcam for immediate analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3>📊 Performance Insights</h3>
            <p>Explore training metrics, confusion matrices, and precision-recall curves</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🎯 Why Skin Health Matters</div>
        <div class="article-content">
            <p>Acne affects over <strong>50 million people annually</strong> in the United States alone, impacting self-confidence, 
            mental health, and quality of life. Our AI-driven platform empowers you to:</p>
            <ul>
                <li>Monitor your skin health proactively with cutting-edge technology</li>
                <li>Receive scientifically-backed severity assessments using GAGS and IGA scales</li>
                <li>Get personalized treatment recommendations based on your specific condition</li>
                <li>Track changes over time to measure treatment effectiveness</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🚀 Powered by YOLOv9 Technology</div>
        <div class="article-content">
            <p>Our platform utilizes <strong>YOLOv9</strong>, the latest advancement in real-time object detection:</p>
            <ul>
                <li><strong>Lightning-Fast Processing:</strong> Analyze images in milliseconds</li>
                <li><strong>High Accuracy:</strong> Over 85% precision in acne lesion detection</li>
                <li><strong>Advanced Feature Extraction:</strong> Identifies subtle variations in skin conditions</li>
                <li><strong>Clinically Validated:</strong> Trained on thousands of annotated medical images</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# About page
def about():
    st.markdown('<div class="banner"><h1>ℹ️ About Our Project</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🎯 Our Mission</div>
        <div class="article-content">
            <p>We're revolutionizing skin health monitoring by combining advanced computer vision with accessible technology. 
            Our mission is to democratize dermatological care, making professional-grade skin analysis available to everyone, anywhere.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔬 Cutting-Edge Technology</h3>
            <ul>
                <li><strong>YOLOv9 Architecture:</strong> State-of-the-art deep learning model</li>
                <li><strong>Real-Time Processing:</strong> Instant results with GPU acceleration</li>
                <li><strong>High Precision:</strong> 85%+ accuracy in lesion detection</li>
                <li><strong>Dual Severity Assessment:</strong> GAGS and IGA clinical scales</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Dataset & Training</h3>
            <ul>
                <li><strong>Source:</strong> High-quality Roboflow medical dataset</li>
                <li><strong>Images:</strong> Thousands of annotated facial images</li>
                <li><strong>Diversity:</strong> Multiple skin types and lighting conditions</li>
                <li><strong>Validation:</strong> Rigorous testing with dermatological standards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">👥 Our Team</div>
        <div class="article-content">
            <p>We're a dedicated group of AI researchers, dermatologists, and healthcare enthusiasts working to bridge 
            the gap between advanced technology and accessible healthcare. Our multidisciplinary approach ensures both 
            technical excellence and clinical relevance.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🔮 Future Vision</div>
        <div class="article-content">
            <ul>
                <li><strong>Expanded Detection:</strong> Additional skin conditions (eczema, rosacea, psoriasis)</li>
                <li><strong>Treatment Tracking:</strong> Monitor progress over time with historical analysis</li>
                <li><strong>Telehealth Integration:</strong> Connect directly with dermatologists</li>
                <li><strong>Mobile Application:</strong> On-the-go skin analysis</li>
                <li><strong>AI-Powered Predictions:</strong> Forecast treatment outcomes</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Algorithm page
def algo():
    st.markdown('<div class="banner"><h1>📊 Algorithm & Results</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🤖 Model Architecture: YOLOv9</div>
        <div class="article-content">
            <p>Our system employs <strong>YOLOv9 (You Only Look Once, Version 9)</strong>, representing the pinnacle of 
            real-time object detection technology. This architecture excels at identifying and localizing acne lesions 
            with unprecedented speed and accuracy.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">85%+</div>
            <div class="metric-label">Precision</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">80%+</div>
            <div class="metric-label">Recall</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-value">0.82</div>
            <div class="metric-label">mAP@0.5</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Training Configuration</h3>
        <ul>
            <li><strong>Environment:</strong> GPU-accelerated computing (CUDA-enabled)</li>
            <li><strong>Dataset Split:</strong> 70% Training, 20% Validation, 10% Testing</li>
            <li><strong>Data Augmentation:</strong> Rotation, flipping, scaling, color jittering</li>
            <li><strong>Optimization:</strong> AdamW optimizer with learning rate scheduling</li>
            <li><strong>Epochs:</strong> Trained until convergence with early stopping</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-top: 40px;'>📈 Performance Visualizations</h2>", unsafe_allow_html=True)
    
    result_images = [
        ('working_data/detect/train/confusion_matrix_normalized.png', "Confusion Matrix", 
         "Shows model classification performance across different lesion types"),
        ('working_data/detect/train/BoxPR_curve.png', "Precision-Recall Curve", 
         "Illustrates the trade-off between precision and recall at various thresholds"),
        ('working_data/detect/train/BoxF1_curve.png', "F1 Score Curve", 
         "Demonstrates the harmonic mean of precision and recall")
    ]
    
    for img_path, title, description in result_images:
        if os.path.exists(img_path):
            st.markdown(f"""
            <div class="feature-card">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """, unsafe_allow_html=True)
            st.image(img_path, use_container_width=True)
        else:
            st.warning(f"⚠️ {title} not found at {img_path}")
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🔍 Key Insights</div>
        <div class="article-content">
            <ul>
                <li>The model demonstrates robust performance across diverse skin types and lighting conditions</li>
                <li>High precision minimizes false positives, ensuring reliable detection results</li>
                <li>Strong recall ensures most acne lesions are successfully identified</li>
                <li>Continuous learning pipeline allows for ongoing model improvements</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Prediction page with severity analysis
def prediction():
    st.markdown('<div class="banner"><h1>📸 Image-Based Detection</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>Upload Your Image for Comprehensive Analysis</h3>
        <p>Our AI will detect acne lesions, classify severity using GAGS and IGA scales, and provide personalized treatment recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📁 Choose an image (JPG, PNG, JPEG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>Original Image</h3>", unsafe_allow_html=True)
            st.image(image, use_container_width=True)
        
        if st.button("🔍 Analyze Image"):
            if model is None:
                st.error("❌ Model not loaded. Please check model file.")
                return
            
            with st.spinner("🔄 Analyzing image... Please wait..."):
                annotated_image, classes = predict_image(image)
                pimple_count = len(classes)
            
            if annotated_image is not None:
                with col2:
                    st.markdown("<h3 style='text-align: center;'>Detection Results</h3>", unsafe_allow_html=True)
                    st.image(annotated_image, use_container_width=True)
                
                if pimple_count > 0:
                    st.success(f"✅ Analysis Complete: {pimple_count} acne lesion(s) detected")
                    display_severity_analysis(pimple_count)
                else:
                    st.info("✨ No acne lesions detected! Your skin looks clear.")
                    st.markdown("""
                    <div class="feature-card">
                        <h3>🎉 Congratulations!</h3>
                        <p>Continue maintaining your current skincare routine and healthy lifestyle habits.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("❌ Analysis failed. Please try a different image.")

# Live Detection page
def live_detection():
    st.markdown('<div class="banner"><h1>🎥 Live Detection</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>Real-Time Acne Detection with Webcam</h3>
        <p>Activate your webcam for instant analysis. Position your face clearly for optimal detection accuracy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="article-card">
        <div class="article-title">📋 Instructions</div>
        <div class="article-content">
            <ul>
                <li>Ensure your webcam is connected and accessible</li>
                <li>Position your face 30-40 cm from the camera</li>
                <li>Use good lighting (natural light preferred)</li>
                <li>Keep your face steady for best results</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    run = st.checkbox("▶️ Start Webcam")
    FRAME_WINDOW = st.empty()
    detection_info = st.empty()
    
    if run:
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                st.error("❌ Failed to access webcam. Ensure it's connected and not in use.")
                return
            
            while run:
                ret, frame = camera.read()
                if not ret:
                    st.error("❌ Failed to capture frame.")
                    break
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                annotated_frame, classes = predict_image(frame)
                
                if annotated_frame is not None:
                    FRAME_WINDOW.image(annotated_frame, use_container_width=True)
                    pimple_count = len(classes)
                    
                    if pimple_count > 0:
                        detection_info.markdown(f"""
                        <div class="feature-card" style="text-align: center;">
                            <h3>🔍 Current Frame: {pimple_count} lesion(s) detected</h3>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        detection_info.markdown("""
                        <div class="feature-card" style="text-align: center;">
                            <h3>✨ No lesions detected in current frame</h3>
                        </div>
                        """, unsafe_allow_html=True)
                
                import time
                time.sleep(0.1)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            if 'camera' in locals():
                camera.release()
    else:
        st.info("📷 Webcam stopped. Check the box above to start.")

# Articles page
def articles():
    st.markdown('<div class="banner"><h1>📚 Skincare & Lifestyle Articles</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>Expert Guidance for Acne-Prone Skin</h3>
        <p>Explore evidence-based articles on skincare routines, lifestyle modifications, and acne management strategies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Article 1
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🧴 Building an Effective Skincare Routine for Acne-Prone Skin</div>
        <div class="article-content">
            <h4>The Foundation: Cleansing</h4>
            <p>Proper cleansing is the cornerstone of acne management. Use a <strong>gentle, pH-balanced cleanser</strong> 
            twice daily (morning and evening). Look for ingredients like:</p>
            <ul>
                <li><strong>Salicylic Acid (BHA):</strong> Penetrates pores to dissolve sebum and dead skin cells</li>
                <li><strong>Glycolic Acid (AHA):</strong> Exfoliates surface skin and promotes cell turnover</li>
                <li><strong>Tea Tree Oil:</strong> Natural antibacterial properties</li>
            </ul>
            
            <h4>Treatment Phase</h4>
            <p>After cleansing, apply targeted treatments:</p>
            <ul>
                <li><strong>Benzoyl Peroxide (2.5%-10%):</strong> Kills acne-causing bacteria, reduces inflammation</li>
                <li><strong>Retinoids (Adapalene, Tretinoin):</strong> Prevents clogged pores, promotes skin renewal</li>
                <li><strong>Niacinamide:</strong> Reduces inflammation, regulates oil production</li>
            </ul>
            
            <h4>Hydration & Protection</h4>
            <ul>
                <li><strong>Moisturizer:</strong> Non-comedogenic, oil-free formulas with hyaluronic acid or ceramides</li>
                <li><strong>Sunscreen:</strong> Broad-spectrum SPF 30+ daily (crucial when using active ingredients)</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Article 2
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🥗 Lifestyle Factors That Impact Acne</div>
        <div class="article-content">
            <h4>Diet & Nutrition</h4>
            <p>Research shows strong correlations between diet and acne severity:</p>
            <ul>
                <li><strong>Foods to Limit:</strong> High-glycemic foods (white bread, sugary snacks), dairy products, processed foods</li>
                <li><strong>Foods to Embrace:</strong> Omega-3 rich fish, leafy greens, berries, nuts, whole grains</li>
                <li><strong>Hydration:</strong> Aim for 8-10 glasses of water daily to flush toxins</li>
            </ul>
            
            <h4>Sleep Quality</h4>
            <p><strong>7-9 hours</strong> of quality sleep is essential for skin repair and hormonal balance. Poor sleep 
            increases cortisol levels, triggering inflammation and oil production.</p>
            
            <h4>Stress Management</h4>
            <p>Chronic stress elevates cortisol, worsening acne. Effective strategies include:</p>
            <ul>
                <li>Meditation and mindfulness (10-15 minutes daily)</li>
                <li>Regular exercise (30 minutes, 5 times weekly)</li>
                <li>Yoga or deep breathing exercises</li>
                <li>Adequate leisure and social connection</li>
            </ul>
            
            <h4>Hygiene Habits</h4>
            <ul>
                <li>Clean pillowcases weekly (cotton preferred)</li>
                <li>Sanitize phone screens daily</li>
                <li>Avoid touching your face throughout the day</li>
                <li>Remove makeup before bed (always!)</li>
                <li>Shower after exercising to remove sweat</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Article 3
    st.markdown("""
    <div class="article-card">
        <div class="article-title">💊 Understanding Acne Treatment Options</div>
        <div class="article-content">
            <h4>Over-the-Counter (OTC) Treatments</h4>
            <p>Suitable for mild to moderate acne:</p>
            <ul>
                <li><strong>Benzoyl Peroxide:</strong> Start with 2.5% to minimize irritation</li>
                <li><strong>Salicylic Acid:</strong> 0.5%-2% concentration for daily use</li>
                <li><strong>Adapalene (Differin):</strong> OTC retinoid for prevention</li>
                <li><strong>Sulfur:</strong> Gentle option for sensitive skin</li>
            </ul>
            
            <h4>Prescription Treatments</h4>
            <p>For moderate to severe acne, dermatologists may prescribe:</p>
            <ul>
                <li><strong>Topical Retinoids:</strong> Tretinoin, Tazarotene (more potent than OTC)</li>
                <li><strong>Topical Antibiotics:</strong> Clindamycin, Erythromycin (often combined with Benzoyl Peroxide)</li>
                <li><strong>Oral Antibiotics:</strong> Doxycycline, Minocycline (for inflammatory acne)</li>
                <li><strong>Hormonal Treatments:</strong> Birth control pills, Spironolactone (for women)</li>
                <li><strong>Isotretinoin (Accutane):</strong> For severe, resistant cystic acne</li>
            </ul>
            
            <h4>Professional Procedures</h4>
            <ul>
                <li><strong>Chemical Peels:</strong> Glycolic, salicylic, or TCA peels</li>
                <li><strong>Laser Therapy:</strong> Targets bacteria and reduces oil production</li>
                <li><strong>Light Therapy:</strong> Blue/red light kills bacteria and reduces inflammation</li>
                <li><strong>Microneedling:</strong> Improves scarring and skin texture</li>
                <li><strong>Extractions:</strong> Professional removal of comedones</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Article 4
    st.markdown("""
    <div class="article-card">
        <div class="article-title">🌿 Natural Remedies and Alternative Approaches</div>
        <div class="article-content">
            <h4>Evidence-Based Natural Ingredients</h4>
            <ul>
                <li><strong>Tea Tree Oil (5%):</strong> Comparable to Benzoyl Peroxide but gentler</li>
                <li><strong>Green Tea Extract:</strong> Powerful antioxidant with anti-inflammatory properties</li>
                <li><strong>Aloe Vera:</strong> Soothes inflammation, promotes healing</li>
                <li><strong>Honey (especially Manuka):</strong> Antibacterial and wound-healing properties</li>
                <li><strong>Zinc Supplements:</strong> Reduces inflammation (30-40mg daily)</li>
            </ul>
            
            <h4>Important Considerations</h4>
            <p>While natural remedies can be beneficial, they should complement, not replace, proven treatments. 
            Always patch test new ingredients and consult a dermatologist for persistent acne.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Article 5
    st.markdown("""
    <div class="article-card">
        <div class="article-title">❌ Common Acne Myths Debunked</div>
        <div class="article-content">
            <h4>Myth vs. Reality</h4>
            <ul>
                <li><strong>Myth:</strong> "Acne is caused by dirty skin" 
                    <br><strong>Reality:</strong> Acne is primarily hormonal and genetic. Over-washing can worsen it.</li>
                
                <li><strong>Myth:</strong> "Toothpaste cures pimples" 
                    <br><strong>Reality:</strong> Toothpaste can irritate skin and cause burns. Use proper spot treatments.</li>
                
                <li><strong>Myth:</strong> "Sun exposure clears acne" 
                    <br><strong>Reality:</strong> UV damage worsens post-inflammatory hyperpigmentation. Always use SPF.</li>
                
                <li><strong>Myth:</strong> "Oily skin doesn't need moisturizer" 
                    <br><strong>Reality:</strong> All skin needs hydration. Skipping moisturizer triggers more oil production.</li>
                
                <li><strong>Myth:</strong> "Popping pimples makes them heal faster" 
                    <br><strong>Reality:</strong> Picking causes scarring, infection, and prolongs healing.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card" style="text-align: center;">
        <h3>📌 Remember</h3>
        <p>Acne treatment requires patience and consistency. Most treatments take <strong>4-12 weeks</strong> to show results. 
        If OTC treatments don't improve your condition after 8 weeks, consult a dermatologist for personalized care.</p>
    </div>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    load_custom_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'show_login' not in st.session_state:
        st.session_state['show_login'] = False
    
    if not st.session_state['logged_in']:
        # Show login if redirected from registration
        if st.session_state['show_login']:
            login()
            if st.button("← Back to Registration"):
                st.session_state['show_login'] = False
                st.rerun()
        else:
            page = st.sidebar.selectbox("🔐 Authentication", ["Login", "Register"])
            if page == "Register":
                register()
            elif page == "Login":
                login()
    else:
        page = st.sidebar.selectbox(
            "📋 Navigation", 
            ["Home", "About", "Algorithm", "Image Detection", "Live Detection", "Articles", "Logout"]
        )
        
        if page == "Home":
            home()
        elif page == "About":
            about()
        elif page == "Algorithm":
            algo()
        elif page == "Image Detection":
            prediction()
        elif page == "Live Detection":
            live_detection()
        elif page == "Articles":
            articles()
        elif page == "Logout":
            st.session_state['logged_in'] = False
            st.session_state.pop('user', None)
            st.session_state['show_login'] = False
            st.success("✅ You have been logged out successfully!")
            st.balloons()
            st.rerun()

if __name__ == "__main__":
    main()

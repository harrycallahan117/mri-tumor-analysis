from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# Load the trained model
model_path = 'E:/private_projects/mri-tumor-analysis/backend/new_model_saved'
model = tf.saved_model.load(model_path)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the root URL
@app.route('/')
def home():
    return "MRI Tumor Classification API is running. Use /predict to send images for classification."

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file.save(file_path)

        try:
            # Prepare the image for prediction
            img = image.load_img(file_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            # Create a TensorFlow session and run prediction
            infer = model.signatures['serving_default']
            predictions = infer(tf.constant(img_array, dtype=tf.float32))
            
            # Ensure you check the keys available
            print("Available output keys:", list(predictions.keys()))  # Debugging line
            
            # Use the appropriate key for your output
            output_key = list(predictions.keys())[0]  # Replace with the correct output key if needed
            prediction = predictions[output_key].numpy()
            class_index = np.argmax(prediction, axis=1)[0]
            class_labels = ['Glioma Tumor', 'Meningioma Tumor', 'Normal', 'Pituitary Tumor']
            tumor_type = class_labels[class_index]

            # Generate PDF
            pdf_bytes = generate_pdf(tumor_type)

            # Return the PDF
            return send_file(BytesIO(pdf_bytes), as_attachment=True, download_name='report.pdf')

        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file format'}), 400

def generate_pdf(tumor_type):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Tumor Classification Report")
    c.drawString(100, height - 150, f"Type of Tumor: {tumor_type}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

if __name__ == '__main__':
    app.run(port=5000)
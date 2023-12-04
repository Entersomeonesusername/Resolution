import os
import cv2
import torch
import numpy as np
from flask import Flask, render_template, request, send_file,after_this_request
import RRDBNet_arch as arch
import base64
from io import BytesIO

app = Flask(__name__)

model_path = 'models/RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth

device = torch.device('cpu')  # Use CPU for processing a single image
model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
model.eval()
model = model.to(device)


@app.route('/')
def index():
    return render_template('index.html', processed_image=None)

@app.route('/process_image', methods=['POST'])
def process_image():
    if request.method == 'POST':
        # Get the uploaded image file
        image_file = request.files['image']
        
        # Save the image file to a temporary location
        image_path = 'temp_image.jpg'
        image_file.save(image_path)

        # Read the input image
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = img * 1.0 / 255
        img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
        img_LR = img.unsqueeze(0)
        img_LR = img_LR.to(device)

        with torch.no_grad():
            output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round()

        # Convert the processed image to a base64-encoded string
        _, img_encoded = cv2.imencode('.jpg', output)
        processed_image = base64.b64encode(img_encoded).decode('utf-8')

        # Remove the temporary image file
        os.remove(image_path)

        return render_template('index.html', processed_image=processed_image)


@app.route('/download_image', methods=['POST'])
def download_image():
    try:
        # Decode the base64-encoded image
        processed_image_data = request.form.get('processed_image', type=str)
        img_decoded = base64.b64decode(processed_image_data)

        # Create an in-memory file-like object
        output = BytesIO(img_decoded)

        # # Save the file temporarily
        # temp_dir = 'temp'
        # os.makedirs(temp_dir, exist_ok=True)
        # temp_filename = 'processed_image.jpg'
        # temp_filepath = os.path.join(temp_dir, temp_filename)

        # with open(temp_filepath, 'wb') as f:
        #     f.write(output.getvalue())

        # Send the file for download
        response = send_file(output, as_attachment=True, download_name='processed_image.jpg')

        # # Clean up: remove the temporary file after the response is sent
        # @after_this_request
        # def remove_temp_file(response):
        #     try:
        #         os.remove(temp_filepath)
        #     except Exception as e:
        #         print(f"Error removing temp file: {str(e)}")
        #     return response

        return response

    except Exception as e:
        # Log the error for debugging
        print(f"Error: {str(e)}")
        return str(e)
if __name__ == '__main__':
    app.add_url_rule('/download_image', 'download_image', download_image)
    app.run(debug=True)

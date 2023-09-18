from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests, os
from PIL import Image
import json

############################################################
API_SERVER = 'http://127.0.0.1:4000/predict'
IMAGE_PATH = os.path.join('static', 'image.jpg')
RESULT_IMAGE_PATH = os.path.join('static', 'image_output.jpg')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Get uploaded image
        image = request.files['image']

        # Save the image to a temporary location
        image.save(IMAGE_PATH)

        return redirect(url_for('input_params'))

    return render_template('upload.html')

@app.route('/input', methods=['GET', 'POST'])
def input_params():
    if request.method == 'POST':
        # Get mode choice from form
        mode = request.form.get('mode')

        img = Image.open(IMAGE_PATH)

        # get width and height
        width = img.width
        height = img.height

        # Prepare parameters based on mode choice
        params = {}
        if mode == 'everything':
            params = {'mode': 'everything'}
        if mode == 'box':
            box_input = request.form.get('box_input')
            text = box_input.split(',')
            x0 = float(text[0]) / width
            y0 = float(text[1]) / height
            x1 = min(float(text[2]) / width, 1.0)
            y1 = min(float(text[3]) / height, 1.0)
            params = {
                'mode': 'box',
                'box_prompt': [x0, y0, x1, y1],
            }
        elif mode == 'text':
            text_input = request.form.get('text_input')
            params = {
                'mode': 'text',
                'text_prompt': text_input,
            }
        elif mode == 'points':
            point_input = request.form.get('point_list')
            label_input = request.form.get('label_list')
            if label_input:
                point_list = point_input.split(',')
                label_list = label_input.split(',')
                point_vector = []
                label_vector = []
                for i in range(0, len(label_list)):
                    label_vector.append(int(label_list[i]))
                    x = float(point_list[2*i]) / width
                    y = float(point_list[2*i+1]) / height
                    point_vector.append([x, y])
                params = {
                    'mode': 'points',
                    'point_prompt': point_vector,
                    'point_label': label_vector,
                }
        payload = json.dumps(params)

        # Send POST request to API server
        # Note that it is not possible to send binary data via "data" and files, because they have different formats: 1 is binary, 2 is form data
        api_response = requests.post(API_SERVER, data={"data": payload}, files={'image': open(IMAGE_PATH, 'rb')})

        if api_response.status_code == 200:
            # Save the processed image to a temporary location
            processed_image_path = RESULT_IMAGE_PATH
            with open(processed_image_path, 'wb') as f:
                f.write(api_response.content)
            return redirect(url_for('display_result'))
        else:
            print(api_response.text)

    return render_template('input.html', image_path=IMAGE_PATH)

@app.route('/result')
def display_result():
    return render_template('result.html', processed_image_path=RESULT_IMAGE_PATH)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

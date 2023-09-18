from fastsam import FastSAM, FastSAMPrompt

from flask import Flask, request, jsonify, send_file
from PIL import Image
import json
from input_validator import InputSetting

###########################################
DEVICE = 'cpu'
IMAGE_PATH = './output/out.jpg'


app = Flask(__name__)

# Load the pre-trained model
model = FastSAM('./weights/FastSAM-s.pt')

@app.route('/ping', methods=['GET'])
def ping():
    try:
        return jsonify({'message':'pong'})
    except Exception as e:
        return str(e), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parser request
        data = json.loads(request.form['data'])
        file = request.files['image']

        # validate the data input and parse input
        setting = InputSetting(
            mode = data.get('mode'),
            box_prompt = data.get('box_prompt', []),
            text_prompt = data.get('text_prompt', ''),
            point_prompt=data.get('point_prompt', []),
            point_label = data.get('point_label', []),
        )
        mode = setting.mode

        # Read the image via file.stream
        input = Image.open(file.stream)
        input = input.convert("RGB")
        w, h = input.size
        everything_results = model(input, device=DEVICE, retina_masks=True, imgsz=1024, conf=0.4, iou=0.9, )
        prompt_process = FastSAMPrompt(input, everything_results, device=DEVICE)

        # everything, box, text, points
        if mode == 'everything':
            ann = prompt_process.everything_prompt()
        elif mode == 'box':
            box_prompt = data['box_prompt']
            x_0 = int(box_prompt[0] * w)
            y_0 = int(box_prompt[1] * h)
            x_1 = int(box_prompt[2] * w)
            y_1 = int(box_prompt[3] * h)
            bbox_integer = [x_0, y_0, x_1, y_1]
            ann = prompt_process.box_prompt(bboxes=[bbox_integer])
        elif mode == 'text':
            text_prompt = data['text_prompt']
            ann = prompt_process.text_prompt(text=text_prompt)
        elif mode == 'points':
            point_prompt = data['point_prompt']
            point_label = data['point_label']
            point_vector = []
            for i in range(len(point_prompt)):
                pos = point_prompt[i]
                x_0 = int(pos[0] * w)
                y_0 = int(pos[1] * h)
                point_vector.append([x_0, y_0])
            ann = prompt_process.point_prompt(points=point_vector, pointlabel=point_label)

        prompt_process.plot(annotations=ann, output_path=IMAGE_PATH, )

        return send_file(IMAGE_PATH, download_name='')

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

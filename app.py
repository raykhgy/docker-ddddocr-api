from flask import Flask, request, jsonify
import ddddocr
from io import BytesIO

app = Flask(__name__)
ocr = ddddocr.DdddOcr(show_ad=False, beta=True)

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        img_bytes = file.read()
        
        result = ocr.classification(img_bytes)
        
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
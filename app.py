from flask import Flask, request, jsonify
import ddddocr
import base64

app = Flask(__name__)
ocr = ddddocr.DdddOcr(show_ad=False, beta=True)

def base64_to_image(base64_string):
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        img_bytes = base64.b64decode(base64_string)
        return img_bytes
    except base64.binascii.Error:
        raise ValueError("無效的 Base64 字符串")
    except Exception as e:
        raise ValueError(f"Base64 解碼失敗: {str(e)}")

def apply_ranges(ranges):
    if ranges is None:
        return
    if isinstance(ranges, str) and ranges.lstrip('-').isdigit():
        ranges = int(ranges)
    ocr.set_ranges(ranges)

@app.route('/ocr_image', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        img_bytes = file.read()

        apply_ranges(request.form.get('ranges'))

        result = ocr.classification(img_bytes)
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ocr_image_str', methods=['POST'])
def ocr_image_str():
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        data = request.get_json()
        if 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        img_bytes = base64_to_image(data['image'])

        apply_ranges(data.get('ranges'))

        result = ocr.classification(img_bytes)
        return jsonify({'result': result}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

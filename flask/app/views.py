
try:
    from app import app
except ImportError as err:
    # Output expected ImportErrors.
    print("while importing app: ")
    raise ImportError(err)
try:
    
    from flask import request
    import shutil
    import json
    import services.fourier as fourier
    import services.convolution as convolution
    import services.noise as convolution
    import services.interpolation as interpolation
    from services.helper import get_response_image, get_input_output_path
except ImportError as err:
    # Output expected ImportErrors.
    print(err)
    raise ImportError(err)


@app.route('/', methods=['GET'])
def hello_route():
    return "<div>Hello</div>"

@app.route('/api/convolution', methods=['POST'])
def convolution_route():
    input_image = request.files['input_image']
    kernel = request.form['kernel']
    kernel_name = request.form['kernel_name']
    kernel = json.loads(kernel)
    for i in range(0, 9):
        kernel[i] = float(kernel[i])
    try:
        input_file_path, out_file_path, uploads_dir = get_input_output_path(
            input_image)

        convolution.main(input_file_path, out_file_path, kernel, kernel_name)
    except Exception as e:
        # traceback.print_exc()
        error = e.__str__()
        return {
            "status": "bad",
            "kernel": kernel,
            "error": error,
        }
    output = get_response_image(out_file_path)
    shutil.rmtree(uploads_dir)
    return {
        "status": "good",
        "output_image": output,
        "kernel": kernel,
    }


@app.route('/api/interpolation', methods=['POST'])
def interpolation_route():
    input_image = request.files['input_image']
    width = int(request.form['width'])
    height = int(request.form['height'])
    try:
        input_file_path, out_file_path, uploads_dir = get_input_output_path(
            input_image)

        interpolation.main(input_file_path, out_file_path, width, height)
    except Exception as e:
        # traceback.print_exc()
        error = e.__str__()
        return {
            "status": "bad",
            "error": error,
        }
    output = get_response_image(out_file_path)
    shutil.rmtree(uploads_dir)
    return {
        "status": "good",
        "output_image": output,
    }


@app.route('/api/noise', methods=['POST'])
def noise_route():
    input_image = request.files['input_image']
    noise_type = request.form['noise']
    print(input_image.__sizeof__())
    try:
        input_file_path, out_file_path, uploads_dir = get_input_output_path(
            input_image)
        noise.main(input_file_path, out_file_path, noise_type)
    except Exception as e:
        # traceback.print_exc()
        error = e.__str__()
        return {
            "status": "bad",
            "error": error,
        }
    output = get_response_image(out_file_path)
    shutil.rmtree(uploads_dir)
    return {
        "status": "good",
        "output_image": output,
    }


@app.route('/api/fourier', methods=['POST'])
def fourier_route():
    # content_type = request.headers.get('Content-Type')
    print(request.files)
    input_image = request.files['input_image']
    try:
        input_file_path, out_file_path, uploads_dir = get_input_output_path(
            input_image)
        fourier.main(input_file_path, out_file_path)
    except Exception as e:
        error = e.__str__()
        return {
            "status": "bad",
            "error": error,
        }
    output = get_response_image(out_file_path)
    shutil.rmtree(uploads_dir)
    return {
        "status": "good",
        "output_image": output,
    }















# # paste camera stream url in quotations ("url") or use 0 to use webcam 
# cam_url = os.getenv('CAMERA_STREAM_URL', '0')


# def process_frame(frame):
#     # do the image processing here
#     return frame


# @app.route('/')
# def home():
#     return render_template('index.html')


# def stream():
#     cap = cv2.VideoCapture(cam_url)
#     while True:
#         cv2.waitKey(1)
#         success, frame = cap.read()
#         frame = process_frame(frame)
#         if success:
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/live_stream/', methods=["GET"])
# def live_stream():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(stream(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

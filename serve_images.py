from PIL import Image
import flask
import json
import os
import random

app = flask.Flask(__name__)

@app.route("/get_random_image", methods=["GET"])
def serve_converted_image():
    image = get_random_image()
    image_byte_array, frame_count = create_bytearray_from_image(image)
    resp = flask.Response(image_byte_array)
    resp.headers["time_to_live"] = "100"
    resp.headers["loop_delay"] = ".5"
    resp.headers["frame_count"] = str(frame_count)
    return resp

def create_bytearray_from_image(image):
    img = Image.open(image)
    frames_count = img.n_frames
    byte_array = []
    for frame_number in range(frames_count):
        img.seek(frame_number)
        rgb_values = img.convert("RGB")
        for x in range(16):
            for y in range(16):
                if x >= img.width or y >= img.height:
                    byte_array.extend([26, 26, 26])
                else:
                    converted = rgb_values.getpixel((x, y))
                    converted = list(converted)
                    converted = [round(i/10) for i in converted]
                    byte_array.extend(list(converted))
    return bytearray(byte_array), frames_count

def get_random_image():
    import logging
    logging.basicConfig(filename='/home/jbg/dev/ledmatrix/matrix.log', level=logging.DEBUG)
    with open("/home/jbg/dev/ledmatrix/previous_index.txt", "r") as f:
        previous_index = int(f.read())
    images = [os.path.join("/home/jbg/dev/ledmatrix/images", i) for i in os.listdir("/home/jbg/dev/ledmatrix/images")]
    #random_int = random.randint(0, len(images) - 1)
    if previous_index >= len(images) - 1:
        previous_index = 0
    else:
        previous_index += 1
    #while random_int == previous_index:
    #    random_int = random.randint(0, len(images) - 1)
    with open("/home/jbg/dev/ledmatrix/previous_index.txt", "w") as f:
        f.write(str(previous_index))
    logging.info(images[previous_index])
    return images[previous_index]

def main():
    app.run(host="0.0.0.0", port=5002)

main()

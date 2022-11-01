import base64
import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import colorgram

app = Flask(__name__)
app.secret_key = os.environ.get('SERVER_KEY')
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/palette", methods=["GET", "POST"])
def palette():
    if request.method == "POST":
        img_to_render = request.files.get('img-path')
        number_of_colors = request.form['number-colors']
        image_b64 = base64.b64encode(img_to_render.read()).decode('utf-8')

        color_list = colorgram.extract(img_to_render, int(number_of_colors))
        rgb_tuples = []
        for i in color_list:
            new_tuple = (i.rgb.r, i.rgb.g, i.rgb.b)
            rgb_tuples.append(new_tuple)

        def rgb_to_hex(rgb):
            return '%02x%02x%02x' % rgb

        hex_codes = []
        for i in rgb_tuples:
            hex_codes.append(rgb_to_hex(i))

        return render_template("palette.html", image_b64=image_b64, colors=hex_codes)
    return render_template("palette.html")


if __name__ == '__main__':
    app.run(debug=True)

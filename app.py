from flask import Flask, request, jsonify, render_template, Response
import huwei_cbs

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/aiApi", methods=["POST"])
def chat():
    prompts = request.form.get("prompts")
    if prompts == None:
        return jsonify({'success': False,'message':'请求内容为空'})
    else:
        message = huwei_cbs.cbsUtil(prompts)
        return jsonify({'success': True,'message':message})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

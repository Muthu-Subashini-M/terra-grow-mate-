from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, 
            template_folder='frontend', 
            static_folder='frontend',
            static_url_path='')

# Enable CORS for fetch requests
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

from backend.rules.soil_evaluator import evaluate_soil_parameters, simulate_image_analysis
from backend.rules.recommendation import generate_crop_recommendations

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        if request.files and "soil_image" in request.files:
            image_file = request.files.get("soil_image")
            if not image_file or image_file.filename == "":
                return jsonify({"status": "error", "message": "No image uploaded"}), 400
            
            img_data = simulate_image_analysis(image_file)
            ph = img_data["estimated_ph"]
            texture = img_data["detected_texture"]
            nitrogen = "medium"
            
            evaluation = evaluate_soil_parameters(ph, texture, nitrogen)
            crops = generate_crop_recommendations(ph, texture, nitrogen)
            
            return jsonify({
                "status": "success",
                "mode": "image",
                "detected_features": img_data,
                "ph": ph,
                "texture": texture,
                "evaluation": evaluation,
                "recommendations": crops
            })
        else:
            data = request.get_json() or {}
            ph = float(data.get("ph", 6.5))
            texture = data.get("texture", "Loam")
            nitrogen = data.get("nitrogen", "medium")

            evaluation = evaluate_soil_parameters(ph, texture, nitrogen)
            crops = generate_crop_recommendations(ph, texture, nitrogen)

            return jsonify({
                "status": "success",
                "mode": "manual",
                "ph": ph,
                "texture": texture,
                "nitrogen": nitrogen,
                "evaluation": evaluation,
                "recommendations": crops
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
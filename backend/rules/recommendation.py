import json
import os

def load_crop_database():
    basedir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(os.path.dirname(basedir))
    json_path = os.path.join(project_root, 'backend', 'data', 'knowledge_base.json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_crop_recommendations(ph, texture, nitrogen):
    crop_database = load_crop_database()
    recommendations = []

    for crop, data in crop_database.items():
        score = 0
        if data["ideal_ph_min"] <= ph <= data["ideal_ph_max"]:
            score += 50
        else:
            score += max(0, 50 - int(abs(ph - ((data["ideal_ph_min"] + data["ideal_ph_max"])/2)) * 25))

        if any(t.lower() == texture.lower() for t in data["preferred_textures"]):
            score += 30
        else:
            score += 10

        recommendations.append({
            "crop": crop,
            "match_score": f"{score}%",
            "description": data["description"]
        })

    recommendations.sort(key=lambda x: int(x["match_score"].replace("%", "")), reverse=True)
    return recommendations[:3]
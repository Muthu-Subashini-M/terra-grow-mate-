def evaluate_soil_parameters(ph, texture, nitrogen):
    issues = []
    score = 100

    if ph < 5.5:
        issues.append("Soil is strongly acidic. Risk of nutrient lockout.")
        score -= 20
    elif ph > 7.8:
        issues.append("Soil is alkaline. Micronutrient availability may be restricted.")
        score -= 20

    if texture.lower() in ["clay", "heavy clay"] and nitrogen == "low":
        issues.append("Clay soil retains moisture well but currently lacks sufficient nitrogen.")
        score -= 10

    return {
        "health_score": max(score, 40),
        "issues": issues if issues else ["Soil parameters look balanced and healthy."]
    }

def simulate_image_analysis(file_storage):
    filename = file_storage.filename.lower()
    
    if "clay" in filename:
        return {"detected_texture": "Clay", "estimated_ph": 6.2, "confidence": "89%"}
    elif "sand" in filename:
        return {"detected_texture": "Sandy Loam", "estimated_ph": 7.2, "confidence": "91%"}
    else:
        return {"detected_texture": "Loam", "estimated_ph": 6.5, "confidence": "85%"}
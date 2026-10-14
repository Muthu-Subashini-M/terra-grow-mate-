DEFAULT_CONFIG = {
    "default_ph": 6.5,
    "default_texture": "Loam",
    "default_nitrogen": "medium",
    "supported_image_types": [".jpg", ".jpeg", ".png"]
}

def get_base_scoring_weights():
    return {
        "ph_weight": 0.4,
        "texture_weight": 0.4,
        "nitrogen_weight": 0.2
    }
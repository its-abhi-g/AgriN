DEMO_SCENARIOS = {
    "Choose an example": None,

    "🌾 Wheat - Yellow leaves": {
        "crop": "Wheat",
        "state": "Uttar Pradesh",
        "district": "",
        "stage": "Vegetative Growth",
        "irrigation": "Available",
        "query": (
            "My wheat leaves are turning yellow during early growth. "
            "What should I check?"
        ),
    },

    "🌾 Rice - Waterlogging": {
        "crop": "Rice",
        "state": "",
        "district": "",
        "stage": "Vegetative Growth",
        "irrigation": "Rain-fed",
        "query": (
            "Heavy rain happened recently and water is remaining "
            "in my field. What should I do?"
        ),
    },

    "🌻 Mustard - Leaf spots": {
        "crop": "Mustard",
        "state": "",
        "district": "",
        "stage": "Unknown",
        "irrigation": "Unknown",
        "query": (
            "Some leaves have spots and the problem seems "
            "to be spreading."
        ),
    },

    "🇮🇳 Hindi - गेहूं की पीली पत्तियां": {
        "crop": "Wheat",
        "state": "Uttar Pradesh",
        "district": "",
        "stage": "Unknown",
        "irrigation": "Unknown",
        "query": (
            "मेरी गेहूं की फसल की पत्तियां पीली हो रही हैं। "
            "मुझे क्या करना चाहिए?"
        ),
    },
}


DEMO_INSIGHTS = [
    {
        "Crop": "Wheat",
        "Problem": "Yellow leaves",
        "Risk": "MODERATE",
    },
    {
        "Crop": "Rice",
        "Problem": "Waterlogging",
        "Risk": "HIGH",
    },
    {
        "Crop": "Mustard",
        "Problem": "Leaf spots",
        "Risk": "MODERATE",
    },
]
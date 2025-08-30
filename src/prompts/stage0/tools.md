{
    "type": "function",
    "function": {
        "name": "extract_features",
        "description": "Extract product features from free-form text about an air conditioner. Return '-' for any field which is not stated.",
        "parameters": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "string",
                    "description": "The standard price, including currency e.g., '45000 INR', '35000 rupees', '25,000', '40000'; Return '-' if it is not mentioned.", 
                },
                "cooling capacity": {
                    "type": "string",
                    "description": "Two possible inputs here 1. AC's cooling capacity as provided e.g., '1.5 tons capacity', '1.5', '1.5 ton', 2. if room size is given, please convert it to tons e.g., '550 square feet' is approximately equal to '1 ton'; Return '-' for any field that is not stated.", 
                },
                "energy efficiency": {
                    "type": "string",
                    "description": "Energy efficiency requirements such as 'standard', 'high efficiency', 'inverter'; Return '-' for any field that is not stated.", 
                },
                "portability": {
                    "type": "string",
                    "description": "Portability factor such as 'portable', 'easy to move', 'fixed', 'for my own house'; Return '-' for any field that is not stated.", 
                },
                "ac type": {
                    "type": "string",
                    "description": "Type like 'split', 'window', 'central', 'portable ac'; Return '-' for any field that is not stated.", 
                },
                "smart features": {
                    "type": "string",
                    "description": "Smart features like 'WiFi', 'voice assistant', 'app remote'; Return '-' for any field that is not stated.", 
                },
            },
            "required": ["price","cooling capacity","energy efficiency", "portability", "ac type", "smart features"],
            "additionalProperties": False,
        },
        "strict": True
    }
}
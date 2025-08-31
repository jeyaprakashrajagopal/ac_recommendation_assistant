{
    "type": "function",
    "function": {
        "name": "extract_features",
        "description": "From user's input, extract only the features that are explicitly mentioned or updated and strictly do not return key with an empty value which is '-'",
        "parameters": {
            "type": "object",
            "properties": {
                "price": {
                    "type": "string",
                    "description": "The standard price, including currency e.g., '45000 INR', '35000 rupees', '25,000', '40000'", 
                },
                "cooling capacity": {
                    "type": "string",
                    "description": "Two possible inputs here 1. AC's cooling capacity as provided e.g., '1.5 tons capacity', '1.5', '1.5 ton', 2. if room size is given, please convert it to tons e.g., '550 square feet' is approximately equal to '1 ton'", 
                },
                "energy efficiency": {
                    "type": "string",
                    "description": "Energy efficiency requirements such as 'standard', 'high efficiency', 'inverter'", 
                },
                "portability": {
                    "type": "string",
                    "description": "Portability factor such as 'portable', 'easy to move', 'fixed', 'for my own house'", 
                },
                "ac type": {
                    "type": "string",
                    "description": "Type like 'split', 'window', 'central', 'portable ac'.", 
                },
                "smart features": {
                    "type": "string",
                    "description": "Smart features like 'WiFi', 'voice assistant', 'app remote'", 
                },
            },
            "additionalProperties": False,
        },
    }
}
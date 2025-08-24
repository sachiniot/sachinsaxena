from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

THINGSBOARD_HOST = "demo.thingsboard.io"
ACCESS_TOKEN = "ZvxA9pfG0GtBiIZZJelX"

@app.route('/esp32-data', methods=['POST'])
def receive_esp32_data():
    try:
        esp32_data = request.get_json()
        print("📥 DATA RECEIVED FROM ESP32")
        print("JSON Data:", json.dumps(esp32_data, indent=2))
        
        processed_data = {
            "original_data": esp32_data,
            "processed_at": datetime.now().isoformat(),
            "status": "success",
            "message": "Processed by Render cloud"
        }
        
        url = f"https://{THINGSBOARD_HOST}/api/v1/{ACCESS_TOKEN}/telemetry"
        response = requests.post(url, json=processed_data)
        
        if response.status_code == 200:
            print("✅ Data sent to ThingsBoard!")
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"}), 500
            
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/')
def home():
    return jsonify({
        "message": "ESP32 to ThingsBoard Bridge",
        "status": "running",
        "endpoint": "POST /esp32-data"
    })

if __name__ == '__main__':
    app.run(debug=True)
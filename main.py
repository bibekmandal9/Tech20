# main.py

# 1. Import proyojoniyo library
import os
import requests  # Gemini API-te HTTP request pathanor jonno
from flask import Flask, request, jsonify
from flask_cors import CORS  # Frontend theke request allow korar jonno
from dotenv import load_dotenv # Environment variable manage korar jonno

# .env file theke environment variable load kora
load_dotenv()

# 2. Flask app initialize kora
app = Flask(__name__)
CORS(app)  # Shob route-er jonno Cross-Origin Resource Sharing enable kora

# 3. Environment variable theke Gemini API Key neowa
# Kokhonoi apnar API key code-er modhye direct likhben na
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 4. Ekti main API endpoint toiri kora
# Frontend ei '/api/generate' endpoint-e request pathabe
@app.route('/api/generate', methods=['POST'])
def generate():
    # Server-e API key configure kora ache kina check kora
    if not GEMINI_API_KEY:
        # Internal Server Error response pathano
        return jsonify({"error": "API key is not configured on the server."}), 500

    try:
        # Frontend theke pathano JSON payload-ti neowa
        user_payload = request.get_json()

        if not user_payload or "contents" not in user_payload:
            # Bad Request response pathano jodi payload thik na thake
            return jsonify({"error": "Invalid payload from frontend. 'contents' are missing."}), 400

        # Gemini API-er jonno URL toiri kora
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

        # Gemini API-te request pathano
        # 'requests' library diye amra external API call korchi
        response = requests.post(api_url, json=user_payload)
        
        # Gemini API theke jodi kono error ashe, shetake handle kora
        response.raise_for_status()

        # Gemini API theke asha response-tike frontend-e pathiye dewa
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        # Gemini API theke asha error-ke log kora ebong frontend-e pathano
        print(f"HTTP error occurred: {http_err}")
        # API theke asha error details shoho response pathano
        return jsonify(http_err.response.json()), http_err.response.status_code
    except Exception as e:
        # Onnanno shob error handle kora
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred on the server."}), 500

# Server cholche kina sheta check korar jonno ekta simple root endpoint
@app.route('/')
def index():
    return "AI Tutor Python Backend is running!"

# 5. Server-ti shuru kora (jodi file-ti direct run kora hoy)
if __name__ == '__main__':
    # Render-er moto platform port-tike dynamically set kore dey
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)

"""
=========================================
PYTHON BACKEND-TI KIVABE CHALABEN
=========================================
* 1. PYTHON INSTALL KORUN:
  Apnar computer-e Python (version 3.7 ba tar opore) install kora nishchit korun.

* 2. PROJECT FOLDER TOIRI KORUN:
  Ekti notun folder toiri korun (e.g., "ai-tutor-python-backend").
  Ei 'main.py' file-ti shekhane rakHun.

* 3. VIRTUAL ENVIRONMENT TOIRI O ACTIVATE KORUN (RECOMMENDED):
  Terminal-e ei command gulo chalun:
  > python -m venv venv
  > source venv/bin/activate  (macOS/Linux-e)
  > venv\\Scripts\\activate    (Windows-e)

* 4. REQUIREMENTS.TXT FILE TOIRI KORUN:
  Project folder-e `requirements.txt` name ekta file toiri korun ebong tar modhye niche dewa package gulo likhun:
  Flask
  requests
  python-dotenv
  Flask-Cors
  gunicorn

* 5. PACKAGE GULO INSTALL KORUN:
  Terminal-e ei command-ti chalun:
  > pip install -r requirements.txt

* 6. .ENV FILE TOIRI KORUN:
  Project folder-e `.env` name ekta file toiri korun ebong tar modhye apnar API key din:
  GEMINI_API_KEY=AIzaSy...........YOUR_REAL_API_KEY

* 7. SERVER-TI LOCALLY CHALUN:
  Terminal-e ei command diye server shuru korun:
  > python main.py
  Apni "Running on http://..." erokom ekta message dekhte paben.

* 8. RENDER-E DEPLOY KORUN:
  - Apnar code (main.py, requirements.txt) ekta GitHub repository-te push korun. `.env` file-ti kokhonoi push korben na.
  - Render.com-e notun "Web Service" toiri korun.
  - GitHub repository connect korun.
  - Render nije thekei bujhe jabe je eta ekta Python app.
  - "Start Command"-er jaygay likhun: `gunicorn main:app`
  - "Environment Variables" section-e giye notun variable jog korun:
    Key: GEMINI_API_KEY
    Value: AIzaSy...........YOUR_REAL_API_KEY
  - "Create Web Service" click korun. Render apnar backend build ebong deploy kore debe.
"""

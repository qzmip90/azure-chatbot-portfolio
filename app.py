from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, logging, uuid, json
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI

# Use absolute path for frontend
frontend_path = os.path.join(os.getcwd(), "frontend")
print(f"📂 Serving frontend from: {frontend_path}")
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app)
load_dotenv()
logging.basicConfig(level=logging.INFO)

# OpenAI config
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-07-01-preview",
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)
deployment_name = os.getenv("DEPLOYMENT_NAME")

# Azure Blob config
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={os.getenv('AZURE_STORAGE_ACCOUNT_NAME')};AccountKey={os.getenv('AZURE_STORAGE_ACCOUNT_KEY')};EndpointSuffix=core.windows.net"
)
container_client = blob_service_client.get_container_client(os.getenv("AZURE_STORAGE_CONTAINER_NAME"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages")

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        logging.error(f"/chat error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    feedback_data = {
        "message": data.get("message"),
        "response": data.get("response"),
        "rating": data.get("rating")
    }

    try:
        blob_name = f"{uuid.uuid4()}.json"
        container_client.upload_blob(name=blob_name, data=json.dumps(feedback_data), overwrite=False)
        return jsonify({"status": "Feedback stored successfully"})
    except Exception as e:
        return jsonify({"error": "Failed to store feedback"}), 500

# Serve index.html
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Serve other static assets
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    print("🚀 Flask app is starting...")
    app.run(debug=True, host="0.0.0.0", port=80)

from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.common.transports.async_ import AsyncTransport
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, uuid, json
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from openai import AzureOpenAI

# Load environment variables
load_dotenv(override=True)

# === Flask Setup ===
frontend_path = os.path.join(os.getcwd(), "frontend")
print(f"📂 Serving frontend from: {frontend_path}")

app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app)

# === Logging Setup ===
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if not connection_string:
    raise ValueError("❌ Missing APPLICATIONINSIGHTS_CONNECTION_STRING in .env")

logger = logging.getLogger(__name__)
logger.addHandler(
    AzureLogHandler(
        connection_string=connection_string,
        transport=AsyncTransport
    )
)
logging.basicConfig(level=logging.INFO)

logger.info("✅ Logger initialized and test log fired🔥.")

# === Azure OpenAI Setup ===
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-07-01-preview",
    azure_endpoint=os.getenv("OPENAI_API_BASE")
)
deployment_name = os.getenv("DEPLOYMENT_NAME")

# === Azure Blob Setup ===
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={os.getenv('AZURE_STORAGE_ACCOUNT_NAME')};AccountKey={os.getenv('AZURE_STORAGE_ACCOUNT_KEY')};EndpointSuffix=core.windows.net"
)
container_client = blob_service_client.get_container_client(
    os.getenv("AZURE_STORAGE_CONTAINER_NAME")
)

# === Routes ===
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages")
    message = messages[-1]["content"] if messages else ""

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages
        )
        reply = response.choices[0].message.content

        # Log user message & reply
        logger.info("User input: %s", message)
        logger.info("Bot response: %s", reply)
        logger.info("🔥 Log test entry!")

        return jsonify({"response": reply})
    except Exception as e:
        logger.error(f"/chat error: {str(e)}")
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
        logger.info("Feedback stored: %s", json.dumps(feedback_data))
        return jsonify({"status": "Feedback stored successfully"})
    except Exception as e:
        logger.error(f"/feedback error: {str(e)}")
        return jsonify({"error": "Failed to store feedback"}), 500

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

print("👀 Testing logs at top level")
logger.info("📢 Global log at module level")

# === Run App ===
if __name__ == "__main__":
    print("🚀 Flask app is starting...")
    app.run(host="0.0.0.0", port=80)

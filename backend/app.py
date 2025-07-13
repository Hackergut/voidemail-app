from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "VoidEmail Backend is Live!"

@app.route("/test-smtp", methods=["POST"])
def test_smtp():
    data = request.json
    try:
        server = smtplib.SMTP(data["host"], int(data["port"]), timeout=5)
        server.starttls()
        server.login(data["user"], data["pass"])
        server.quit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/send", methods=["POST"])
def send_email():
    data = request.json
    try:
        msg = MIMEText(data["html"], "html")
        msg["Subject"] = data["subject"]
        msg["From"] = data["from_addr"]
        msg["To"] = data["to"]

        server = smtplib.SMTP(data["host"], int(data["port"]))
        server.starttls()
        server.login(data["user"], data["pass"])
        server.sendmail(data["from_addr"], [data["to"]], msg.as_string())
        server.quit()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

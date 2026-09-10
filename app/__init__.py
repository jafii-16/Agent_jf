import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from app.gmail import(
    is_email_command,
    extract_email,
    create_gmail_url,
    generate_email_with_gemini
)


from app.youtube import youtube_bp


def create_app():

    app = Flask(__name__)
    CORS(app)

#YOUTUBE
app.register_blueprint(
    youtube_bp,
    url_prefix="/youtube"
)

#HOME 
@app.route("/")
def home():
    return render_template("index.html")

#HTML
@app.route("/html")
def html():
    return render_template("index.html")


#HEALTH
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Nova AI Agent"
        )

#Gmail  AI Agent
@app.route("/agent",methods=["POST"])
def agent():
    try:
        data = request.get_json(silent=True) or {}
        command = data.get("command","").strip()

        if not command:
            return jsonify({
                "success": False,
                "message": "Command is requires"
            }),400

        if not is_email_command(command):
            return jsonify({
                "success": False,
                "messege": "Please give a Gmail command."
            }),400


         recipitant = extract_email(command)

        email = generate_email_with_gemini(command)

        return jsonify({
            "success": True,
            "type": "email",
            "email_generated": True,
            "recipitant": recipitant,
            "subject": email["subject"],
            "body": email["body"],
            "gmail_url":create_gmail_url(
                eamil["subject"],
                emial["body"],
                recipitant
            )
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "messege": str(e)
        })500

return app

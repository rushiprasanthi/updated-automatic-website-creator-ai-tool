import os
from flask import Flask, request, redirect, abort
import smtplib
from email.message import EmailMessage
from html import escape

# Environment variables (required)
# OWNER_EMAIL: where applications are sent (set to the same email you entered when running blog.py)
# SMTP_USER: SMTP username (e.g. same Gmail address)
# SMTP_PASS: SMTP app password (for Gmail, use App Password, not account password)
OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")

if not OWNER_EMAIL or not SMTP_USER or not SMTP_PASS:
    raise RuntimeError("Please set OWNER_EMAIL, SMTP_USER and SMTP_PASS environment variables before running server.py")

# Serve static files from project root (so Blog/Pages, apply.html, thankyou.html work)
app = Flask(__name__, static_folder='.', static_url_path='')

def build_email_body(form_data):
    # Build a readable body with HTML-safe escaping
    lines = []
    for key in form_data:
        # request.form may include multiple values; take first
        value = form_data.get(key)
        lines.append(f"{key}: {value}")
    return "\n".join(lines)

@app.route("/apply", methods=["POST"])
def apply():
    form = request.form

    # Required fields validation
    if not form.get("first_name") or not form.get("last_name") or not form.get("applicant_email"):
        return "Missing required fields", 400

    # 🔹 DYNAMIC receiver from form (blog.py input)
    receiver = form.get("owner")

    # 🔐 Minimal validation (VERY IMPORTANT)
    if not receiver or "@" not in receiver:
        abort(400)

    job_title = form.get("job_title") or form.get("job_title_visible") or "Job Application"
    applicant_name = f"{form.get('first_name','')} {form.get('last_name','')}".strip()

    # Construct email
    msg = EmailMessage()
    msg["Subject"] = f"Job Application: {job_title} - {applicant_name}"
    msg["From"] = SMTP_USER          # FIXED sender
    msg["To"] = receiver             # ✅ DYNAMIC receiver

    body = build_email_body(form)
    msg.set_content(body)

    html_lines = ["<h2>New Job Application</h2>", "<pre>"]
    html_lines.append(escape(body))
    html_lines.append("</pre>")
    msg.add_alternative("\n".join(html_lines), subtype="html")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print("SMTP error:", e)
        return "Failed to send application", 500

    return redirect("/thankyou.html")


if __name__ == "__main__":
    # For development only. On production use gunicorn/uwsgi.
    app.run(host="0.0.0.0", port=5000, debug=True)

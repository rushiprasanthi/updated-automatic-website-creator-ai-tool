# updated-automatic-website-creator-ai-tool
this is a AI tools this crestes a websites to the user usage: user crestes a websites without coding language 
```markdown
Automatic Website Creator — Extended with Job Application Form & Emailing
=======================================================================

What this delivers
- blog.py (interactive generator) — now validates owner email, fixes services bug, and injects an "Apply Now" link on generated article pages.
- template.html (updated) — shows an "Apply Now" button that links to the job application form.
- apply.html — job application form (client-side reads owner and job from query params).
- server.py — Flask backend that receives POSTed applications and emails them to OWNER_EMAIL via SMTP.
- thankyou.html — simple confirmation page.
- requirements.txt

Important design notes
- Static HTML cannot directly send email. server.py (Flask + SMTP) is required to accept the submitted form and deliver it via SMTP.
- The backend uses environment variables (OWNER_EMAIL, SMTP_USER, SMTP_PASS). OWNER_EMAIL must be set to the owner email you validated when running blog.py (so the owner receives submissions).
- For Gmail, create an "App Password" and use that as SMTP_PASS. Do not use your account's main password.

Setup & run (local development)
1. Install dependencies
   python -m pip install -r requirements.txt

2. Set environment variables (example Linux/macOS)
   export OWNER_EMAIL="you@yourdomain.com"
   export SMTP_USER="you@yourdomain.com"
   export SMTP_PASS="your_smtp_app_password"

   On Windows PowerShell:
   $env:OWNER_EMAIL="you@yourdomain.com"
   $env:SMTP_USER="you@yourdomain.com"
   $env:SMTP_PASS="your_smtp_app_password"

   NOTE: OWNER_EMAIL should be the same real email you entered when you ran blog.py previously (so that the contact info and the recipient match).

3. Generate a blog page
   python blog.py
   - Follow prompts. When asked for Gmail ID (owner email) enter a real email address that will receive applications.
   - The generated HTML will be saved to Blog/Pages/<slug>.html

4. Run the Flask server (serves apply.html, thankyou.html and will receive '/apply' posts)
   python server.py

5. Open the generated page in a browser (e.g. http://localhost:5000/Blog/Pages/<slug>.html)
   - Click "Apply Now" to open the form.
   - Fill and submit the form.
   - The application will be emailed to OWNER_EMAIL.

Security & production notes
- Use HTTPS in production and run Flask behind a proper WSGI server (gunicorn, uWSGI).
- For Gmail, use an App Password (if using a Google account with 2FA).
- Consider adding CAPTCHA and validation on server side to reduce spam.
- The server currently saves failed email bodies to local files for debugging. Remove or secure this in production.

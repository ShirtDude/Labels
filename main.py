from flask import Flask, redirect, render_template, request, url_for
from secrets import save_openai_secret
from email_labels import send_email

app = Flask(__name__)
app.secret_key = b"_5#y2L\"F4Q8z\n\xec]/"

@app.route("/")
def index():
    """Renders index.html template."""
    return render_template("index.html")

@app.route("/send_email", methods=["POST"])
def send_email_view():
    """Sends email to the recipient."""
    to_email = request.form["to_email"]
    subject = request.form["subject"]
    message = request.form["message"]
    try:
        send_email(to_email, subject, message)
        return redirect(url_for("index"))
    except smtplib.SMTPException as error:
        return f"An error occurred: {error}"

if __name__ == "__main__":
    save_openai_secret()
    app.run(debug=True)

import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)


def generate_password(length=12, use_upper=True, use_lower=True,
                      use_digits=True, use_special=True) -> str:
    """Erzeugt ein Passwort nach den gewünschten Kriterien."""

    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!$%&/()=?#@*+-_"

    if not characters:
        # Fallback: wenn nichts ausgewählt ist, nimm Kleinbuchstaben
        characters = string.ascii_lowercase

    password_chars = []

    # Sicherstellen, dass jede gewählte Kategorie mindestens einmal vorkommt
    if use_upper:
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        password_chars.append(random.choice(string.digits))
    if use_special:
        password_chars.append(random.choice("!$%&/()=?#@*+-_"))

    # Rest auffüllen
    remaining = max(0, length - len(password_chars))
    password_chars += random.choices(characters, k=remaining)

    # Durchmischen
    random.shuffle(password_chars)

    return "".join(password_chars)


@app.route("/", methods=["GET", "POST"])
def index():
    generated_password = None

    if request.method == "POST":
        try:
            length = int(request.form.get("length", "12"))
        except ValueError:
            length = 12

        use_upper = request.form.get("upper") == "on"
        use_lower = request.form.get("lower") == "on"
        use_digits = request.form.get("digits") == "on"
        use_special = request.form.get("special") == "on"

        generated_password = generate_password(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special
        )

    return render_template("index.html", password=generated_password)


if __name__ == "__main__":
    # Debug=True nur für Entwicklung, nicht in Produktion benutzen
    app.run(debug=True)

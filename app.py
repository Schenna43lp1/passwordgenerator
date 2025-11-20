from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)


def generate_password(length=12, upper=True, lower=True, digits=True, special=True):
    """
    Generiert ein Passwort anhand der gewünschten Optionen.
    Optimierte, schnelle Version.
    """

    # Zeichengruppen definieren
    pools = {
        "upper": string.ascii_uppercase,
        "lower": string.ascii_lowercase,
        "digits": string.digits,
        "special": "!$%&/()=?#@*+-_"
    }

    # Ausgewählte Gruppen aktivieren
    active_groups = []
    if upper:   active_groups.append(pools["upper"])
    if lower:   active_groups.append(pools["lower"])
    if digits:  active_groups.append(pools["digits"])
    if special: active_groups.append(pools["special"])

    # Fallback, falls nichts ausgewählt
    if not active_groups:
        active_groups = [pools["lower"]]

    # Aufbau: Erst 1 Zeichen aus jeder Kategorie, Rest aus allen
    password = [random.choice(group) for group in active_groups]

    # Gesamter Zeichenpool
    all_chars = "".join(active_groups)

    # Rest auffüllen
    remaining = length - len(password)
    if remaining > 0:
        password.extend(random.choices(all_chars, k=remaining))

    # Reihenfolge mischen
    random.shuffle(password)

    return "".join(password)


@app.route("/", methods=["GET", "POST"])
def index():
    password = None

    if request.method == "POST":
        length = int(request.form.get("length", 12))

        password = generate_password(
            length=length,
            upper=request.form.get("upper") == "on",
            lower=request.form.get("lower") == "on",
            digits=request.form.get("digits") == "on",
            special=request.form.get("special") == "on"
        )

    return render_template("index.html", password=password)


if __name__ == "__main__":
    app.run(debug=False)

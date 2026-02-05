from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from database import session
from models import Anketa, Opcii, Glasovi
# from services.ai_service import generate_summary

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")

@app.route("/anketi")
def lista_anketi():
    anketi = session.query(Anketa).all()
    return render_template("lista_anketi.html", anketi=anketi)

@app.route("/anketi/new",methods=["GET","POST"])
def sozdava_anketa():
    if request.method == "POST":
        prasanje = request.form["prasanje"]
        opcii = request.form.getlist("opcii")
        rok = request.form["rok"]

        kraj = None
        if rok:
            kraj = datetime.strptime(rok, "%Y-%m-%d")

        anketa = Anketa(prasanje=prasanje,rok=kraj)
        session.add(anketa)
        session.commit()

        for o in opcii:
            opcija = Opcii(tekst=o,anketa_id=anketa.id)
            session.add(opcija)

        session.commit()
        return redirect(url_for("lista_anketi"))

    return render_template("create_anketa.html")

@app.route("/anketi/<int:anketa_id>",methods=["GET","POST"])
def anketa_detali(anketa_id):
    anketa = session.query(Anketa).get(anketa_id)

    if request.method == "POST":
        opcija_id = request.form.get("opcija")

        if not opcija_id:
            flash("Nema opcija")
            return redirect(url_for("anketa", anketa_id=anketa.id))

        glas = Glasovi(opcija_id=opcija_id)
        session.add(glas)
        session.commit()
        return redirect(url_for("anketa_detali", anketa_id=anketa.id))

    vkupno_glasovi = sum(len(o.glasovi) for o in anketa.opcii)

    return render_template(
        "anketa.html",
        anketa=anketa,
        vkupno_glasovi=vkupno_glasovi,
    )


@app.route("/ai/rewrite/<int:anketa_id>",methods=["POST"])
def ai_zaklucok(anketa_id):
    anketa = session.query(Anketa).get(anketa_id)
    rezultati = []
    vkupno = sum(len(o.glasovi) for o in anketa.opcii)

    for o in anketa.opcii:
        procent = (len(o.glasovi)/ vkupno * 100) if vkupno > 0 else 0
        rezultati.append({
            "opcija": o.tekst,
            "glasovi": o.glasovi,
            "procent": f"{round(procent, 2)}%",
        })

    # anketa.ai_zaklucok = generate_summary(anketa.prasanje,rezultati)
    session.commit()
    return redirect(url_for("anketa_detali", anketa_id=anketa.id))


@app.route("/anketi/<int:anketa_id>/delete",methods=["POST"])
def delete_anketa(anketa_id:int):
    anketa = session.get(Anketa,anketa_id)
    if not anketa:
        return "Nema vakvo Id Error 404", 404
    session.delete(anketa)
    session.commit()
    return redirect(url_for("lista_anketi"))

if __name__ == "__main__":
    app.run(debug=True)

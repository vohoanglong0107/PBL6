from flask import flash, redirect, render_template, request

from .app import app


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if "song" not in request.files:
        flash("You haven't uploaded anyfile")
        return redirect(request.url)
    song = request.files["song"]
    if not song.filename:
        flash("Song don't have filename")
        return redirect(request.url)
    return redirect("/abc")

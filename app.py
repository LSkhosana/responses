import csv
import io
import json
import os
import sqlite3
from datetime import datetime, timezone
from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for
from survey_config import SURVEYS, OPTIONS, get_survey

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-change-me")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join("data", "responses.db"))

def db():
    folder = os.path.dirname(DB_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn=db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS survey_responses(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      survey_type TEXT NOT NULL,
      started_at TEXT,
      submitted_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS answers(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      response_id INTEGER NOT NULL,
      question_key TEXT NOT NULL,
      answer_value TEXT,
      FOREIGN KEY(response_id) REFERENCES survey_responses(id)
    );
    """)
    conn.close()

def visible_answer(form, q):
    cond=q.get("show_if")
    return not cond or form.get(cond["key"]) == cond["value"]

@app.route("/")
def index():
    return render_template("index.html", surveys=SURVEYS)

@app.route("/survey/<slug>", methods=["GET","POST"])
def survey(slug):
    spec=get_survey(slug)
    if not spec: abort(404)
    if request.method=="POST":
        missing=[]
        for q in spec["questions"]:
            if q.get("required") and visible_answer(request.form,q):
                vals=request.form.getlist(q["key"])
                if not any(v.strip() for v in vals): missing.append(q["text"])
        if missing:
            flash("Please complete all required questions.")
            return render_template("survey.html", survey=spec, options=OPTIONS, form=request.form)
        conn=db()
        cur=conn.execute("INSERT INTO survey_responses(survey_type,started_at,submitted_at) VALUES(?,?,?)",
            (slug, request.form.get("_started_at"), datetime.now(timezone.utc).isoformat()))
        rid=cur.lastrowid
        for q in spec["questions"]:
            if not visible_answer(request.form,q): continue
            vals=request.form.getlist(q["key"])
            if not vals: continue
            value=json.dumps(vals) if q["type"]=="multi" else vals[0]
            conn.execute("INSERT INTO answers(response_id,question_key,answer_value) VALUES(?,?,?)",(rid,q["key"],value))
        conn.commit(); conn.close()
        return redirect(url_for("thank_you"))
    return render_template("survey.html", survey=spec, options=OPTIONS, form={})

@app.route("/thank-you")
def thank_you(): return render_template("thank_you.html")

@app.route("/admin")
def admin():
    conn=db()
    total=conn.execute("SELECT COUNT(*) c FROM survey_responses").fetchone()["c"]
    counts={r["survey_type"]:r["c"] for r in conn.execute("SELECT survey_type,COUNT(*) c FROM survey_responses GROUP BY survey_type")}
    common={}
    positive={"Agree","Strongly agree"}
    for key in ["common_easy_use","common_information","common_manual_work","common_workflow","common_confidence","common_training","common_support","common_resolution"]:
        rows=conn.execute("SELECT answer_value FROM answers WHERE question_key=?",(key,)).fetchall()
        common[key]=round(100*sum(r["answer_value"] in positive for r in rows)/len(rows)) if rows else None
    recent=conn.execute("SELECT id,survey_type,submitted_at FROM survey_responses ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    return render_template("admin.html", total=total, counts=counts, common=common, recent=recent)

@app.route("/admin/responses")
def responses():
    module=request.args.get("module","")
    conn=db()
    if module in SURVEYS:
        rows=conn.execute("SELECT * FROM survey_responses WHERE survey_type=? ORDER BY id DESC",(module,)).fetchall()
    else:
        rows=conn.execute("SELECT * FROM survey_responses ORDER BY id DESC").fetchall()
    out=[]
    for r in rows:
        answers={a["question_key"]:a["answer_value"] for a in conn.execute("SELECT question_key,answer_value FROM answers WHERE response_id=?",(r["id"],))}
        out.append({"row":r,"answers":answers})
    conn.close()
    return render_template("responses.html", responses=out, surveys=SURVEYS, module=module)

@app.route("/admin/export.csv")
def export_csv():
    conn=db()
    rows=conn.execute("SELECT * FROM survey_responses ORDER BY id").fetchall()
    keys=[]
    for slug in SURVEYS:
        for q in get_survey(slug)["questions"]:
            if q["key"] not in keys: keys.append(q["key"])
    buf=io.StringIO(); writer=csv.writer(buf)
    writer.writerow(["response_id","survey_type","submitted_at",*keys])
    for r in rows:
        answers={a["question_key"]:a["answer_value"] for a in conn.execute("SELECT question_key,answer_value FROM answers WHERE response_id=?",(r["id"],))}
        writer.writerow([r["id"],r["survey_type"],r["submitted_at"],*[answers.get(k,"") for k in keys]])
    conn.close()
    return Response(buf.getvalue(), mimetype="text/csv", headers={"Content-Disposition":"attachment; filename=hph_medworkflow_feedback.csv"})

if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)), debug=os.environ.get("FLASK_DEBUG")=="1")
else:
    init_db()

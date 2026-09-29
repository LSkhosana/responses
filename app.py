import csv
import io
import json
import os
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for
from survey_config import SURVEYS, OPTIONS, get_survey

app=Flask(__name__)
app.secret_key=os.environ.get("SECRET_KEY","dev-change-me")
DB_PATH=os.environ.get("DATABASE_PATH",os.path.join("data","responses.db"))

def db():
    folder=os.path.dirname(DB_PATH)
    if folder: os.makedirs(folder,exist_ok=True)
    conn=sqlite3.connect(DB_PATH); conn.row_factory=sqlite3.Row
    return conn

def init_db():
    conn=db(); conn.executescript("""
    CREATE TABLE IF NOT EXISTS survey_responses(id INTEGER PRIMARY KEY AUTOINCREMENT,survey_type TEXT NOT NULL,started_at TEXT,submitted_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS answers(id INTEGER PRIMARY KEY AUTOINCREMENT,response_id INTEGER NOT NULL,question_key TEXT NOT NULL,answer_value TEXT,FOREIGN KEY(response_id) REFERENCES survey_responses(id));
    """); conn.close()

def visible_answer(form,q):
    cond=q.get("show_if"); return not cond or form.get(cond["key"])==cond["value"]

def question_map():
    out={}
    for slug in SURVEYS:
        for q in get_survey(slug)["questions"]: out.setdefault(q["key"],q)
    return out

@app.route("/")
def index(): return render_template("index.html",surveys=SURVEYS)

@app.route("/survey/<slug>",methods=["GET","POST"])
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
            return render_template("survey.html",survey=spec,options=OPTIONS,form=request.form)
        conn=db()
        cur=conn.execute("INSERT INTO survey_responses(survey_type,started_at,submitted_at) VALUES(?,?,?)",(slug,request.form.get("_started_at"),datetime.now(timezone.utc).isoformat()))
        rid=cur.lastrowid
        for q in spec["questions"]:
            if not visible_answer(request.form,q): continue
            vals=request.form.getlist(q["key"])
            if not vals: continue
            value=json.dumps(vals) if q["type"]=="multi" else vals[0]
            conn.execute("INSERT INTO answers(response_id,question_key,answer_value) VALUES(?,?,?)",(rid,q["key"],value))
        conn.commit(); conn.close()
        return redirect(url_for("thank_you"))
    return render_template("survey.html",survey=spec,options=OPTIONS,form={})

@app.route("/thank-you")
def thank_you(): return render_template("thank_you.html")

@app.route("/admin")
def admin():
    conn=db()
    total=conn.execute("SELECT COUNT(*) c FROM survey_responses").fetchone()["c"]
    counts={r["survey_type"]:r["c"] for r in conn.execute("SELECT survey_type,COUNT(*) c FROM survey_responses GROUP BY survey_type")}
    positive={"Agree","Strongly agree"}; common={}
    common_keys=["common_easy_use","common_information","common_manual_work","common_workflow","common_confidence","common_training","common_support","common_resolution"]
    for key in common_keys:
        rows=conn.execute("SELECT answer_value FROM answers WHERE question_key=?",(key,)).fetchall()
        common[key]=round(100*sum(r["answer_value"] in positive for r in rows)/len(rows)) if rows else None
    module_common={}
    for slug in SURVEYS:
        module_common[slug]={}
        for key in common_keys:
            rows=conn.execute("""SELECT a.answer_value FROM answers a JOIN survey_responses r ON r.id=a.response_id
                WHERE a.question_key=? AND r.survey_type=?""",(key,slug)).fetchall()
            module_common[slug][key]=round(100*sum(r["answer_value"] in positive for r in rows)/len(rows)) if rows else None
    diagnostic_keys={
      "admissions":["case_available","case_complete","create_pre_admission","create_theatre_case","trimed_available","trimed_reentry","trimed_fallback"],
      "doctor-rooms":["patient_capture_easy","case_create_easy","without_help","outside_method","case_not_appear","workflow_change"],
      "theatre":["cases_appear","cases_complete","manual_add","reorder_easy","late_change_easy","excel_export","outside_info","work_change"]
    }
    qmap=question_map(); diagnostics={}
    for slug,keys in diagnostic_keys.items():
        diagnostics[slug]=[]
        for key in keys:
            rows=conn.execute("""SELECT a.answer_value FROM answers a JOIN survey_responses r ON r.id=a.response_id
              WHERE a.question_key=? AND r.survey_type=?""",(key,slug)).fetchall()
            c=Counter(r["answer_value"] for r in rows)
            diagnostics[slug].append({"label":qmap[key]["text"],"total":len(rows),"top":c.most_common(1)[0] if c else None,"distribution":dict(c)})
    training={}
    for slug in SURVEYS:
        rows=conn.execute("""SELECT a.answer_value FROM answers a JOIN survey_responses r ON r.id=a.response_id
          WHERE a.question_key='training_more' AND r.survey_type=?""",(slug,)).fetchall()
        c=Counter(r["answer_value"] for r in rows); training[slug]={"total":len(rows),"yes":c.get("Yes",0),"no":c.get("No",0),"unsure":c.get("Unsure",0)}
    feedback=[]
    for key,label in [("improved_most","What improved"),("frustration","Current frustration"),("improve_one","Priority improvement")]:
        rows=conn.execute("""SELECT r.survey_type,a.answer_value,r.submitted_at FROM answers a JOIN survey_responses r ON r.id=a.response_id
          WHERE a.question_key=? AND TRIM(a.answer_value)<>'' ORDER BY r.id DESC LIMIT 12""",(key,)).fetchall()
        feedback.extend({"category":label,"module":r["survey_type"],"text":r["answer_value"],"submitted_at":r["submitted_at"]} for r in rows)
    recent=conn.execute("SELECT id,survey_type,submitted_at FROM survey_responses ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()
    return render_template("admin.html",total=total,counts=counts,common=common,module_common=module_common,diagnostics=diagnostics,training=training,feedback=feedback,recent=recent,surveys=SURVEYS)

@app.route("/admin/responses")
def responses():
    module=request.args.get("module",""); conn=db()
    rows=conn.execute("SELECT * FROM survey_responses WHERE survey_type=? ORDER BY id DESC",(module,)).fetchall() if module in SURVEYS else conn.execute("SELECT * FROM survey_responses ORDER BY id DESC").fetchall()
    qmap=question_map(); out=[]
    for r in rows:
        answers=[]
        for a in conn.execute("SELECT question_key,answer_value FROM answers WHERE response_id=?",(r["id"],)):
            val=a["answer_value"]
            try:
                parsed=json.loads(val)
                if isinstance(parsed,list): val=", ".join(parsed)
            except (json.JSONDecodeError,TypeError): pass
            answers.append({"label":qmap.get(a["question_key"],{}).get("text",a["question_key"]),"value":val})
        out.append({"row":r,"answers":answers})
    conn.close()
    return render_template("responses.html",responses=out,surveys=SURVEYS,module=module)

@app.route("/admin/export.csv")
def export_csv():
    conn=db(); rows=conn.execute("SELECT * FROM survey_responses ORDER BY id").fetchall(); keys=[]
    for slug in SURVEYS:
        for q in get_survey(slug)["questions"]:
            if q["key"] not in keys: keys.append(q["key"])
    buf=io.StringIO(); writer=csv.writer(buf); writer.writerow(["response_id","survey_type","submitted_at",*keys])
    for r in rows:
        answers={a["question_key"]:a["answer_value"] for a in conn.execute("SELECT question_key,answer_value FROM answers WHERE response_id=?",(r["id"],))}
        writer.writerow([r["id"],r["survey_type"],r["submitted_at"],*[answers.get(k,"") for k in keys]])
    conn.close()
    return Response(buf.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=hph_medworkflow_feedback.csv"})

if __name__=="__main__":
    init_db(); app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=os.environ.get("FLASK_DEBUG")=="1")
else: init_db()

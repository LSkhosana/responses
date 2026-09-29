# HPH Medworkflow Post-Implementation Review

Internal feedback application for evaluating the Medworkflow implementation at Hoedspruit Private Hospital.

## What it covers

- Admissions
- Doctor Rooms / Doctor Dashboard
- Theatre Management
- Common user experience, training and support measures
- Anonymous response viewing and CSV export

Operational Medworkflow analytics remain separate from survey feedback and are combined during the final analysis/report.

## Stack

Python/Flask, SQLite, HTML/CSS and vanilla JavaScript.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Privacy

The review is anonymous by default. Do not collect patient names, ID numbers or other patient information in free-text responses.

## Production deployment

Set `SECRET_KEY` and configure `DATABASE_PATH` to a persistent disk path. SQLite must not be stored only on an ephemeral deployment filesystem.

# Invoice Email Automation

Automated invoice reminder system that reads unpaid invoices from Google Sheets and sends email reminders to clients daily at 9:00 AM.

---

## How It Works

1. Reads invoice data from your Google Sheet as a CSV
2. Parses `due_date` and `reminder_date` into proper date objects
3. Loops through every row and checks:
   - Today's date is **on or after** the `due_date`
   - `has_paid` is `"no"`
4. If both conditions are true, sends a reminder email to that client
5. Repeats automatically every day at **9:00 AM**

---

## Project Structure

```
travnook/
├── main.py          # Main script — loads sheet, checks invoices, sends emails
└── email_login.py   # Contains the send_email() function
```

---

## Google Sheet Format

Your sheet must be named `invoice_data` and have these exact column headers:

| Column | Description |
|---|---|
| `email` | Client's email address |
| `name` | Client's first name |
| `invoice_no` | Invoice number (e.g. `INV-21-12-009`) |
| `amount` | Amount owed |
| `due_date` | Payment due date (`DD/MM/YY`) |
| `reminder_date` | Date to send reminder (`DD/MM/YY`) |
| `has_paid` | `yes` or `no` |

> **Note:** The Google Sheet must be set to **public** or accessible via link so the script can read it as a CSV.

---

## Configuration

In `main.py`, set your Google Sheet credentials at the top:

```python
SHEET_ID = "your_google_sheet_id_here"
SHEET_NAME = "invoice_data"
```

Your Sheet ID is found in the URL:
```
https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit
```

---

## Installation

```bash
pip install pandas schedule
```

---

## Usage

```bash
python main.py
```

The script will:
- Run **once immediately** on startup
- Then repeat every day at **9:00 AM**
- Print `Emails has been sent.` or `No emails to send.` after each run

---

## Keeping It Running 24/7

The script must stay running for the scheduler to work. Options:

### Windows Task Scheduler
Schedule `python main.py` to run at 9AM daily — Windows handles it automatically even after reboots.

### Linux Cron Job
```bash
0 9 * * * /usr/bin/python3 /path/to/main.py
```

### Cloud Deployment
Deploy to [Railway](https://railway.app), [Render](https://render.com), or a VPS (DigitalOcean, AWS) for always-on execution without needing your PC on.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pandas` | Reads Google Sheet CSV and parses dates |
| `schedule` | Runs the job on a daily timer |
| `email_login` | Custom module containing `send_email()` |


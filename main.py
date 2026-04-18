from datetime import date
import pandas as pd
import schedule
import time
from email_login import send_email


SHEET_ID = "1vn3kUy9HYCNcPF7lTMxVp6VLs-2IdEY10bsjqt8u6aE"
SHEET_NAME = "invoice_data"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def load_df(url):
    df = pd.read_csv(url)
    df["due_date"] = pd.to_datetime(df["due_date"], format="%d/%m/%y")
    df["reminder_date"] = pd.to_datetime(df["reminder_date"], format="%d/%m/%y")
    return df

def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0

    for _, row in df.iterrows():
        if (present >= row["due_date"].date()) and (row["has_paid"].strip().lower() == "no"):
            send_email(
                subject=f'[TravNook] Invoice: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1

    if email_counter > 0:
        print("Emails has been sent.")
    else:
        print("No emails to send.")

def cron_job():
    df = load_df(URL)
    result = query_data_and_send_emails(df)
    print(result)


schedule.every().day.at("09:00").do(cron_job)

if __name__ == "__main__":
    cron_job()
    while True:
        schedule.run_pending()
        time.sleep(60)
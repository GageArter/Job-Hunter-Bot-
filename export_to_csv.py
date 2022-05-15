import gspread
import sqlite3
import csv
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

############ GOOGLE AUTHORIZATION #############

credentials = ServiceAccountCredentials.from_json_keyfile_name('google_creds.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open('Job Hunter Data')

############ EXPORT CODE #############

print("EXPORTING TO CSV...")
#connect to db
conn = sqlite3.connect('jobs.db')
c = conn.cursor()
c.execute("SELECT * from jobs")
# move db to csv
with open("jobs.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter="\t")
    csv_writer.writerow([i[0] for i in c.description])
    csv_writer.writerows(c)
    csv_file.close()
#upload csv to gspread
with open('jobs.csv', 'r') as csv_file:
    content = csv_file.read()
    client.import_csv(spreadsheet.id, data = content.encode('utf-8'))

print("DATA EXPORTED.")
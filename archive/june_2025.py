from sys import int_info

import requests
from bs4 import BeautifulSoup, Comment
import re
import time
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

import gspread
from oauth2client.service_account import ServiceAccountCredentials

RATING_MILESTONES = [400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
ACCESS_FILE = "velvety-rock-453721-q8-9216969d6bf4.json"


def get_uscf_ids(data_sheet): # Gets USCF IDs directly from Google sheets
    all_uscf_ids = []
    id_column = data_sheet.col_values(4)[375:]
    print(id_column)

    for uscf_id in id_column:
        if uscf_id == "":  # Stop when an empty cell is encountered
            break
        all_uscf_ids.append(uscf_id)

    return all_uscf_ids


def get_name(session, uscf_id): # Returns name for any player
    url = f"https://www.uschess.org/msa/MbrDtlMain.php?{uscf_id}"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    name = soup.find("b").text.split(" ", 1)[1]

    return name

def get_june_rating(session, uscf_id):
    url = f"https://www.uschess.org/msa/MbrDtlMain.php?{uscf_id}"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    cell = soup.find("td", string=lambda text: text and "Regular Rating" in text)
    b_tag = cell.find_next('b')
    rating = int(re.search(r"\d+", b_tag.text).group())
    print(f"Rating: {rating}")

    return rating



def scrape(session, uscf_id_list):

    for row_index, uscf_id in enumerate(uscf_id_list, start=376):

        name = get_name(session, uscf_id)
        print(name)

        june_rating = get_june_rating(session, uscf_id)

        data_row = [june_rating]
        start_column = 5
        cell_range = f"{chr(64 + start_column)}{row_index}"

        sheet.update(range_name=cell_range, values=[data_row])


if __name__ == '__main__':
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(ACCESS_FILE, scope)

    client = gspread.authorize(creds)

    sheet = client.open("June Ratings").sheet1

    uscf_ids = get_uscf_ids(sheet)




    # Open Google Sheet

    start_time = time.time()
    session = requests.Session()
    scrape(session, uscf_ids)
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.3f} seconds")
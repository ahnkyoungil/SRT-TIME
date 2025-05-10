from flask import Flask, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/arrival/<departure>/<arrival>/<train_no>')
def get_arrival(departure, arrival, train_no):
    url = 'https://etk.srail.kr/hpg/hra/01/selectScheduleList.do'
    today = datetime.today().strftime('%Y%m%d')

    payload = {
        'dptRsStnCd': departure,
        'arvRsStnCd': arrival,
        'stlbTrnClsfCd': '05',
        'dptDt': today,
        'dptTm': '000000',
        'psgNum': '1',
        'seatAttCd_3': '000',
        'seatAttCd_4': '011',
        'seatAttCd_5': '001',
        'seatAttCd_6': '013',
        'seatAttCd_7': '015',
        'seatAttCd_8': '014'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    res = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.select('table.tbl_col tbody tr')

    for row in rows:
        tds = row.find_all('td')
        if len(tds) > 1 and train_no.strip() in tds[1].text:
            arrival_time = tds[3].text.strip()
            return jsonify({'arrival_time': arrival_time})

    return jsonify({'error': 'not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime, timedelta
import ch_url
import ch_create

app = Flask(__name__)

def fetch_links():
    url = "https://menu.5ch.net/bbstable.html"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        link_set = {(link.get_text(), link['href']) for link in links}
        link_list = list(link_set)
        return link_list
    else:
        return []

@app.route('/')
def index():
    links = fetch_links()
    return render_template('index.html', links=links)

@app.route('/get_selected_link', methods=['POST'])
def get_selected_link():
    selected_text = request.form.get('selected_text')
    links = fetch_links()
    selected_link = next((href for text, href in links if text == selected_text), None)
    if selected_link:
        last_segment = urlparse(selected_link).path.rstrip('/').split('/')[-1]
        return jsonify({'url': f"http://hissi.org/read.php/{last_segment}/"})
    return jsonify({'error': 'Link not found'}), 404

@app.route('/execute_action', methods=['POST'])
def execute_action():
    url = request.form.get('url')
    id_value = request.form.get('id_value')
    keyword_value = request.form.get('keyword_value')
    date = request.form.get('date')
    data = ch_url.process_data(url, id_value, keyword_value, date)
    processed_data = ch_create.process_href_attributes_list(data)
    return jsonify({'data': processed_data})

if __name__ == '__main__':
    app.run(debug=True)

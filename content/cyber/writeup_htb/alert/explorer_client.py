import requests
import sys
import time

explore_server_ip = '<REPLACE_ME>'
explore_server_port = '<REPLACE_ME>'
explore_server_url = f'http://{explore_server_ip}:{explore_server_port}'

def cat_file(filepath):
    args = {
        "filepath": filepath
    }

    a = requests.post(explore_server_url, data=args)
    time.sleep(1)
    print(requests.get(explore_server_url + '/readfile', params = {'filepath':filepath}).text)

if __name__ == "__main__":
    filepath = sys.argv[1]
    cat_file(filepath)
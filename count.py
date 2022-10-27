import time
import os
import csv
from typing import Final
import http.client
from urllib.parse import urlparse
import requests
from parse_env import read_env_file


read_env_file()
CISCO_MERAKI_BASE_URL: Final = os.getenv('CISCO_MERAKI_BASE_URL')
CISCO_MERAKI_ORG_ID: Final = os.getenv('CISCO_MERAKI_ORG_ID')
CISCO_MERAKI_NETWORK_ID: Final = os.getenv('CISCO_MERAKI_NETWORK_ID')
CISCO_MERAKI_API_KEY: Final = os.getenv('CISCO_MERAKI_API_KEY')
CISCO_MERAKI_CAMERA_SERIAL: Final = os.getenv('CISCO_MERAKI_CAMERA_SERIAL')
REQUEST_HEADERS: Final = {
  'X-Cisco-Meraki-API-Key': CISCO_MERAKI_API_KEY
}
CSV_FILE_PATH: Final = os.getenv('CSV_FILE_PATH')


def csv_init() -> None:
    with open(CSV_FILE_PATH, 'a', newline='') as f_out:
        csv_writer = csv.writer(f_out, delimiter=';')
        csv_writer.writerow(['filename', 'count'])


def csv_add_image(filename: str, people_count: int) -> None:
    """Records a new picture in the csv"""
    with open(CSV_FILE_PATH, 'a', newline='') as f_out:
        csv_writer = csv.writer(f_out, delimiter=';')
        csv_writer.writerow([filename, people_count])


def get_epoch_ms():
    """Returns the epoch time in ms"""
    return int(time.time() * 1000)


def download_image(url: str):
    """Downloads an image from a URL"""
    domain = urlparse(url).netloc
    conn = http.client.HTTPSConnection(domain)
    conn.request('GET', url, '', {})
    res = conn.getresponse()
    data = res.read()
    filename = f'./images/snapshot_{get_epoch_ms()}.jpeg'
    with open(filename, 'wb') as f:
        f.write(data)


def main():
    """Main"""
    alive = True
    while alive:
        try:
            response = requests.post(f'{CISCO_MERAKI_BASE_URL}/devices/{CISCO_MERAKI_CAMERA_SERIAL}/camera/generateSnapshot', headers=REQUEST_HEADERS)

            if response.status_code == 202:
                response_payload = response.json()
                image_url = response_payload.get('url')
                # print(f'Downloading image from {response_payload.get("url")}...')
                # response =
                download_image(image_url)

                # if response.status_code == 200:
                #     filename = f'./images/snapshot_{get_epoch_ms()}.jpeg'
                #     with open(filename, 'wb') as f:
                #         f.write(response.content)
                # else:
                #     print('Cannot get image')
                #     print(response.text)

                response = requests.get(f'{CISCO_MERAKI_BASE_URL}/devices/{CISCO_MERAKI_CAMERA_SERIAL}/camera/analytics/live', headers=REQUEST_HEADERS)
                if response.status_code == 200:
                    image_filename = f'test_{get_epoch_ms()}'
                    people_count = response.json().get('zones').get('0').get('person')
                    csv_add_image(image_filename, people_count)
                else:
                    print('Cannot get analytics')
                    print(response.text)
            else:
                print('Cannot get image URL')
                print(response.text)

            time.sleep(5)
        except KeyboardInterrupt:
            alive = False
    print('Bye!')


if __name__ == "__main__":
    main()

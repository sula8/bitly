import requests
import os
import sys
import argparse
from dotenv import load_dotenv


def shorten_link(token, long_url):
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  headers = {
    'Authorization': token,
    'Accept-Language': 'ru-RU'
  }
  data = {
    "long_url": long_url
  }
  response = requests.post(url, headers=headers, json=data)
  response.raise_for_status()
  short_link = response.json()['id']
  return short_link

def count_clicks(token, bitlink):
  payload = {"unit":"day", "units":"-1"}
  url = 'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'.format(bitlink=bitlink)
  headers = {
    'Authorization': token,
    'Accept-Language': 'ru-RU'
  }
  response = requests.get(url, params=payload, headers=headers)
  response.raise_for_status()
  total_clicks = response.json()['total_clicks']
  return total_clicks

def create_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('url')
  return parser


if __name__ == '__main__':
  load_dotenv()
  bitly_token = os.getenv("BITLY_TOKEN")
  parser = create_parser()
  namespace = parser.parse_args(sys.argv[1:])
  url = namespace.url
  if url.startswith("bit"):
    total_clicks = count_clicks(bitly_token, url)
    print(total_clicks)
  else:
    try:
      short_link = shorten_link(bitly_token, url)
      print(short_link)
    except requests.exceptions.HTTPError as error:
      exit("Can't get data from server:\n{0}".format(error))
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import json
import subprocess
import urllib
import urllib.request
from datetime import datetime
import time

###################### functions #####################

def send_message(msg, iserror=False):
  if not TELEGRAM_BOT_API_KEY:
    return

  if iserror:
    text = LOG_PREFIX + ' ERROR: ' + msg
  else:
    text = LOG_PREFIX + ' ' + msg

  data = {
    "chat_id": TELEGRAM_CHANNEL,
    "text": text,
    "disable_notification": "false" if iserror else "true"
  }

  params = json.dumps(data).encode('utf8')
  url = "https://api.telegram.org/bot"+TELEGRAM_BOT_API_KEY+"/sendMessage";

  req = urllib.request.Request(url, data=params, headers={'content-type': 'application/json'})

  try:
    response = urllib.request.urlopen(req)
  except urllib.error.HTTPError as e:
    error_message = e.read()
    print(error_message)
    raise

def convert_bytes(num):
  """
  this function will convert bytes to MB.... GB... etc
  """
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
      if num < 1024.0:
          return "%3.1f %s" % (num, x)
      num /= 1024.0


def file_size(file_path):
  """
  this function will return the file size
  """
  if os.path.isfile(file_path):
      file_info = os.stat(file_path)
      return convert_bytes(file_info.st_size)
  else:
    raise Exception('File not exists', file_path)

def pretty_time(sec):
  m, s = divmod(sec, 60)
  h, m = divmod(m, 60)
  return "%d:%02d:%02d" % (h, m, s)

######################################################
start_time = time.time()

os.chdir('/dumps')

parser = argparse.ArgumentParser(description='Dumps postgresql database.\nAll pg_dump options allowed.', add_help=False)
parser.add_argument('-f', metavar="filename", required=True, default='', help="output file or directory name")
parser.add_argument('-?','--help', action='help', help="show this help, then exit")

args, unknown = parser.parse_known_args()

TELEGRAM_BOT_API_KEY = os.environ.get('TELEGRAM_BOT_API_KEY', None)
TELEGRAM_CHANNEL = os.environ.get('TELEGRAM_CHANNEL', None)
LOG_PREFIX = os.environ.get('LOG_PREFIX', 'pgdumper: ')

popen = subprocess.Popen('pg_dump '+' '.join(sys.argv[1:])+' -w', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = popen.communicate()

if popen.returncode != 0:
  send_message(err.decode("utf-8"), iserror=True)
  raise Exception(err)
else:
  runtime = pretty_time(int(time.time() - start_time))
  send_message('dump created: '+args.f+' size: '+file_size(args.f)+' time: '+runtime)

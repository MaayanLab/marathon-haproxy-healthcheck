from dotenv import load_dotenv
import base64
import functools
import json
import logging
import os
import time
import urllib.parse, urllib.request

logging.basicConfig(
  format='%(asctime)s %(levelname)-8s %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv(override=True)

BASE_MARATHON_URL = os.environ['MARATHON_URL']
MARATHON_AUTHORIZATION = 'Basic ' + base64.b64encode(
  (os.environ['MARATHON_USERNAME'] + ':' + os.environ['MARATHON_PASSWORD']).encode()
).decode('ascii')

def marathon_app_restart(marathon_image):
  logging.info('restarting `%s`...' % (marathon_image))
  req = urllib.request.urlopen(
    urllib.request.Request(
      BASE_MARATHON_URL + '/v2/apps/' + marathon_image + '/restart',
      method='POST',
      headers={
        'Content-Type': 'application/json',
        'Authorization': MARATHON_AUTHORIZATION,
      },
      data=json.dumps({
        'force': False,
      }).encode('utf8'),
    )
  )
  assert req.status == 200, 'Failed to restart the application'

def check_url(url):
  try:
    logging.info('checking `%s`...' % (url))
    req = urllib.request.urlopen(
      urllib.request.Request(url, method='GET')
    )
    return req.status <= 299
  except Exception as e:
    logging.error(e)
    return False

restart_haproxy = functools.partial(marathon_app_restart, 'maayan-haproxy-certified')

apps = {
  # url: what to do on failure
  'https://amp.pharm.mssm.edu/archs4/': restart_haproxy,
  'https://amp.pharm.mssm.edu/biojupies/': restart_haproxy,
  'https://amp.pharm.mssm.edu/chea3/': restart_haproxy,
  'https://amp.pharm.mssm.edu/creeds/': restart_haproxy,
  'https://amp.pharm.mssm.edu/Enrichr/': restart_haproxy,
  'https://amp.pharm.mssm.edu/geneshot/': restart_haproxy,
  'https://amp.pharm.mssm.edu/Harmonizome/': restart_haproxy,
  'https://amp.pharm.mssm.edu/kea3/': restart_haproxy,
  'https://amp.pharm.mssm.edu/L1000CDS2/': restart_haproxy,
  'https://amp.pharm.mssm.edu/l1000fwd/': restart_haproxy,
  'https://amp.pharm.mssm.edu/scavi/': restart_haproxy,
}

for url, func_on_failure in apps.items():
  if not check_url(url):
    func_on_failure()
    time.sleep(5)
  time.sleep(1)

import hashlib
import hmac
import time
import urllib
import urllib2

APP_ID      = '1385'
API_KEY     = 'j27mMuFbtKPvGVz8AEQRLY'
API_SECRET  = 'iFbDAY5horzPVsuWOMxj1tE3lSCe2nyg'

def api_request(url, request_method='get', params={}):
  nonce       = str(int(time.time() * 1e6))
  message     = str(nonce) + str(APP_ID) + API_KEY
  signature   = hmac.new(API_SECRET, message, hashlib.sha256).hexdigest()

  headers = {
    'Access-Nonce': nonce,
    'Access-Key': API_KEY,
    'Access-Signature': signature
  }

  if request_method == 'get':
    req = urllib2.Request(url, headers=headers)
  elif request_method == 'post':
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    req = urllib2.Request(url, data=urllib.urlencode(params), headers=headers)

  try:
    response      = urllib2.urlopen(req)
    status_code   = response.getcode()
    response_body = response.read()
  except urllib2.HTTPError as e:
    status_code   = e.getcode()
    response_body = e.read()

  return status_code, response_body
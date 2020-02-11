#app.py
#from gevent import monkey, pwsgi
import json, os, shutil
import falcon

class ansibleResource:

  def __init__(self, user, url, dir, cmd):
    self.ssh_user = user
    self.git_url = url
    self.git_dir = dir
    self.command = cmd

  def validate_req_body(self, body):
    print(body)
    return body

  def on_get(self, req, resp):
    """Handles GET requests"""
    result = {'error': 'invalid request'}
    print(json.dumps(result))
    resp.body = json.dumps(result)

  def on_post(self, req, resp):
    """Handles POST requests"""
    try:
      raw_json = req.stream.read().decode('utf-8')
    except Exception as ex:
      raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'This service only accepts POST requests: {}'.format(ex))

    try:
      result = json.loads(raw_json, encoding='utf-8')
      self.validate_req_body(result)

      ansible_cmd = self.command
      if ('real-run' in result):
        print("Request for real run, this will potentially make changes to the inventory system(s)")
      else:
        print("Defaulting to check only mode, no changes will be made to inventory system(s)")
        ansible_cmd += ' --check'

      if ('ask-pass' in result):
        print('ssh pass included in request, using pass instead of key')
        ansible_cmd += ' --ask pass {}'.format(result['ask-pass'])
      else:
        print('ssh pass not included with request, using mounted private key instead')
        ansible_cmd += ' --key-file /key.rsa'

      # print('HTTP request body: {}'.format(json.dumps(result)))

      print(ansible_cmd)
      if "check" in result:
        if result.check:
          print('Webhook asked for check mode, changes will not be applied to inventory.')
          ansible_cmd += ' --check'

      #resp.body = json.dumps(result)
    except ValueError:
      raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Could not decode the request body, must be a valid JSON document.')

    try:
      if os.path.exists(self.git_dir):
          shutil.rmtree(self.git_dir)

      # Clone the git repo
      clone_result = os.system('git clone {} {}'.format(self.git_url, self.git_dir))
      print('Clone result: {}'.format(clone_result))

      # Execute the ansible run command
      os.system(ansible_cmd)

      # return the log
      run_log = open(os.environ["ANSIBLE_LOG_PATH"], 'r')
      resp.status = falcon.HTTP_202
      resp.body = {
        "run_log": run_log.read()
      }
      
    except Exception as ex:
      raise falcon.HTTPError(falcon.HTTP_500,'Server Error', 'Actual error: {}'.format(ex))



api = falcon.API()
api.add_route('/run', ansibleResource(
  os.environ["SSH_USER"],
  os.environ["GIT_URL"],
  os.environ["GIT_DIR"],
  os.environ["ANSIBLE_CMD"]
))
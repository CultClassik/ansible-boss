#app.py
import falcon, json, os, shutil

class ansibleResource:

  def __init__(self, user, url, dir, cmd):
    self.ssh_user = user
    self.git_url = url
    self.git_dir = dir
    self.command = cmd

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
      print('HTTP request body: {}'.format(json.dumps(result)))
      ansible_cmd = self.command
      if "check" in result:
        print('Webhook asked for check mode, changes will not be applied to inventory.')
        ansible_cmd.append(' --check')

      resp.body = json.dumps(result)
    except ValueError:
      raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Could not decode the request body, must be a valid JSON document.')

    try:
      # Delete the git repo folder if it exists
      if os.path.exists(self.git_dir):
          shutil.rmtree(self.git_dir)

      # Clone the git repo
      #git.Git(self.git_dir).clone(self.git_url)
      clone_result = os.system('git clone {} {}'.format(self.git_url, self.git_dir))
      print('Clone result: {}'.format(clone_result))

      # print contents of ansible repo dir
      print(os.listdir(self.git_dir))

      # Execute the ansible run command
      os.system(self.command)

      # add a falcon response here?

    except Exception as ex:
      raise falcon.HTTPError(falcon.HTTP_500,'Server Error', 'Actual error: {}'.format(ex))

api = falcon.API()
api.add_route('/run', ansibleResource(
  os.environ["SSH_USER"],
  os.environ["GIT_URL"],
  os.environ["GIT_DIR"],
  os.environ["ANSIBLE_CMD"]
))
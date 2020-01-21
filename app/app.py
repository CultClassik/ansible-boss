#app.py
import falcon, json, os, shutil, asyncio

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
        if result.check:
          print('Webhook asked for check mode, changes will not be applied to inventory.')
          ansible_cmd += ' --check'

      #resp.body = json.dumps(result)
    except ValueError:
      raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', 'Could not decode the request body, must be a valid JSON document.')

    try:
      run_task = asyncio.ensure_future(
        run_ansible(self.git_url, self.git_dir, ansible_cmd))

      print('Created Ansible run task: {}'.format(run_task))
      resp.status = falcon.HTTP_202
      resp.body = 'Ansible run initiated as asyncio task'
      print('Awaiting task completion: {}'.format(await run_task))
    except Exception as ex:
      raise falcon.HTTPError(falcon.HTTP_500,'Server Error', 'Actual error: {}'.format(ex))

async def run_ansible(repo_url, clone_to_dir, ansible_cmd):
  try:
    # Delete the git repo folder if it exists
    if os.path.exists(clone_to_dir):
        shutil.rmtree(clone_to_dir)

    # Clone the git repo
    clone_result = os.system('git clone {} {}'.format(repo_url, clone_to_dir))
    print('Clone result: {}'.format(clone_result))

    # Execute the ansible run command
    os.system(ansible_cmd)
  except Exception as ex:
    print('Application error: {}'.format(ex))

api = falcon.API()
api.add_route('/run', ansibleResource(
  os.environ["SSH_USER"],
  os.environ["GIT_URL"],
  os.environ["GIT_DIR"],
  os.environ["ANSIBLE_CMD"]
))
#app.py
import falcon, json, git, os, shutil

class ansibleResource:

    def __init__(self, user, host, url, dir, cmd):
        self.ssh_user = user
        self.ssh_host = host
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
            raise falcon.HTTPError(falcon.HTTP_400,'Error',ex.message)

        try:
            result = json.loads(raw_json, encoding='utf-8')
            print(json.dumps(result))
            resp.body = json.dumps(result)
            # Clone the git repo
            git.Git(self.git_dir).clone(self.git_url)
            # Use ssh to execute ansible run on remote host
            os.system('ssh -o StrictHostKeyChecking=no -i /key.rsa {}@{} "{}"',format(self.ssh_user, self.ssh_host, self.command))
            # Delete the git repo folder
            shutil.rmtree(self.git_dir)

        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The ''JSON was incorrect.')

api = falcon.API()
api.add_route('/deploy', ansibleResource(
    os.environ["SSH_USER"],
    os.environ["SSH_HOST"],
    os.environ["GIT_URL"],
    os.environ["GIT_DIR"],
    os.environ["ANSIBLE_CMD"]
))
#app.py
import falcon, json
from os import system



class ansibleResource:

    ssh_user = os.environ["SSH_USER"]
    ssh_host = os.environ["SSH_HOST"]

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
            system('ssh -o StrictHostKeyChecking=no -i /key.rsa {}@{} "ansible cmd line goes here"',format(ssh_user, ssh_host))

        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,'Invalid JSON','Could not decode the request body. The ''JSON was incorrect.')

api = falcon.API()
api.add_route('/deploy', ansibleResource())
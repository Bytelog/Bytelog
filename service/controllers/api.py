from .. import documents
from flask import Blueprint
from flask import abort
from flask import render_template
from subprocess import Popen, PIPE

blueprint = Blueprint('api', __name__, url_prefix='/api')



#TODO: Implement proper update which doesn't rebuild everything
@blueprint.route('/notify')
def notify():
    # Verify that it's github or localhost

    # Return forbidden if not verified

    # Shell out to git

    """
    id = 'c15acbcafcd9947ca21d5204fed8ab36bd2ed9cc'
    dir = 'content'

    with Popen(['git', 'pull'], cwd=dir, stdout=PIPE) as proc:
        print("::", proc.communicate()[0])

    with Popen(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', id], cwd=dir, stdout=PIPE) as proc:
        files = proc.communicate()[0].split()
        [reader.build(f, print("Updating: ", files)
        for file in files
        reader.build()

    """
    # Return 204 if successful
    return '', 204


@blueprint.route('update/<item>')
def update():
    pass


@blueprint.route('/rebuild')
def rebuild():
    documents.remove()
    documents.update()
    return '', 204


"""
def verify_request(payload, ip):

    # Check for secure token

    # Get sha string
    #ver, signature = request.headers.get('X-Hub-Signature')
    if ver != 'sha1':
        abort(501)

    mac = hmac.new(str(secret), msg=request.data, digestmod=sha1)

    if hmac.compare_digest(str(mac.hexdigest()), str(signature))
        return True

    abort(403)
    return False
"""
# TODO: Implement 418 (I'm a teapot)
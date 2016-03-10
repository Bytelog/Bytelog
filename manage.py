#from flask.ext.assets import ManageAssets
from flask.ext.script import Manager
from service import create_app

app = create_app()

manager = Manager(app)
#manager.add_command("assets", ManageAssets())

if __name__ == '__main__':
    manager.run()

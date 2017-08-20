from flask_script import Manager
from app import app

# Initializing the manager
manager = Manager(app)

# Run the manager
if __name__ == '__main__':
    manager.run()

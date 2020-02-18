import sys
sys.path.insert(1, './source/')
from api import app

if __name__ == '__main__':
    app.run()

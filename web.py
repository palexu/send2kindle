import web
from schedule import run_background

if __name__ == '__main__':
    run_background()
    web.app.run(debug=False)

from flask import Flask

app = Flask(__name__, static_folder=None)


@app.route('/')
def hello():
    return "Hello World!"


def main():
    app.run()


if __name__ == '__main__':
    main()

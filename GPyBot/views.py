from flask import Flask

app = Flask(__name__)

app.config.from_object('')

@app.route('/')
def index():
    return "Hi Bebi Amandine !"

#if __name__ == "__main__":
#    app.run()

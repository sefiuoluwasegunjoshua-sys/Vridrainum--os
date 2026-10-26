from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>🔮 VIBRANIUM OS IS LIVE!</h1><p>Bro you built it!</p><p>Your free AI Jarvis is running.</p>"
if __name__ == '__main__':
    app.run()

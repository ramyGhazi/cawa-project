from flask import Flask

app=Flask(__name__)
app.secret_key='asdasdasd12e124e412e'
from TP import routes

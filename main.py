from api import app
from api.sign_up import sign_up
from api.sign_in import sign_in
from api.products import *
from api.vending_machines import *
from api.admin import *

app.run(host="127.0.0.1", port=5000)

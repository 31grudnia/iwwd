import pyrebase

config = {
  "apiKey": "AIzaSyD7tmTTkKaPwOW8MHt42ruhar2dd-xmduo",
  "authDomain": "iwwd-77dbe.firebaseapp.com",
  "databaseURL": "https://iwwd-77dbe-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "iwwd-77dbe",
  "storageBucket": "iwwd-77dbe.appspot.com",
  "messagingSenderId": "344923570857",
  "appId": "1:344923570857:web:13e6de707a2f5e105fdfb8",
  "measurementId": "G-RQLTSRR24G"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

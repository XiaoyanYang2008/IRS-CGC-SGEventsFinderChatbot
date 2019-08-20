class Config(object):
    #EventFinda
    EF_API_USERNAME = 'eventfindachatbot'
    EF_API_PASSWORD = 'nyrp2bhh98nt'
    EF_GEN_URL = 'http://api.eventfinda.sg/v2/events.json?row=10t&$q=%s&order=popularity'
    # Firebase config
    FIREBASE_APIKEY = "apiKey",
    FIREBASE_authDomain = "projectId.firebaseapp.com"
    FIREBASE_DBURL= "https://databaseName.firebaseio.com"
    storageBucket = "projectId.appspot.com"
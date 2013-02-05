
from google.appengine.ext import db

#### Datastore Classes ####

class App(db.Model):
    number = db.IntegerProperty()
    title = db.StringProperty()
    appId = db.StringProperty()
    heroHeader = db.StringProperty()
    heroCopy = db.TextProperty()
    pdfChapter = db.BooleanProperty(default=True)
    timestamp = db.DateTimeProperty(auto_now=True)

# for the "Build It" section of a generated app page
class Step(db.Model):
	# appId = db.IntegerProperty() # specifies app the step belongs to
	appId = db.StringProperty() # temporary identifier | TODO: remove this
	number = db.IntegerProperty()
	header = db.StringProperty()
	copy = db.TextProperty()
	videoPath = db.StringProperty()
	fullscreenPath = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)

class Concept(db.Model):
	# appId = db.IntegerProperty() # specifies app the step belongs to
	appId = db.StringProperty() # temporary identifier | TODO: remove this
	number = db.IntegerProperty()
	header = db.StringProperty()
	copy = db.TextProperty()
	blockPath = db.StringProperty()
	videoPath = db.StringProperty()
	fullscreenPath = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)

class Custom(db.Model):
	# appId = db.IntegerProperty() # specifies app the step belongs to
	appId = db.StringProperty() # temporary identifier | TODO: remove this
	number = db.IntegerProperty()
	header = db.StringProperty()
	copy = db.TextProperty()
	blockPath = db.StringProperty()
	videoPath = db.StringProperty()
	fullscreenPath = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)


class Account(db.Model):
    	firstName = db.StringProperty()
	lastName = db.StringProperty()
	dateOfBirth = db.StringProperty()
	location = db.StringProperty()
	organization = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)
	user = db.UserProperty()


# for the "Conceptualize It" section of a generated app page	
# class Concept(db.Model):	 

# for the "Customize It" section of a generated app page
# class Custom(db.Model):

	





		
		
	
		
	
	

		



	







 


    

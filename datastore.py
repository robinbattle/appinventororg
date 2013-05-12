
from google.appengine.ext import db

#### Datastore Classes ####

class App(db.Model):
    number = db.IntegerProperty()
    title = db.StringProperty()
    appId = db.StringProperty()
    heroHeader = db.StringProperty()
    heroCopy = db.TextProperty()
    pdfChapter = db.BooleanProperty(default=True)
    conceptualLink = db.BooleanProperty(default=True)
    manyMold = db.StringProperty()
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
        user = db.UserProperty()
        profilePicture = db.BlobProperty()
    	firstName = db.StringProperty()
	lastName = db.StringProperty()
	location = db.StringProperty()
	organization = db.StringProperty()
	ifEducator = db.BooleanProperty(default=False)
	educationLevel = db.StringProperty()
	introductionLink = db.StringProperty()
	timestamp = db.DateTimeProperty(auto_now=True)
	latitude = db.FloatProperty()
	longitude = db.FloatProperty()

class DefaultAvatarImage(db.Model):
        title = db.StringProperty()
        picture = db.BlobProperty(default=None)

class Position(db.Model):
        latitude = db.FloatProperty()
	longitude = db.FloatProperty()

class Comment(db.Model):
        submitter = db.ReferenceProperty()
        timestamp = db.DateTimeProperty(auto_now=True)
        content = db.StringProperty()
        appId = db.StringProperty()
	
	
	


# for the "Conceptualize It" section of a generated app page	
# class Concept(db.Model):	 

# for the "Customize It" section of a generated app page
# class Custom(db.Model):

	





		
		
	
		
	
	

		



	







 


    

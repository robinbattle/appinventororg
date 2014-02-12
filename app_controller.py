import logging
import os
import datetime
try: import simplejson as json
except ImportError: import json
import wsgiref.handlers
import cgi
import urllib2, json
from google.appengine.api import urlfetch

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
from time import time
from datastore import App
from datastore import Step
from datastore import Custom
from datastore import Account
from datastore import Comment
from datastore import Position
from datastore import Tutorial
from datastore import TutorialStep
import gdata.analytics.client
import gdata.sample_util
import datetime
from datetime import date
from geopy import geocoders
from google.appengine.api import mail
import locale

APPSDIR='/apps'
APPS2DIR='/apps2'

def intWithCommas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

class Home(webapp.RequestHandler):
    def get(self):
        #
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        #appCount = allAppsQuery.count()
        #allAppsList = allAppsQuery.fetch(appCount)
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        #visitor
        email="lubin2012tj@gmail.com"             #change it here
        password="1223343a"       #chage it here
        table_ids = (
                    'ga:34666339',          # TABLE_ID for first website
                                            # This is the table ID, or can be seen as
                                            # ga: PROFILE_ID
                                            # THe profile_id of Appinventor.org is 34666339
                                            # (...)
                    )

        SOURCE_APP_NAME = 'Genomika-Google-Analytics-Quick-Client-v1'
        client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)
        client.client_login(email, password, source=SOURCE_APP_NAME, service=client.auth_service)

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=2000)
        counter = 0
        for table_id in table_ids:
            for table_id in table_ids:
                data_query=gdata.analytics.client.DataFeedQuery({
                'ids': table_id,
                'start-date':yesterday.isoformat(),
                'end-date': today.isoformat(),
                'metrics': 'ga:visits, ga:pageviews'})      
        feed = client.GetDataFeed(data_query)                                           
         
        numVisitors = feed.entry[0].metric[0].value
	
	numVisitors=int(numVisitors)
	formattedCounter=intWithCommas(numVisitors)
        
        template_values={'allAppsList': allAppsList, 'userStatus': userStatus, 'counter': formattedCounter}
        
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/index.html')
        self.response.out.write(template.render(path, template_values))


class PublicProfileHandler(webapp.RequestHandler):
    def get(self):

        key = self.request.get("accountKey")
        account = db.get(key)
        if not account:
            self.response.out.write('Invalid Request')
            return

                #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)




        template_values={'account': account,  'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/publicProfile.html')
        self.response.out.write(template.render(path, template_values))



class ProfileHandler(webapp.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()

        educationLevelCheck0 = ''
        educationLevelCheck1 = ''
        educationLevelCheck2 = ''
        ifEducatorShow = "collapse"

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        if not user:
            self.redirect(userStatus['loginurl'])

        if account:  # dude has already registered
            message='Welcome Back,'
            firstName = account.firstName
            lastName = account.lastName
            location = account.location
            organization = account.organization
            displayName=account.displayName
            ifEducator = account.ifEducator
            if(ifEducator == True):
                ifEducatorShow = "collapse in"
            else:
                ifEducatorShow = "collapse"

            educationLevel = account.educationLevel
            if educationLevel == None:
                educationLevelCheck0 = 'checked'
            else:
                if educationLevel == 'K-8':
                    educationLevelCheck0 = 'checked'
                elif educationLevel == 'High School':
                    educationLevelCheck1 = 'checked'
                elif educationLevel == 'College/University':
                    educationLevelCheck2 = 'checked'
            
        else:
            message='Welcome Aboard,'
            firstName = ''
            lastName = ''
            location = ''
            organization = ''
            ifEducator = ''
            educationLevel = ''               
            user = users.get_current_user()
            account = Account()
            account.user  = user
            account.firstName = ''
            account.lastName = ''
            account.location = ''
            account.organization = ''
            account.introductionLink = ''
            account.displayName = str(user.nickname())#default displayname is email
            account.put()

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)




        template_values={'account': account,  'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus,
                         'ifEducatorShow': ifEducatorShow, 'educationLevel': educationLevel, 'educationLevelCheck0': educationLevelCheck0, 'educationLevelCheck1': educationLevelCheck1, 'educationLevelCheck2': educationLevelCheck2}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/profile.html')
        self.response.out.write(template.render(path, template_values))

class ChangeProfileHandler(webapp.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()

        

        educationLevelCheck0 = ''
        educationLevelCheck1 = ''
        educationLevelCheck2 = ''
        ifEducatorShow = "collapse"

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        if not user:
            self.redirect(userStatus['loginurl'])


        if account:  # dude has already registered
            message='Welcome Back,'
            firstName = account.firstName
            lastName = account.lastName
            location = account.location
            organization = account.organization
            account.displayName = account.displayName
            displayName = account.displayName
            ifEducator = account.ifEducator
            if(ifEducator == True):
                ifEducatorShow = "collapse in"
            else:
                ifEducatorShow = "collapse"

            educationLevel = account.educationLevel
            if educationLevel == None:
                educationLevelCheck0 = 'checked'
            else:
                if educationLevel == 'K-8':
                    educationLevelCheck0 = 'checked'
                elif educationLevel == 'High School':
                    educationLevelCheck1 = 'checked'
                else:
                    educationLevelCheck2 = 'checked'
            
        else:
            message='Welcome Aboard,'
            firstName = ''
            lastName = ''
            location = ''
            organization = ''
            ifEducator = ''
            educationLevel = ''

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        template_values={'account': account,  'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 
                         'ifEducatorShow': ifEducatorShow, 'educationLevelCheck0': educationLevelCheck0, 'educationLevelCheck1': educationLevelCheck1, 'educationLevelCheck2': educationLevelCheck2}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/changeProfile.html')
        self.response.out.write(template.render(path, template_values))
    
        
class SaveProfile(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()

        ##user status
        #userStatus = UserStatus()
        #userStatus = userStatus.getStatus(self.request.uri)
        #if not user:
        #    self.redirect(userStatus['loginurl'])


        if account:  # dude has already registered
            message='Welcome Back,'
        else:
            message='Welcome Aboard,'
            account = Account()

        account.user=user
        account.firstName=self.request.get('firstName')
        account.lastName=self.request.get('lastName')
        account.location=self.request.get('location')
        account.organization=self.request.get('organization')
        account.displayName=self.request.get('displayName')
        b=self.request.get('ifEducator')
        if(b == "on"):
                account.ifEducator = True
                #only record lat/lon if it is an educator
                g = geocoders.GoogleV3()
                try:
                    
                    place, (lat, lng) = g.geocode(account.location)
                    account.latitude = float(lat)
                    account.longitude = float(lng)
                except:
                    a = "1"
        else:
                account.ifEducator = False
        
        
        account.educationLevel=self.request.get('educationLevel')
        link = self.request.get('introductionLink')
        if(len(link.strip()) == 0):
            account.introductionLink = ''
        else:
            link = link.replace("http://","")
            link = link.replace("https://","")
            account.introductionLink = link
        

        
        account.put()

        #if uploading image
        if self.request.get('pictureFile') is not None :
            if len(self.request.get('pictureFile').strip(' \t\n\r')) != 0:
                self.uploadimage()
                self.redirect("/profile?savePic=successful")

        self.redirect("/profile?save=successful" + str(self.request.get('h')))
        #self.redirect("/profile?save=successful")
        
    def uploadimage(self):
        picture = self.request.get('pictureFile')

        user = users.get_current_user()
        account_query = db.GqlQuery("Select * from Account where user=:1",user)
        account = account_query.get()



        x1=float(self.request.get('x1'))
        y1=float(self.request.get('y1'))
        x2=float(self.request.get('x2'))
        y2=float(self.request.get('y2'))
        newH=float(self.request.get('h'))
        newW=float(self.request.get('w'))

        x_left=float(self.request.get('x_left'))
        y_top=float(self.request.get('y_top'))
        x_right=float(self.request.get('x_right'))
        y_bottom=float(self.request.get('y_bottom'))

        originalW = x_right-x_left
        originalH = y_bottom-y_top

        #originalW = 300
        #originalH = 300

        


        x1_fixed = x1 - x_left
        y1_fixed = y1 - y_top
        x2_fixed = x2 - x_left
        y2_fixed = y2 - y_top


        if(x1_fixed < 0):
            x1_fixed = 0
        if(y1_fixed < 0):
            y1_fixed = 0
        if(x2_fixed > originalW):
            x2_fixed = originalW
        if(y2_fixed > originalH):
            y2_fixed = originalH


        picture = images.crop(picture, float(x1_fixed/originalW), float(y1_fixed/originalH), float(x2_fixed/originalW), float(y2_fixed/originalH))
        picture = images.resize(picture, 300, 300)


        if not account:
            account = Account()
        if picture:
            account.user = user      #maybe duplicate, but it is really imporant to make sure
            account.profilePicture = db.Blob(picture)  
        account.put()
        return


    
class CourseOutlineHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/outline.html')
        self.response.out.write(template.render(path, template_values))

class GettingStartedHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/gettingstarted.html')
        self.response.out.write(template.render(path, template_values))

class IntroductionHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introduction.html')
        self.response.out.write(template.render(path, template_values))

class CourseInABoxHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/course-in-a-box.html')
        self.response.out.write(template.render(path, template_values))

class CourseInABoxHandlerTeaching(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/course-in-a-box.html')
        self.response.out.write(template.render(path, template_values))


class SoundBoardHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/soundboard.html')
        self.response.out.write(template.render(path, template_values))

class PortfolioHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/portfolio.html')
        self.response.out.write(template.render(path, template_values))


class IntroTimerHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introTimerEvents.html')
        self.response.out.write(template.render(path, template_values))

class SmoothAnimationHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/smoothAnimation.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/media.html')
        self.response.out.write(template.render(path, template_values))

class MediaFilesHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/mediaFiles.html')
        self.response.out.write(template.render(path, template_values))

class StructureHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/structure.html')
        self.response.out.write(template.render(path, template_values))


class HelloPurrHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/helloPurr.html')
        self.response.out.write(template.render(path, template_values))

class AppPageHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/appPage.html')
        self.response.out.write(template.render(path, template_values))

class AppInventorIntroHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/AppInventorIntro.html')
        self.response.out.write(template.render(path, template_values))

class RaffleHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/raffleApp.html')
        self.response.out.write(template.render(path, template_values))
class LoveYouHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/loveYou.html')
        self.response.out.write(template.render(path, template_values))

class LoveYouWSHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/loveYouWS.html')
        self.response.out.write(template.render(path, template_values))


class AndroidWhereHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/androidWhere.html')
        self.response.out.write(template.render(path, template_values))

class GPSHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/gpsIntro.html')
        self.response.out.write(template.render(path, template_values))

class NoTextingHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/noTexting.html')
        self.response.out.write(template.render(path, template_values))

class MoleMashHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/moleMash.html')
        self.response.out.write(template.render(path, template_values))

class PaintPotHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        

        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintPot.html')
        self.response.out.write(template.render(path, template_values))

class ShooterHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/shooter.html')
        self.response.out.write(template.render(path, template_values))

class UserGeneratedHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/userGenerated.html')
        self.response.out.write(template.render(path, template_values))

class BroadcastHubHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/broadcastHub.html')
        self.response.out.write(template.render(path, template_values))


class NoteTakerHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/noteTaker.html')
        self.response.out.write(template.render(path, template_values))


class QuizHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quiz.html')
        self.response.out.write(template.render(path, template_values))

class QuizIntroHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quizIntro.html')
        self.response.out.write(template.render(path, template_values))
class IntroIfHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandlerTeaching(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintpot.html')
        self.response.out.write(template.render(path, template_values))

class TryItHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        manyMoldAppsList = []
        for app in allAppsList:
            if app.manyMold:
                manyMoldAppsList.append(app)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'manyMoldAppsList': manyMoldAppsList, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/tryit.html')
        self.response.out.write(template.render(path, template_values))


class PaintPotIntroHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintPotIntro.html')
        self.response.out.write(template.render(path, template_values))

class MoleMashManymoHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/moleMashManymo.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandlerTeaching(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/media.html')
        self.response.out.write(template.render(path, template_values))


class TeachingHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/teaching.html')
        self.response.out.write(template.render(path, template_values))

class IHaveADreamHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/IHaveADream.html')
        self.response.out.write(template.render(path, template_values))


class WebDatabaseHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/webDatabase.html')
        self.response.out.write(template.render(path, template_values))

class ConceptsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/concepts.html')
        self.response.out.write(template.render(path, template_values))

class AbstractionHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/proceduralAbstraction.html')
        self.response.out.write(template.render(path, template_values))

class MoleMash2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/molemashAI2.html')
        self.response.out.write(template.render(path, template_values))

class HelloPurr2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/hellopurrAI2.html')
        self.response.out.write(template.render(path, template_values))

class PaintPot2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintpotAI2.html')
        self.response.out.write(template.render(path, template_values))
        
class NoTexting2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/notextingAI2.html')
        self.response.out.write(template.render(path, template_values))

class PresidentsQuiz2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/presidentsquizAI2.html')
        self.response.out.write(template.render(path, template_values))

class MapTour2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/maptourAI2.html')
        self.response.out.write(template.render(path, template_values))

class EventHandlersHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/eventHandlers.html')
        self.response.out.write(template.render(path, template_values))

class ConditionalsInfoHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/conditionals.html')
        self.response.out.write(template.render(path, template_values))

class PropertiesHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/properties.html')
        self.response.out.write(template.render(path, template_values))

class QuizlyHandler(webapp.RequestHandler):
    def get(self):
        quizName= self.request.get('quizname')
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
                
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR,'quizname':quizName}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/dquizly.html')
        self.response.out.write(template.render(path, template_values))

class WorkingWithMediaHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/workingWithMedia.html')
        self.response.out.write(template.render(path, template_values))

class MathBlasterHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/mathBlaster.html')
        self.response.out.write(template.render(path, template_values))


class SlideShowQuizHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/slideshowQuiz.html')
        self.response.out.write(template.render(path, template_values))

class MeetMyClassmatesHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/meetMyClassmates.html')
        self.response.out.write(template.render(path, template_values))

class JavaBridgeHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/javaBridge.html')
        self.response.out.write(template.render(path, template_values))

class AppInventor2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/appInventor2.html')
        self.response.out.write(template.render(path, template_values))

class GalleryHowToHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/galleryHowTo.html')
        self.response.out.write(template.render(path, template_values))



#MODULES
class Module1Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module1.html')
        self.response.out.write(template.render(path, template_values))

class Module2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module2.html')
        self.response.out.write(template.render(path, template_values))

class Module3Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module3.html')
        self.response.out.write(template.render(path, template_values))

class Module4Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module4.html')
        self.response.out.write(template.render(path, template_values))

class Module5Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module5.html')
        self.response.out.write(template.render(path, template_values))

class Module6Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module6.html')
        self.response.out.write(template.render(path, template_values))

class ModuleXHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/moduleX.html')
        self.response.out.write(template.render(path, template_values))
class Quiz1Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quiz1.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))

#Quiz Page
class QuizQuestionsHandler(webapp.RequestHandler):
    def get(self):
        
        template_values={}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quizquestions.html')
        self.response.out.write(template.render(path, template_values))
#Quizzes Begin
class Quiz1Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz1.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 1###

class Quiz2Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz2.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 2###
class Quiz3Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz3.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 3###
class Quiz4Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz4.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 4###
class Quiz5Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz5.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 5###
class Quiz6Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz6.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 6###
class Quiz7Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz7.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 7###
class Quiz8Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz8.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 8###
class Quiz9Handler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/Quiz9.html')
        self.response.out.write(template.render(path, template_values))
class ConditionsHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introIf.html')
        self.response.out.write(template.render(path, template_values))
###END OF QUIZ 9###




#LESSON PLANS

class LPIntroHandler(webapp.RequestHandler):
    def get(self):
        

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/ai_introduction.html')
        self.response.out.write(template.render(path, template_values))

class LPCreatingHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/creating.html')
        self.response.out.write(template.render(path, template_values))

class LPConceptsHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/programming_concepts.html')
        self.response.out.write(template.render(path, template_values))

class LPAugmentedHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/augmented.html')
        self.response.out.write(template.render(path, template_values))

class LPGamesHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/games.html')
        self.response.out.write(template.render(path, template_values))

class LPIteratingHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/iterating.html')
        self.response.out.write(template.render(path, template_values))

class LPUserGenHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/user_gen_data.html')
        self.response.out.write(template.render(path, template_values))

class LPForeachHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/foreach.html')
        self.response.out.write(template.render(path, template_values))

class LPPersistenceWorksheetHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/persistence_worksheet.html')
        self.response.out.write(template.render(path, template_values))

class LPPersistenceFollowupHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/persistence_followup.html')
        self.response.out.write(template.render(path, template_values))

class LPFunctionsHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/functions.html')
        self.response.out.write(template.render(path, template_values))

class LPCodeReuseHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/code_reuse.html')
        self.response.out.write(template.render(path, template_values))

class LPQRHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/qr_code.html')
        self.response.out.write(template.render(path, template_values))

class ContactHandler(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/contact.html')
        self.response.out.write(template.render(path, template_values))

class BookHandler(webapp.RequestHandler):
    def get(self):
        
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ }
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/book.html')
        self.response.out.write(template.render(path, template_values))


# Inventor's Manual Handlers #

class Handler14(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter14.html')
        self.response.out.write(template.render(path, template_values))

class Handler15(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter15.html')
        self.response.out.write(template.render(path, template_values))

class Handler16(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter16.html')
        self.response.out.write(template.render(path, template_values))

class Handler17(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter17.html')
        self.response.out.write(template.render(path, template_values))

class Handler18(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter18.html')
        self.response.out.write(template.render(path, template_values))

class Handler19(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter19.html')
        self.response.out.write(template.render(path, template_values))

class Handler20(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter20.html')
        self.response.out.write(template.render(path, template_values))

class Handler21(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter21.html')
        self.response.out.write(template.render(path, template_values))

class Handler22(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter22.html')
        self.response.out.write(template.render(path, template_values))

class Handler23(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter23.html')
        self.response.out.write(template.render(path, template_values))

class Handler24(webapp.RequestHandler):
    def get(self):
        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter24.html')
        self.response.out.write(template.render(path, template_values))









# ADMIN







class AddAppHandler(webapp.RequestHandler):
    def get(self):
        
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'addapp.html')
        self.response.out.write(template.render(path, template_values))

class AddStepHandler(webapp.RequestHandler):
    def get(self):
        
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'admin_step.html')
        self.response.out.write(template.render(path, template_values))

class AddConceptHandler(webapp.RequestHandler):
    def get(self):
        
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'addconcept.html')
        self.response.out.write(template.render(path, template_values))

class AddCustomHandler(webapp.RequestHandler):
    def get(self):
        
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'addcustom.html')
        self.response.out.write(template.render(path, template_values))
        
class PostStep(webapp.RequestHandler):
    def post(self):
        stepId = self.request.get('modify_step_name') # the ID is a header


        if (stepId):
            cacheHandler = CacheHandler()
            step = cacheHandler.GettingCache("Step", True, "header", stepId, False, None, None, False)

        else:
            step = Step()

        if self.request.get('appId'):
            step.appId = self.request.get('appId')

        if self.request.get('number'):
            step.number = int(self.request.get('number'))

        if self.request.get('header'):
            step.header = self.request.get('header')

        if self.request.get('copy'):
            step.copy = self.request.get('copy')

        if self.request.get('videoPath'):
            step.videoPath = self.request.get('videoPath')

        if self.request.get('fullscreenPath'):
            step.fullscreenPath = self.request.get('fullscreenPath')

        step.put()

        #flush all the memcache
        memcache.flush_all()  

        self.redirect('/AddStepPage?add_step_app_name=' + step.appId) # TODO: change to admin or app area


class PostCustom(webapp.RequestHandler):
    def post(self):

        customId = self.request.get('modify_custom_name') # the ID is a header


        if (customId):
            cacheHandler = CacheHandler()
            custom = cacheHandler.GettingCache("Custom", True, "header", customId, False, None, None, False)

        else:
            custom = Custom()

        if self.request.get('appId'):
            custom.appId = self.request.get('appId')

        if self.request.get('number'):
            custom.number = int(self.request.get('number'))

        if self.request.get('header'):
            custom.header = self.request.get('header')

        if self.request.get('copy'):
            custom.copy = self.request.get('copy')

        if self.request.get('videoPath'):
            custom.videoPath = self.request.get('videoPath')

        if self.request.get('fullscreenPath'):
            custom.fullscreenPath = self.request.get('fullscreenPath')

        custom.put()

        #flush all the memcache
        memcache.flush_all()
        
        self.redirect('/AddCustomPage?add_custom_app_name=' + custom.appId)



class AddCustomRenderer(webapp.RequestHandler):
    def get(self):
        custom_listing = ""

        appId = self.request.get('add_custom_app_name')
        cacheHandler = CacheHandler()
        app = cacheHandler.GettingCache("App", True, "appId", appId, False, None, None, False)
        appTitle = app.title

        cacheHandler = CacheHandler()
        customs = cacheHandler.GettingCache("Custom", True, "appId", appId, True, "number", "ASC", True)
   
        for custom in customs:
            custom_listing += str(custom.number) + '. ' + custom.header + '|'

        template_values = {
            'appId': appId,
            'appTitle': appTitle,
            'custom_listing': custom_listing
        }

        path = os.path.join(os.path.dirname(__file__),'static_pages/admin/admin_custom.html')
        self.response.out.write(template.render(path, template_values))

class PostApp(webapp.RequestHandler):
    def post(self):

        appId = self.request.get('modify_app_name')

        if (appId):
            cacheHandler = CacheHandler()
            app = cacheHandler.GettingCache("App", True, "appId", appId, False, None, None, False)
        else:
            app = App()

        if self.request.get('appNumber'):
            app.number = int(self.request.get('appNumber'))

        if self.request.get('appId'):
            app.appId = self.request.get('appId')

        if self.request.get('title'):
            app.title = self.request.get('title')

        if self.request.get('heroCopy'):
            app.heroCopy = self.request.get('heroCopy')

        if self.request.get('heroHeader'):
            app.heroHeader = self.request.get('heroHeader')
            
        if self.request.get('pdfChapter'):
            b = self.request.get('pdfChapter')
            if(b == "True"):
                app.pdfChapter = True
            else:
                app.pdfChapter = False
                
        if self.request.get('conceptualLink'):
            b = self.request.get('conceptualLink')
            if(b == "True"):
                app.conceptualLink = True
            else:
                app.conceptualLink = False

        if self.request.get('webTutorial'):
            b = self.request.get('webTutorial')
            if(b == "True"):
                if self.request.get('webTutorialLink'):
                    app.webTutorialLink = self.request.get('webTutorialLink')
                    app.webTutorial = True
                else:
                    app.webTutorial = False
            else:
                app.webTutorial = False

        if (self.request.get('manyMold').strip() != ''):
            app.manyMold = self.request.get('manyMold')

        if (self.request.get('version').strip() != ''):
            app.version = self.request.get('version')
            

        app.put() # now the app has a key() --> id()

        #flush all the memcache
        memcache.flush_all()
        
        self.redirect('/Admin') # TODO: change to /admin (area)
        # wherever we put() to datastore, we'll need to also save the appId

class DeleteApp(webapp.RequestHandler):
    def get(self):
        appId = self.request.get('del_app_name')
        logging.info("appId is " + appId)

        query = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId).get()
        db.delete(query)

#                app_to_del = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
#                result = app_to_del.get()
#                db.delete(result)


        #flush all the memcache
        memcache.flush_all()
        
        self.redirect('/Admin')

class DeleteStep(webapp.RequestHandler):
    def get(self):
        logging.info("hello world")
        stepId = self.request.get('del_step_name') #this id is actually step header, should be re-thinked later
        stepId = self.request.get('del_step_name') #this id is actually step header, should be re-thinked later
        
        logging.info("stepId is " + stepId)

        query = db.GqlQuery("SELECT * FROM Step WHERE header = :1", stepId).get()
        appID = query.appId
        db.delete(query)


        #flush all the memcache
        memcache.flush_all()

        self.redirect('/AddStepPage?add_step_app_name=' + appID)







class AddStepRenderer(webapp.RequestHandler):
    def get(self):
        step_listing = ""

        appId = self.request.get('add_step_app_name')
        cacheHandler = CacheHandler()
        app = cacheHandler.GettingCache("App", True, "appId", appId, False, None, None, False)
        appTitle = app.title


        cacheHandler = CacheHandler()
        steps = cacheHandler.GettingCache("Step", True, "appId", appId, True, "number", "ASC", True)
        
        for step in steps:
            step_listing += str(step.number) + '. ' + step.header + '|'

        template_values = {
            'appId': appId,
            'appTitle': appTitle,
            'step_listing': step_listing
        }

        path = os.path.join(os.path.dirname(__file__),'static_pages/admin/admin_step.html')
        self.response.out.write(template.render(path, template_values))





        
class AdminHandler(webapp.RequestHandler):
    def get(self):
        

        app_listing = ""
        app_listing2 = ""
        tutorials_listing = ""

        cacheHandler = CacheHandler()
        apps = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        apps2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        tutorials = cacheHandler.GettingCache("Tutorial", False, None, None, True, "number", "ASC", True)
        #apps = apps + apps2

        for app in apps:
            app_listing += app.appId + '|'
        for app in apps2:
            app_listing2 += app.appId + '|'
        for tutorial in tutorials:
            tutorials_listing += tutorial.tutorialId + '|'

        template_values={
            
            'app_listing': app_listing,
            'app_listing2': app_listing2,
            'tutorials_listing': tutorials_listing
        }
        path = os.path.join(os.path.dirname(__file__),'static_pages/admin/admin_main.html')
        self.response.out.write(template.render(path, template_values))





class AppRenderer(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        t_path = path[1:]
        logging.info(t_path)
        cacheHandler = CacheHandler()
        app = cacheHandler.GettingCache("App", True, "appId", t_path, False, None, None, False)
        # logging.info(app.heroCopy)

            
        steps = cacheHandler.GettingCache("Step", True, "appId", t_path, True, "number", "ASC", True)    
        customs = cacheHandler.GettingCache("Custom", True, "appId", t_path, True, "number", "ASC", True)

        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        template_values = {
            'steps': steps,
            'customs': customs,
            'app': app,
            'userStatus': userStatus,
            'allAppsList': allAppsList
            }

        path = os.path.join(os.path.dirname(__file__),'app_base.html')
        self.response.out.write(template.render(path, template_values))

class NewAppRenderer(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        #t_path = path[1:]
        t_path = path[1:(len(path)-6)] #take out -steps in path
        

        
        
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()



        cacheHandler = CacheHandler()
        app = cacheHandler.GettingCache("App", True, "appId", t_path, False, None, None, False)
        # logging.info(app.heroCopy)

            
        steps = cacheHandler.GettingCache("Step", True, "appId", t_path, True, "number", "ASC", True)    
        customs = cacheHandler.GettingCache("Custom", True, "appId", t_path, True, "number", "ASC", True)

        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

   
        #check if reach the last one
        try:
            nextApp = allAppsList[app.number]
        except:
            nextApp = None
            
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        #comment
        pquery = db.GqlQuery("SELECT * FROM Comment WHERE appId = :1 ORDER BY timestamp DESC", t_path) # t_path is appID
        #pquery = db.GqlQuery("SELECT * FROM Comment")
        comments = pquery.fetch(pquery.count())

        template_values = {
            'steps': steps,
            'customs': customs,
            'app': app,
            'allAppsList': allAppsList, 'allAppsList2': allAppsList2,
            'userStatus': userStatus,
            'nextApp':nextApp,
            'comments': comments,
            'currentAppsDir':APPSDIR
            }

        path = os.path.join(os.path.dirname(__file__),'static_pages/other/app_base_new.html')
        self.response.out.write(template.render(path, template_values))

class NewAppRenderer_AI2(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        #t_path = path[1:]
        t_path = path[1:(len(path)-6)] #take out -steps in path
        

        
        
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()



        cacheHandler = CacheHandler()
        app = cacheHandler.GettingCache("App", True, "appId", t_path, False, None, None, False)
        # logging.info(app.heroCopy)

            
        steps = cacheHandler.GettingCache("Step", True, "appId", t_path, True, "number", "ASC", True)    
        customs = cacheHandler.GettingCache("Custom", True, "appId", t_path, True, "number", "ASC", True)

        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)
        
        #check if forward to the first one
        try:
            if(app.number - 2 >= 0):
                previousApp = allAppsList2[app.number - 2]
            else:
                previousApp = None
        except:
            previousApp = None

        #check if reach the last one
        try:
            nextApp = allAppsList2[app.number]
        except:
            nextApp = None
            
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        #comment
        pquery = db.GqlQuery("SELECT * FROM Comment WHERE appId = :1 ORDER BY timestamp DESC", t_path) # t_path is appID
        #pquery = db.GqlQuery("SELECT * FROM Comment")
        comments = pquery.fetch(pquery.count())

        template_values = {
            'steps': steps,
            'customs': customs,
            'app': app,
            'allAppsList': allAppsList, 'allAppsList2': allAppsList2,
            'allAppsList2':allAppsList2,
            'userStatus': userStatus,
            'previousApp': previousApp,
            'nextApp':nextApp,
            'comments': comments,
            'currentAppsDir':APPS2DIR
            }

        path = os.path.join(os.path.dirname(__file__),'static_pages/other/app_base_new.html')
        self.response.out.write(template.render(path, template_values))

#commenting system
class PostCommentHandler (webapp.RequestHandler):
    def post(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)

        user = users.get_current_user()

        if not user:
            self.redirect(userStatus['loginurl'])

        content = self.request.get('comment_content').strip(' \t\n\r')
        if(content != ''):
            user = users.get_current_user()
            pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
            account = pquery.get()
            if not account:
                account = Account()
                account.user  = user
                account.displayName = str(user.nickname())
                account.put()
            comment = Comment()
            comment.submitter = account
            comment.content = content
            comment.appId = self.request.get('comment_appId')
            if(self.request.get('comment_replyTo')):
                comment.replyTo = db.get(self.request.get('comment_replyTo'))
                #comment.replyTo = self.request.get('comment_replyTo')
            comment.put()
            emailHandler = EmailHandler()
            emailHandler.sendToAdmin(self.request.get('redirect_link'), comment)

        
        self.redirect(self.request.get('redirect_link'))
class DeleteCommentHandler (webapp.RequestHandler):
    def get(self):
        

        user = users.get_current_user()
        
        

        if users.is_current_user_admin():
            commentKey = self.request.get('commentKey')
            if(commentKey != ""):
                db.delete(commentKey)
            self.redirect(self.request.get('redirect_link'))
        else:
            
            print 'Content-Type: text/plain'
            print 'You are NOT administrator'
        
       
class AboutHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/about.html')
        self.response.out.write(template.render(path, template_values))



class GetAppDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_app_data()")
        app = self.request.get('app')
        cacheHandler = CacheHandler()        
        app_to_get = cacheHandler.GettingCache("App", True, "appId", app, False, None, None, False)

        appId = app

        number = app_to_get.number;
        title = app_to_get.title;
        heroHeader = app_to_get.heroHeader;
        heroCopy = app_to_get.heroCopy;
        pdfChapter = app_to_get.pdfChapter;
        webTutorial = app_to_get.webTutorial;
        webTutorialLink = app_to_get.webTutorialLink;
        conceptualLink = app_to_get.conceptualLink;
        manyMold = app_to_get.manyMold;
        version = app_to_get.version;

        my_response = {'number': number, 'title': title, 'heroHeader': heroHeader, 'heroCopy': heroCopy, 'pdfChapter':pdfChapter, 'webTutorial': webTutorial, 'webTutorialLink': webTutorialLink, 'conceptualLink': conceptualLink, 'manyMold': manyMold, "version": version}
#        json = JSON.dumps(my_response)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))


class GetStepDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_step_data()")
        step_header = self.request.get('step_header')
        cacheHandler = CacheHandler()
        step = cacheHandler.GettingCache("Step", True, "header", step_header, False, None, None, False)

        appId = step.appId;
        number = step.number;
        header = step.header;
        copy = step.copy;
        videoPath = step.videoPath;
        fullPath = step.fullscreenPath;

        my_response = {'appId': appId, 'number': number, 'header': header, 'copy': copy, 'videoPath': videoPath, 'fullPath': fullPath}
        #        json = JSON.dumps(my_response)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))

class GetCustomDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_custom_data()")
        custom_header = self.request.get('custom_header')
        logging.info("custom_header: " + custom_header)
        cacheHandler = CacheHandler()
        custom = cacheHandler.GettingCache("Custom", True, "header", custom_header, False, None, None, False)

        number = custom.number;
        header = custom.header;
        copy = custom.copy;
        videoPath = custom.videoPath;
        fullPath = custom.fullscreenPath;

        my_response = {'number': number, 'header': header, 'copy': copy, 'videoPath': videoPath, 'fullPath': fullPath}
        #        json = JSON.dumps(my_response)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))

class SetupHandler(webapp.RequestHandler):
    def get(self):

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/setup2.html')
        self.response.out.write(template.render(path, template_values))

class SetupAI2Handler(webapp.RequestHandler):
    def get(self):

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/setupAI2.html')
        self.response.out.write(template.render(path, template_values))

class TryItHandler(webapp.RequestHandler):
    def get(self):
        
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)


        manyMoldAppsList = []
        for app in allAppsList:
            if app.manyMold:
                manyMoldAppsList.append(app)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
       
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus, 'manyMoldAppsList': manyMoldAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/tryit.html')
        self.response.out.write(template.render(path, template_values))


#Upload Pic
class UploadPictureHandler(webapp.RequestHandler):
    def post(self):
                
        picture = self.request.get('pictureFile')

        user = users.get_current_user()
        account_query = db.GqlQuery("Select * from Account where user=:1",user)
        account = account_query.get()



        x1=float(self.request.get('x1'))
        y1=float(self.request.get('y1'))
        x2=float(self.request.get('x2'))
        y2=float(self.request.get('y2'))
        newH=float(self.request.get('h'))
        newW=float(self.request.get('w'))

        x_left=float(self.request.get('x_left'))
        y_top=float(self.request.get('y_top'))
        x_right=float(self.request.get('x_right'))
        y_bottom=float(self.request.get('y_bottom'))

        originalW = x_right-x_left
        originalH = y_bottom-y_top

        #originalW = 300
        #originalH = 300

        


        x1_fixed = x1 - x_left
        y1_fixed = y1 - y_top
        x2_fixed = x2 - x_left
        y2_fixed = y2 - y_top


        if(x1_fixed < 0):
            x1_fixed = 0
        if(y1_fixed < 0):
            y1_fixed = 0
        if(x2_fixed > originalW):
            x2_fixed = originalW
        if(y2_fixed > originalH):
            y2_fixed = originalH


        picture = images.crop(picture, float(x1_fixed/originalW), float(y1_fixed/originalH), float(x2_fixed/originalW), float(y2_fixed/originalH))
        picture = images.resize(picture, 300, 300)

        if not account:
            account = Account()
            account.displayName = str(user.nickname())
        if picture:
            account.user = user      #maybe duplicate, but it is really imporant to make sure
            account.profilePicture = db.Blob(picture)  
        account.put()
        ad = picture
        self.redirect('/changeProfile')
                

class ImageHandler (webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        account_query = db.GqlQuery("Select * from Account where user=:1",user)
        account = account_query.get()

        #if not account:
        #    self.redirect('/assets/img/avatar-default.gif')
        #    return
            
        account_key=self.request.get('key')

        if(len(account_key) == 0):
            self.redirect('/assets/img/avatar-default.gif')
            return
            

        account = db.get(account_key)
        if account.profilePicture:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(account.profilePicture)
        else:
            self.redirect('/assets/img/avatar-default.gif')
            #self.response.headers['Content-Type'] = "image/png"
            #self.response.out.write('/assets/img/avatar-default.gif')
            #self.error(404)
#Map
class TeacherMapHandler(webapp.RequestHandler):
    def get(self):

        #all apps list
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        #allAccountsQuery = db.GqlQuery("SELECT * FROM Account")
        allAccountsQuery = db.GqlQuery("SELECT * FROM Account WHERE ifEducator=:1", True)
                                                                                    #now only show teachers
                                                                                    #TO-DO:Not sure if need to be memcached

        accountCount = allAccountsQuery.count()
        accounts = allAccountsQuery.fetch(accountCount)

        account_k_8 = []
        account_high_school = []
        account_college_university = []
        for account in accounts:
           if(account.ifEducator):
               if(account.educationLevel == "K-8"):
                   account_k_8.append(account)
               elif(account.educationLevel == "High School" ):
                   account_high_school.append(account)
               elif(account.educationLevel == "College/University"):
                   account_college_university.append(account)
               

        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'accounts': accounts, 'account_k_8':account_k_8,  'account_high_school':account_high_school, 'account_college_university':account_college_university, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/maps.html')
        self.response.out.write(template.render(path, template_values))               
               
#Google Custom Search
class SearchHandler (webapp.RequestHandler):
    def get(self):
               
        query=self.request.get('query')
        

        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)


        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/searchResult.html')
        self.response.out.write(template.render(path, template_values))


#Cache

class CacheHandler(webapp.RequestHandler):

    def GettingCache(self, tableName, whereClause, whereField, dataId, orderClause, orderField, orderValue, fetch):
        keyName = tableName.lower()
        if(whereClause == True):
            keyName = keyName + dataId

        expiredTime = 86400
        data = memcache.get(keyName)

        if data is not None:
            return data
        else:
            query = self.createDBQuery(tableName, whereClause, whereField, dataId, orderClause, orderField, orderValue)
            if(whereClause == True):
                datasQuery = db.GqlQuery(query, dataId)
            else:
                datasQuery = db.GqlQuery(query)

            if(fetch == False):
                data = datasQuery.get()
            else:
                data = datasQuery.fetch(datasQuery.count())
            
            memcache.add(keyName, data, expiredTime)
            return data
  

    def createDBQuery(self, tableName, whereClause, whereField, dataId, orderClause, orderField, orderValue):
         
        query1 = "SELECT * FROM " + tableName + " "
        if(whereClause == True):
            query2 = "WHERE " + whereField + " =:1 "
        else:
            query2 = ""
        if(orderClause == True):
            query3 = "ORDER BY " + orderField + " " + orderValue
        else:
            query3 = ""

        return query1 + query2 + query3

class MemcacheFlushHandler(webapp.RequestHandler):

    def get(self):
        memcache.flush_all()       
       
        if users.is_current_user_admin():
            if(self.request.get('redirect_link')):                  #implemented now, it is not required
                self.redirect(self.request.get('redirect_link'))
            else:
                self.redirect("/Admin")
        else:        
            print 'Content-Type: text/plain'
            print 'You are NOT administrator'        
        return


# user status checking(login/logout)
class UserStatus(webapp.RequestHandler):
    
   
    def getStatus(self, uri):
        user = users.get_current_user()
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1 ",user)
        account = pquery.get()

        loginurl = users.create_login_url(uri)
        logouturl = users.create_logout_url('/')

        admin = False
        if user:
            ifUser = True
            if users.is_current_user_admin():
                admin = True
        else:
            ifUser = False

        
        
        status = {'loginurl': loginurl, 'logouturl':logouturl, 'ifUser':ifUser, 'account':account, 'admin': admin}
        return status




#only use when add new field to database
class UpdateDatabase (webapp.RequestHandler):

    def get(self):
        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())
        for account in accounts:
            if account.introductionLink == None:
                account.introductionLink = ''
                account.put()
    
    def bacup3(self):
	  #this is from adam
        adam_boolean = true
        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())
        for account in accounts:
            b = False
            if account.lastName == None:
                account.lastName = ""
                b = True
                print account.displayName
            if account.firstName == None:
                account.firstName = ""
                b = True
            if account.location == None:
                account.location = ""
                b = True
            if account.organization == None:
                account.organization = ""
                b = True
            if(b == True):
                account.put()
        
    def backup2(self):

        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())
        
        for account in accounts:
            old = account.displayName
            i = old.find('@')
            if (i != -1):
               account.displayName = old[:i]
               account.put()

        return
    def backup(self):
        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())

        for account in accounts:
            if account.introductionLink:
                link = account.introductionLink
                if(len(link.strip()) == 0):
                    account.introductionLink = ''
                else:
                    link = link.replace("http://","")
                    link = link.replace("https://","")
                    account.introductionLink = link
                account.put()

        return
        
class UpdateGEODatabase (webapp.RequestHandler):
    def get(self):

        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())
        g = geocoders.GoogleV3()
        for account in accounts:
            if account.location:
                try:             
                    place, (lat, lng) = g.geocode(account.location)
                    account.latitude = lat
                    account.longitude = lng
                    account.put()
                except:
                    print "account_key:" + str(account.key()) + "\n"
                    print "account_name:" + account.displayName + "\n"
                    #print "account_location:" + account.location + "\n"
                    print "\n"
        return

class PrintOut (webapp.RequestHandler):
    def get(self):

        account = db.get("ahBzfmFwcGludmVudG9yb3Jncg8LEgdBY2NvdW50GOn7Aww")
        g = geocoders.GoogleV3()
        
           
        place, (lat, lng) = g.geocode(account.location)

        print lat
        print lng

        return
    
#convert profile user name
class ConvertProfileName1 (webapp.RequestHandler):
    def get(self):
        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())

        for account in accounts:
            
            try:
                firstName = account.firstName
                lastName = account.lastName
                if firstName == None or lastName == None:
                    account.displayName = str(account.user.nickname())
                    account.put()
                elif firstName.strip() == "" or lastName.strip() == "":
                    account.displayName = str(account.user.nickname())
                    account.put()
                elif firstName.strip() == "None" or lastName.strip() == "None":
                    account.displayName = str(account.user.nickname())
                    account.put()
                else:
                    account.displayName = firstName.strip() + " " + lastName.strip()
                    account.put()
                
            except:
                 print "1"
        return
class ConvertProfileName2 (webapp.RequestHandler):
    def get(self):
        pquery = db.GqlQuery("SELECT * FROM Account")
        accounts = pquery.fetch(pquery.count())

        for account in accounts:
            if account.displayName == None:
                    account.displayName = str(account.user.nickname())
                    account.put()
            
        return

class PrintUserName (webapp.RequestHandler):
    def get(self):
        key = self.request.get('key')
        account = db.get(key)

        self.response.headers['Content-Type'] = 'text/plain'

        if(account.firstName == None):
            self.response.write(" firstName: " + "\"" + "None" + "\"" )
        else:
            self.response.write(" firstName: " + "\"" + account.firstName.strip() + "\"" )

        if(account.lastName == None):
            self.response.write(" lastName: " + "\"" + "None" + "\"" )
        else:
            self.response.write(" lastName: " +  "\""+ account.firstName.strip() + "\"")

            
        if(account.displayName == None):
            self.response.write(" displayName: " +  "\""+ "None"+  "\"")
        else:
            self.response.write(" displayName: " +  "\""+ account.displayName.strip()+  "\"")


        
        return



    

class StepIframe(webapp.RequestHandler):
    def get(self):
        
        # login_url=users.create_login_url(self.request.uri)
        #       logout_url=users.create_logout_url(self.request.uri)

        #allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        #appCount = allAppsQuery.count()
        #allAppsList = allAppsQuery.fetch(appCount)
        cacheHandler = CacheHandler()
        allAppsList = cacheHandler.GettingCache("App", True, "version", "1", True, "number", "ASC", True)
        allAppsList2 = cacheHandler.GettingCache("App", True, "version", "2", True, "number", "ASC", True)

        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        
        template_values={ 'allAppsList': allAppsList, 'allAppsList2': allAppsList2, 'userStatus': userStatus}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/app_base_new_ai2_step_iframe.html')
        self.response.out.write(template.render(path, template_values))


#Web Tutorial
class WebTutorialHandler(webapp.RequestHandler):
    def get(self):
        #user status
        userStatus = UserStatus()
        userStatus = userStatus.getStatus(self.request.uri)
        tutorialId = self.request.get("tutorialId")
        tutorial = db.GqlQuery("SELECT * FROM Tutorial WHERE tutorialId = :1", tutorialId).get()

        pquery = db.GqlQuery("SELECT * FROM TutorialStep WHERE tutorialId = :1", tutorialId)
        tuturialSteps = pquery.fetch(pquery.count())

        
        template_values = {
            'userStatus': userStatus,
            'tutorial': tutorial,
            'tuturialSteps': tuturialSteps
            }

        path = os.path.join(os.path.dirname(__file__),'static_pages/other/web_tutorial.html')
        self.response.out.write(template.render(path, template_values))

class GetTutorialDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_tutorial_data()")
        tutorial = self.request.get('tutorial')
        cacheHandler = CacheHandler()        
        tutorial_to_get = cacheHandler.GettingCache("Tutorial", True, "tutorialId", tutorial, False, None, None, False)

        tutorialId = tutorial

        number = tutorial_to_get.number;
        title = tutorial_to_get.title;
        heroHeader = tutorial_to_get.heroHeader;
        heroCopy = tutorial_to_get.heroCopy;
        

        my_response = {'number': number, 'title': title, 'heroHeader': heroHeader, 'heroCopy': heroCopy, 'tutorialId': tutorialId}
#       json = JSON.dumps(my_response)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))
        
class GetTutorialStepDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_tutorial_step_data()")
        step_header = self.request.get('step_header')
        cacheHandler = CacheHandler()
        step = cacheHandler.GettingCache("TutorialStep", True, "header", step_header, False, None, None, False)

        tutorialId = step.tutorialId;
        number = step.number;
        header = step.header;
        copy = step.copy;
        tutorialLink = step.tutorialLink;

        my_response = {'tutorialId': tutorialId, 'number': number, 'header': header, 'copy': copy, 'tutorialLink': tutorialLink}
#       json = JSON.dumps(my_response)

        

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))

class PostTutorialStep(webapp.RequestHandler):
    def post(self):
        tutorialStepId = self.request.get('modify_tutorial_step_name') # the ID is a header


        if (tutorialStepId):
            cacheHandler = CacheHandler()
            tutorialStep = cacheHandler.GettingCache("TutorialStep", True, "header", tutorialStepId, False, None, None, False)

        else:
            tutorialStep = TutorialStep()

        if self.request.get('tutorialId'):
            tutorialStep.tutorialId = self.request.get('tutorialId')

        if self.request.get('number'):
            tutorialStep.number = int(self.request.get('number'))

        if self.request.get('header'):
            tutorialStep.header = self.request.get('header')

        if self.request.get('copy'):
            tutorialStep.copy = self.request.get('copy')

        if self.request.get('tutorialLink'):
            tutorialStep.tutorialLink = self.request.get('tutorialLink')


        tutorialStep.put()

        #flush all the memcache
        memcache.flush_all()

        self.redirect('/AddTutorialStepPage?add_step_tutorial_name=' + tutorialStep.tutorialId) # TODO: change to admin or app area

class PostTutorial(webapp.RequestHandler):
    def post(self):

        tutorialId = self.request.get('modify_tutorial_name')

        if (tutorialId):
            cacheHandler = CacheHandler()
            tutorial = cacheHandler.GettingCache("Tutorial", True, "tutorialId", tutorialId, False, None, None, False)
        else:
            tutorial = Tutorial()

        if self.request.get('tutorialNumber'):
            tutorial.number = int(self.request.get('tutorialNumber'))

        if self.request.get('tutorialId'):
            tutorial.tutorialId = self.request.get('tutorialId')

        if self.request.get('tutorialTitle'):
            tutorial.title = self.request.get('tutorialTitle')

        if self.request.get('tutorialHeroCopy'):
            tutorial.heroCopy = self.request.get('tutorialHeroCopy')

        if self.request.get('tutorialHeroHeader'):
            tutorial.heroHeader = self.request.get('tutorialHeroHeader')
            
        
            

        tutorial.put() # now the app has a key() --> id()

        #flush all the memcache
        memcache.flush_all()
        
        self.redirect('/Admin') # TODO: change to /admin (area)
        # wherever we put() to datastore, we'll need to also save the appId

class AddTutorialStepRenderer(webapp.RequestHandler):
    def get(self):
        step_listing = ""

        tutorialId = self.request.get('add_step_tutorial_name')
        cacheHandler = CacheHandler()
        tutorial = cacheHandler.GettingCache("Tutorial", True, "tutorialId", tutorialId, False, None, None, False)
        tutorialTitle = tutorial.title


        cacheHandler = CacheHandler()
        steps = cacheHandler.GettingCache("TutorialStep", True, "tutorialId", tutorialId, True, "number", "ASC", True)
        
        for step in steps:
            step_listing += str(step.number) + '. ' + step.header + '|'

        template_values = {
            'tutorialId': tutorialId,
            'tutorialTitle': tutorialTitle,
            'step_listing': step_listing
        }

        path = os.path.join(os.path.dirname(__file__),'static_pages/admin/admin_tutorial_step.html')
        self.response.out.write(template.render(path, template_values))


class EmailHandler(webapp.RequestHandler):
    def get(self):
        

        mail.send_mail(sender=" App Inventor <lubin2012tj@gmail.com>",
              to="<blu2@dons.usfca.edu>",
              subject="Gmail ApI Test",
              body="""
                    Test Here

                    """)

    def sendToAdmin(self, link, comment):
        mail.send_mail(sender=" <lubin2012tj@gmail.com>",
              to="David W Wolber <blu2@usfca.edu>",
              subject="Comment Notification",
              body= '',
              html= '<p><b>' + comment.submitter.displayName + '</b> says "' + comment.content + '"</p></p> <a href="http://www.appinventor.org/' + link + '">See this comment</a></p>'

              )


# create this global variable that represents the application and specifies which class
# should handle each page in the site
application = webapp.WSGIApplication(
    # MainPage handles the home page load
    [('/', Home), ('/Admin', AdminHandler),
        ('/hellopurr', AppRenderer), ('/paintpot', AppRenderer), ('/molemash', AppRenderer),
        ('/shootergame', AppRenderer), ('/no-text-while-driving', AppRenderer), ('/ladybug-chase', AppRenderer),
        ('/map-tour', AppRenderer), ('/android-where-s-my-car', AppRenderer), ('/quiz', AppRenderer),
        ('/notetaker', AppRenderer), ('/xylophone', AppRenderer), ('/makequiz-and-takequiz-1', AppRenderer),
        ('/broadcaster-hub-1', AppRenderer), ('/robot-remote', AppRenderer), ('/stockmarket', AppRenderer),
        ('/amazon', AppRenderer), ('/gettingstarted', GettingStartedHandler),
        ('/AddApp', AddAppHandler), ('/AddStep', AddStepHandler),
        ('/AddConcept', AddConceptHandler), ('/AddCustom', AddCustomHandler),
        ('/PostApp', PostApp), ('/PostStep', PostStep), ('/PostCustom', PostCustom),
        ('/outline', CourseOutlineHandler), ('/introduction', IntroductionHandler), ('/course-in-a-box', CourseInABoxHandler),('/portfolio', PortfolioHandler),('/introTimer', IntroTimerHandler),('/smoothAnimation', SmoothAnimationHandler),('/soundboard', SoundBoardHandler),
        ('/media', MediaHandler), ('/mediaFiles',MediaFilesHandler),('/teaching-android', TeachingHandler), ('/lesson-introduction-to-app-inventor', LPIntroHandler),
        ('/lesson-plan-creating', LPCreatingHandler), ('/lesson-plan-paintpot-and-initial-discussion-of-programming-con', LPConceptsHandler),
        ('/lesson-plan-mobile-apps-and-augmented-real', LPAugmentedHandler), ('/lesson-plan-games', LPGamesHandler),
        ('/iterate-through-a-list', LPIteratingHandler), ('/lesson-plan-user-g', LPUserGenHandler),
        ('/lesson-plan-foreach-iteration-and', LPForeachHandler), ('/persistence-worksheet', LPPersistenceWorksheetHandler),
        ('/persistence-r', LPPersistenceFollowupHandler), ('/functions', LPFunctionsHandler),
    ('/hellopurrLesson', HelloPurrHandler),('/paintpotLesson', PaintPotHandler),('/molemashLesson', MoleMashHandler),('/no-text-while-drivingLesson', NoTextingHandler),('/notetakerLesson', NoteTakerHandler),('/broadcaster-hub-1Lesson', BroadcastHubHandler),('/quizLesson', QuizHandler),('/shootergameLesson', ShooterHandler),('/paintPotIntro', PaintPotIntroHandler),('/structure', StructureHandler), ('/appPage', AppPageHandler),('/appInventorIntro', AppInventorIntroHandler),('/loveYouLesson', LoveYouHandler),('/loveYouWS', LoveYouWSHandler),('/raffle',RaffleHandler),('/gpsIntro', GPSHandler),('/androidWhere', AndroidWhereHandler), ('/quizIntro', QuizIntroHandler),('/userGenerated', UserGeneratedHandler), ('/tryit',TryItHandler),
        ('/procedures', LPCodeReuseHandler), ('/deploying-an-app-and-posting-qr-code-on-web', LPQRHandler),
        ('/module1', Module1Handler), ('/module2', Module2Handler), ('/module3', Module3Handler),
        ('/module4', Module4Handler), ('/module5', Module5Handler), ('/module6', Module6Handler),
        ('/moduleX', ModuleXHandler), ('/contact', ContactHandler), ('/about', AboutHandler ), ('/book', BookHandler), ('/quizquestions',  QuizQuestionsHandler), ('/Quiz1',Quiz1Handler), ('/Quiz2',Quiz2Handler), ('/Quiz3',Quiz3Handler), ('/Quiz4',Quiz4Handler), ('/Quiz5',Quiz5Handler), ('/Quiz6',Quiz6Handler), ('/Quiz7',Quiz7Handler), ('/Quiz8',Quiz8Handler), ('/Quiz9',Quiz9Handler), ('/app-architecture', Handler14), ('/engineering-and-debugging', Handler15), ('/variables-1', Handler16),
        ('/animation-3', Handler17), ('/conditionals', Handler18), ('/lists-2', Handler19),
        ('/iteration-2', Handler20), ('/procedures-1', Handler21), ("/databases", Handler22), ("/sensors-1", Handler23),
        ("/apis", Handler24), ('/course-in-a-box_teaching', CourseInABoxHandlerTeaching), ('/media_teaching', MediaHandlerTeaching),
        ('/DeleteApp', DeleteApp), ('/AddStepPage', AddStepRenderer), ('/DeleteStep', DeleteStep), ('/AddCustomPage', AddCustomRenderer),
        ('/projects', BookHandler ), ('/appinventortutorials', BookHandler), ('/get_app_data', GetAppDataHandler),
        ('/get_step_data', GetStepDataHandler), ('/get_custom_data', GetCustomDataHandler), ('/setup', SetupHandler),('/setupAI2',SetupAI2Handler),
        ('/profile', ProfileHandler), ('/changeProfile', ChangeProfileHandler),('/saveProfile', SaveProfile), ('/uploadPicture', UploadPictureHandler), ('/imageHandler', ImageHandler), ('/teacherMap', TeacherMapHandler),
        ('/siteSearch', SearchHandler), ('/moleMashManymo',MoleMashManymoHandler),


        # NewAppRenderer 
        ('/hellopurr-steps', NewAppRenderer), ('/paintpot-steps', NewAppRenderer), ('/molemash-steps', NewAppRenderer),
        ('/shootergame-steps', NewAppRenderer), ('/no-text-while-driving-steps', NewAppRenderer), ('/ladybug-chase-steps', NewAppRenderer),
        ('/map-tour-steps', NewAppRenderer), ('/android-where-s-my-car-steps', NewAppRenderer), ('/quiz-steps', NewAppRenderer),
        ('/notetaker-steps', NewAppRenderer), ('/xylophone-steps', NewAppRenderer), ('/makequiz-and-takequiz-1-steps', NewAppRenderer),
        ('/broadcaster-hub-1-steps', NewAppRenderer), ('/robot-remote-steps', NewAppRenderer), ('/stockmarket-steps', NewAppRenderer),
        ('/amazon-steps', NewAppRenderer),

        # AI2
        ('/IHaveADream-steps', NewAppRenderer_AI2), ('/paintpot2-steps', NewAppRenderer_AI2), ('/mathblaster-steps', NewAppRenderer_AI2), 

        # Comment
        ('/postComment', PostCommentHandler),('/deleteComment', DeleteCommentHandler),

        # Memcache Flush
        ('/memcache_flush_all', MemcacheFlushHandler),

        ('/introIf',ConditionsHandler),
      

        ('/IHaveADream', IHaveADreamHandler),('/properties', PropertiesHandler), ('/eventHandlers', EventHandlersHandler),('/quizly',QuizlyHandler),('/conditionalsInfo',ConditionalsInfoHandler), ('/workingWithMedia',WorkingWithMediaHandler),('/mathBlaster',MathBlasterHandler),('/appInventor2',AppInventor2Handler) ,('/slideshowQuiz',SlideShowQuizHandler), ('/javaBridge',JavaBridgeHandler), ('/meetMyClassmates',MeetMyClassmatesHandler), ('/webDatabase',WebDatabaseHandler), ('/concepts',ConceptsHandler), ('/abstraction',AbstractionHandler),('/galleryHowTo', GalleryHowToHandler), 
        ('/sentEmail', EmailHandler),

        # Update Database
        ('/updateDB', UpdateDatabase),('/updateDBGEO', UpdateGEODatabase),('/PrintOut', PrintOut),
        ('/convertProfileName1', ConvertProfileName1),('/convertProfileName2', ConvertProfileName2),
        ('/printUserName', PrintUserName),
        ('/stepIframe', StepIframe),
        
        #Web Tutorial
        ('/webtutorial', WebTutorialHandler), ('/get_tutorial_data', GetTutorialDataHandler),('/PostTutorial', PostTutorial), ('/AddTutorialStepPage', AddTutorialStepRenderer), ('/PostTutorialStep', PostTutorialStep), ('/get_tutorial_step_data', GetTutorialStepDataHandler),

        #Public Profile
        ('/publicProfile', PublicProfileHandler),

        #AI2 Chapter
        ('/PaintPot2', PaintPot2Handler),('/MoleMash2', MoleMash2Handler),('/HelloPurr2', HelloPurr2Handler),('/NoTexting2', NoTexting2Handler), ('/PresidentsQuiz2', PresidentsQuiz2Handler), ('/MapTour2', MapTour2Handler),
        
        
    ],
    debug=True)




def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()




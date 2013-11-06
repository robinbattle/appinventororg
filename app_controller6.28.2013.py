 
import logging
import os
import datetime
import json
import wsgiref.handlers
import cgi

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import datetime
from time import time
from datastore import App
from datastore import Step
from datastore import Custom

APPS2DIR='/apps2'

class Home(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        # login_url=users.create_login_url(self.request.uri)
        #		logout_url=users.create_logout_url(self.request.uri)
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)

        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/index.html')
        self.response.out.write(template.render(path, template_values))

class CourseOutlineHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/outline.html')
        self.response.out.write(template.render(path, template_values))

class GettingStartedHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/gettingstarted.html')
        self.response.out.write(template.render(path, template_values))

class IntroductionHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introduction.html')
        self.response.out.write(template.render(path, template_values))

class CourseInABoxHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/course-in-a-box.html')
        self.response.out.write(template.render(path, template_values))

class CourseInABoxHandlerTeaching(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/course-in-a-box.html')
        self.response.out.write(template.render(path, template_values))


class SoundBoardHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")


        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)

        template_values={'currenttime': currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/soundboard.html')
        self.response.out.write(template.render(path, template_values))

class PortfolioHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")


        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)

        template_values={'currenttime': currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/portfolio.html')
        self.response.out.write(template.render(path, template_values))


class IntroTimerHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/introTimerEvents.html')
        self.response.out.write(template.render(path, template_values))

class SmoothAnimationHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/smoothAnimation.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/media.html')
        self.response.out.write(template.render(path, template_values))


class StructureHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/structure.html')
        self.response.out.write(template.render(path, template_values))


class HelloPurrHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/helloPurr.html')
        self.response.out.write(template.render(path, template_values))

class AppPageHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/appPage.html')
        self.response.out.write(template.render(path, template_values))

class AppInventorIntroHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/appInventorIntro.html')
        self.response.out.write(template.render(path, template_values))

class LoveYouHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/loveYou.html')
        self.response.out.write(template.render(path, template_values))

class AndroidWhereHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/androidWhere.html')
        self.response.out.write(template.render(path, template_values))

class GPSHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/gpsIntro.html')
        self.response.out.write(template.render(path, template_values))

class NoTextingHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/noTexting.html')
        self.response.out.write(template.render(path, template_values))

class MoleMashHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/moleMash.html')
        self.response.out.write(template.render(path, template_values))

class PaintPotHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintPot.html')
        self.response.out.write(template.render(path, template_values))

class ShooterHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/shooter.html')
        self.response.out.write(template.render(path, template_values))

class UserGeneratedHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/userGenerated.html')
        self.response.out.write(template.render(path, template_values))

class BroadcastHubHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/broadcastHub.html')
        self.response.out.write(template.render(path, template_values))


class NoteTakerHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/noteTaker.html')
        self.response.out.write(template.render(path, template_values))


class QuizHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quiz.html')
        self.response.out.write(template.render(path, template_values))

class QuizIntroHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/quizIntro.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandlerTeaching(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/paintpot.html')
        self.response.out.write(template.render(path, template_values))


class PaintPotIntroHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        #allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")

        #appCount = allAppsQuery.count()
        #allAppsList = allAppsQuery.fetch(appCount)
        #template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        template_values={}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/PaintPotIntro.html')
        self.response.out.write(template.render(path, template_values))

class MediaHandlerTeaching(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/media.html')
        self.response.out.write(template.render(path, template_values))


class TeachingHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/teaching.html')
        self.response.out.write(template.render(path, template_values))

class IHaveADreamHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/IHaveADream.html')
        self.response.out.write(template.render(path, template_values))

class EventHandlersHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/eventHandlers.html')
        self.response.out.write(template.render(path, template_values))

class ConditionalsInfoHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/conditionals.html')
        self.response.out.write(template.render(path, template_values))

class PropertiesHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList, 'apps2Dir':APPS2DIR}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/properties.html')
        self.response.out.write(template.render(path, template_values))

class QuizlyHandler(webapp.RequestHandler):
    def get(self):
	quizName= self.request.get('quizname')
        currenttime = datetime.utcnow()
        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        appCount = allAppsQuery.count()
        allAppsList = allAppsQuery.fetch(appCount)
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList, 'apps2Dir':APPS2DIR,'quizname':quizName}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/dquizly.html')
        self.response.out.write(template.render(path, template_values))


#MODULES
class Module1Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module1.html')
        self.response.out.write(template.render(path, template_values))

class Module2Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module2.html')
        self.response.out.write(template.render(path, template_values))

class Module3Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module3.html')
        self.response.out.write(template.render(path, template_values))

class Module4Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module4.html')
        self.response.out.write(template.render(path, template_values))

class Module5Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module5.html')
        self.response.out.write(template.render(path, template_values))

class Module6Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module6.html')
        self.response.out.write(template.render(path, template_values))

class Module7Handler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/module7.html')
        self.response.out.write(template.render(path, template_values))





#LESSON PLANS

class LPIntroHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/ai_introduction.html')
        self.response.out.write(template.render(path, template_values))

class LPCreatingHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/creating.html')
        self.response.out.write(template.render(path, template_values))

class LPConceptsHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/programming_concepts.html')
        self.response.out.write(template.render(path, template_values))

class LPAugmentedHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/augmented.html')
        self.response.out.write(template.render(path, template_values))

class LPGamesHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/games.html')
        self.response.out.write(template.render(path, template_values))

class LPIteratingHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/iterating.html')
        self.response.out.write(template.render(path, template_values))

class LPUserGenHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/user_gen_data.html')
        self.response.out.write(template.render(path, template_values))

class LPForeachHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/foreach.html')
        self.response.out.write(template.render(path, template_values))

class LPPersistenceWorksheetHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/persistence_worksheet.html')
        self.response.out.write(template.render(path, template_values))

class LPPersistenceFollowupHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/persistence_followup.html')
        self.response.out.write(template.render(path, template_values))

class LPFunctionsHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/functions.html')
        self.response.out.write(template.render(path, template_values))

class LPCodeReuseHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/code_reuse.html')
        self.response.out.write(template.render(path, template_values))

class LPQRHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/lesson_plans/qr_code.html')
        self.response.out.write(template.render(path, template_values))

class ContactHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/contact.html')
        self.response.out.write(template.render(path, template_values))

class BookHandler(webapp.RequestHandler):
    def get(self):

        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        allAppsList = allAppsQuery.fetch(allAppsQuery.count())

        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/book.html')
        self.response.out.write(template.render(path, template_values))


# Inventor's Manual Handlers #

class Handler14(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter14.html')
        self.response.out.write(template.render(path, template_values))

class Handler15(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter15.html')
        self.response.out.write(template.render(path, template_values))

class Handler16(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter16.html')
        self.response.out.write(template.render(path, template_values))

class Handler17(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter17.html')
        self.response.out.write(template.render(path, template_values))

class Handler18(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter18.html')
        self.response.out.write(template.render(path, template_values))

class Handler19(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter19.html')
        self.response.out.write(template.render(path, template_values))

class Handler20(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter20.html')
        self.response.out.write(template.render(path, template_values))

class Handler21(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter21.html')
        self.response.out.write(template.render(path, template_values))

class Handler22(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter22.html')
        self.response.out.write(template.render(path, template_values))

class Handler23(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter23.html')
        self.response.out.write(template.render(path, template_values))

class Handler24(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'/assets/pdf/chapter24.html')
        self.response.out.write(template.render(path, template_values))









# ADMIN







class AddAppHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        # login_url=users.create_login_url(self.request.uri)
        #		logout_url=users.create_logout_url(self.request.uri)

        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'addapp.html')
        self.response.out.write(template.render(path, template_values))

class AddStepHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        # login_url=users.create_login_url(self.request.uri)
        #		logout_url=users.create_logout_url(self.request.uri)

        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'admin_step.html')
        self.response.out.write(template.render(path, template_values))

class AddConceptHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        # login_url=users.create_login_url(self.request.uri)
        #		logout_url=users.create_logout_url(self.request.uri)

        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'addconcept.html')
        self.response.out.write(template.render(path, template_values))

class AddCustomHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        # login_url=users.create_login_url(self.request.uri)
        #		logout_url=users.create_logout_url(self.request.uri)

        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'addcustom.html')
        self.response.out.write(template.render(path, template_values))
        
class PostStep(webapp.RequestHandler):
    def post(self):
        stepId = self.request.get('modify_step_name') # the ID is a header


        if (stepId):
            stepsQuery = db.GqlQuery("SELECT * FROM Step WHERE header = :1", stepId)
            step = stepsQuery.get()
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

        self.redirect('/AddStepPage?add_step_app_name=' + step.appId) # TODO: change to admin or app area


class PostCustom(webapp.RequestHandler):
    def post(self):

        customId = self.request.get('modify_custom_name') # the ID is a header


        if (customId):
            customsQuery = db.GqlQuery("SELECT * FROM Custom WHERE header = :1", customId)
            custom = customsQuery.get()
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
        self.redirect('/AddCustomPage?add_custom_app_name=' + custom.appId)



class AddCustomRenderer(webapp.RequestHandler):
    def get(self):
        custom_listing = ""

        appId = self.request.get('add_custom_app_name')
        appsQuery = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
        app = appsQuery.get()
        appTitle = app.title


        customsQuery = db.GqlQuery("SELECT * FROM Custom " +
                                 "WHERE appId = :1 " +
                                 "ORDER BY number ASC", appId)

        customs = customsQuery.fetch(customsQuery.count())

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
            appsQuery = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
            app = appsQuery.get()
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

        app.put() # now the app has a key() --> id()
        self.redirect('/Admin') # TODO: change to /admin (area)
        # wherever we put() to datastore, we'll need to also save the appId

class DeleteApp(webapp.RequestHandler):
    def get(self):
        appId = self.request.get('del_name')
        logging.info("appId is " + appId)


        apps = App.all()

        for app in apps:
            logging.info("appId is " + app.appId)
            if (app.appId is appId):
                app.appId = "aaa"
                app.put()


#                app_to_del = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
#                result = app_to_del.get()
#                db.delete(result)



        self.redirect('/Admin')

class DeleteStep(webapp.RequestHandler):
    def get(self):
        logging.info("hello world")
        stepId = self.request.get('del_name')
        logging.info("stepId is " + stepId)

#        s_query = db.GqlQuery('SELECT * FROM Step WHERE appId = :1', stepId)
#        s_result = s_query.get()
#        s_key = s_result.key()



        steps = Step.all()



        for step in steps:
            logging.info("step header is " + step.header)
            if (step.header is stepId):
                logging.info("step.header is: " + step.header)
                del step.appId
                step.put()




#                app_to_del = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
#                result = app_to_del.get()
#                db.delete(result)



        self.redirect('/AddStepPage?add_step_app_name=' + step.appId)







class AddStepRenderer(webapp.RequestHandler):
    def get(self):
        step_listing = ""

        appId = self.request.get('add_step_app_name')
        appsQuery = db.GqlQuery("SELECT * FROM App WHERE appId = :1", appId)
        app = appsQuery.get()
        appTitle = app.title



        stepsQuery = db.GqlQuery("SELECT * FROM Step " +
                                 "WHERE appId = :1 " +
                                 "ORDER BY number ASC", appId)

        steps = stepsQuery.fetch(stepsQuery.count())

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
        currenttime = datetime.utcnow()

        app_listing = ""

        apps = db.GqlQuery("SELECT * FROM App")
        for app in apps:
            app_listing += app.appId + '|'

        template_values={
            'currenttime': currenttime,
            'app_listing': app_listing
        }
        path = os.path.join(os.path.dirname(__file__),'static_pages/admin/admin_main.html')
        self.response.out.write(template.render(path, template_values))



class AppRenderer(webapp.RequestHandler):
    def get(self):
        path = self.request.path
        t_path = path[1:]
        logging.info(t_path)
        appsQuery = db.GqlQuery("SELECT * FROM App WHERE appId = :1", t_path)
        app = appsQuery.get()
        # logging.info(app.heroCopy)
        stepsQuery = db.GqlQuery("SELECT * FROM Step " +
                                 "WHERE appId = :1 " +
                                 "ORDER BY number ASC", t_path)

        customsQuery = db.GqlQuery("SELECT * FROM Custom " +
                                   "WHERE appId = :1 " +
                                   "ORDER BY number ASC", t_path)

        steps = stepsQuery.fetch(stepsQuery.count())
        customs = customsQuery.fetch(customsQuery.count())



        allAppsQuery = db.GqlQuery("SELECT * FROM App " +
                                    "ORDER BY number ASC")

        appCount = allAppsQuery.count()


        allAppsList = allAppsQuery.fetch(appCount)



        template_values = {
            'steps': steps,
            'customs': customs,
            'app': app,
            'allAppsList': allAppsList
            }

        path = os.path.join(os.path.dirname(__file__),'app_base.html')
        self.response.out.write(template.render(path, template_values))



class AboutHandler(webapp.RequestHandler):
    def get(self):
        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/about.html')
        self.response.out.write(template.render(path, template_values))



class GetAppDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_app_data()")
        app = self.request.get('app')
        appsQuery = db.GqlQuery("SELECT * FROM App WHERE appId = :1", app)
        app_to_get = appsQuery.get()

        appId = app

        number = app_to_get.number;
        title = app_to_get.title;
        heroHeader = app_to_get.heroHeader;
        heroCopy = app_to_get.heroCopy;

        my_response = {'number': number, 'title': title, 'heroHeader': heroHeader, 'heroCopy': heroCopy}
#        json = JSON.dumps(my_response)

        self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
        self.response.out.write(json.dumps(my_response))


class GetStepDataHandler(webapp.RequestHandler):
    def get(self):
        logging.info("I'm inside get_step_data()")
        step_header = self.request.get('step_header')
        stepQuery = db.GqlQuery("SELECT * FROM Step WHERE header = :1", step_header)
        step = stepQuery.get()

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
        customQuery = db.GqlQuery("SELECT * FROM Custom WHERE header = :1", custom_header)
        custom = customQuery.get()

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

        allAppsQuery = db.GqlQuery("SELECT * FROM App ORDER BY number ASC")
        allAppsList = allAppsQuery.fetch(allAppsQuery.count())


        currenttime = datetime.utcnow()
        template_values={'currenttime':currenttime, 'allAppsList': allAppsList}
        path = os.path.join(os.path.dirname(__file__),'static_pages/other/setup.html')
        self.response.out.write(template.render(path, template_values))



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
        ('/media', MediaHandler), ('/teaching-android', TeachingHandler), ('/lesson-introduction-to-app-inventor', LPIntroHandler),
        ('/lesson-plan-creating', LPCreatingHandler), ('/lesson-plan-paintpot-and-initial-discussion-of-programming-con', LPConceptsHandler),
        ('/lesson-plan-mobile-apps-and-augmented-real', LPAugmentedHandler), ('/lesson-plan-games', LPGamesHandler),
        ('/iterate-through-a-list', LPIteratingHandler), ('/lesson-plan-user-g', LPUserGenHandler),
        ('/lesson-plan-foreach-iteration-and', LPForeachHandler), ('/persistence-worksheet', LPPersistenceWorksheetHandler),
        ('/persistence-r', LPPersistenceFollowupHandler), ('/functions', LPFunctionsHandler),
	('/helloPurrLesson', HelloPurrHandler),('/paintPotLesson', PaintPotHandler),('/moleMashLesson', MoleMashHandler),('/shooterLesson', ShooterHandler),('/paintPotIntro', PaintPotIntroHandler),('/structure', StructureHandler), ('/appPage', AppPageHandler),('/appInventorIntro', AppInventorIntroHandler),('/loveYouLesson', LoveYouHandler),('/noTextingLesson', NoTextingHandler),('/gpsIntro', GPSHandler),('/androidWhere', AndroidWhereHandler), ('/quizLesson', QuizHandler),('/quizIntro', QuizIntroHandler),('/userGenerated', UserGeneratedHandler),('/noteTakerLesson', NoteTakerHandler),('/broadcastHubLesson', BroadcastHubHandler),
        ('/procedures', LPCodeReuseHandler), ('/deploying-an-app-and-posting-qr-code-on-web', LPQRHandler),
        ('/module1', Module1Handler), ('/module2', Module2Handler), ('/module3', Module3Handler),
        ('/module4', Module4Handler), ('/module5', Module5Handler), ('/module6', Module6Handler),
        ('/module7', Module7Handler), ('/contact', ContactHandler), ('/about', AboutHandler ), ('/book', BookHandler),
        ('/app-architecture', Handler14), ('/engineering-and-debugging', Handler15), ('/variables-1', Handler16),
        ('/animation-3', Handler17), ('/conditionals', Handler18), ('/lists-2', Handler19),
        ('/iteration-2', Handler20), ('/procedures-1', Handler21), ("/databases", Handler22), ("/sensors-1", Handler23),
        ("/apis", Handler24), ('/course-in-a-box_teaching', CourseInABoxHandlerTeaching), ('/media_teaching', MediaHandlerTeaching),
        ('/DeleteApp', DeleteApp), ('/AddStepPage', AddStepRenderer), ('/DeleteStep', DeleteStep), ('/AddCustomPage', AddCustomRenderer),
        ('/projects', BookHandler ), ('/appinventortutorials', BookHandler), ('/get_app_data', GetAppDataHandler),
        ('/get_step_data', GetStepDataHandler), ('/get_custom_data', GetCustomDataHandler), ('/setup', SetupHandler),
	('/IHaveADream', IHaveADreamHandler),('/properties', PropertiesHandler), ('/eventHandlers', EventHandlersHandler),('/quizly',QuizlyHandler),('/conditionalsInfo',ConditionalsInfoHandler)
    ],
    debug=True)




def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()



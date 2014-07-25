import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2 = 'default_guestbook2'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MemberOnePage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('One.html')
        self.response.write(template.render(template_values))


class MemberTwoPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('Two.html')
        self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Guestbook1(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name1',
                                          DEFAULT_GUESTBOOK_NAME1)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class Guestbook2(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name2',
                                          DEFAULT_GUESTBOOK_NAME2)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


class Student(ndb.Model):
    department = ndb.StringProperty(indexed=False)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    student_number = ndb.StringProperty(indexed=False)
    remarks = ndb.StringProperty(indexed=False)

class SuccessPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('student_success.html')
        self.response.write(template.render())

class StudentListHandler(webapp2.RequestHandler):
    def get(self):
        students = Student.query().fetch()
        template_values = {
            "all_students": students,
        }
        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_values))

class StudentNewHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('student_new.html')
        self.response.write(template.render())

    def post(self):
        student = Student()
        student.department = self.request.get('department')
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.student_number = self.request.get('student_number')
        student.remarks = self.request.get('remarks')
        student.put()
        self.redirect('/success')

class StudentView(webapp2.RequestHandler):
    def get(self,s_id):
        
        students = Student.query().fetch()
        s_id = int(s_id)

        values = {
            'all_students': students,
            'id': s_id
        }

 
        template = JINJA_ENVIRONMENT.get_template('student_view.html')
        self.response.write(template.render(values))


class StudentEdit(webapp2.RequestHandler):
    def get(self,s_id):
        
        students = Student.query().fetch()
        s_id = int(s_id)

        values = {
            'all_students': students,
            'id': s_id
        }

 
        template = JINJA_ENVIRONMENT.get_template('student_edit.html')
        self.response.write(template.render(values))


    def post(self, s_id):
        s_id = int(s_id)    
        student = Student.get_by_id(s_id)
        student.department = self.request.get('department')
        student.first_name = self.request.get('first_name')
        student.last_name = self.request.get('last_name')
        student.email = self.request.get('email')
        student.student_number = self.request.get('student_number')
        student.remarks = self.request.get('remarks')
        student.put()
        self.redirect('/success')



class Adviser(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    Title = ndb.StringProperty(indexed=False)
    First_Name = ndb.StringProperty(indexed=False)
    Last_Name = ndb.StringProperty(indexed=False)
    Email = ndb.StringProperty(indexed=False)
    Phone_Number = ndb.StringProperty(indexed=False)
    Department = ndb.StringProperty(indexed=False)

class AdviserNew(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('adviser_new.html')
        self.response.write(template.render())
    
    def post(self):
        adviser = Adviser()
        adviser.Title = self.request.get('Title')
        adviser.First_Name = self.request.get('First_Name')
        adviser.Last_Name = self.request.get('Last_Name')
        adviser.Email = self.request.get('Email')
        adviser.Phone_Number = self.request.get('Phone_Number')
        adviser.Department = self.request.get('Department')
        adviser.put()
        self.redirect('/adviser/success')

class SuccessPass(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('adviser_success.html')
        self.response.write(template.render())

class AdviserList(webapp2.RequestHandler):
    def get(self):

        adviserquery = Adviser.query().fetch()
        template_values ={
            "all_adviserquery" : adviserquery
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_list.html')
        self.response.write(template.render(template_values))

class AdviserView(webapp2.RequestHandler):
    def get(self, advise_id):
        adviserquery = Adviser.query().fetch()
        advise_id = int(advise_id)
        template_values ={
            'id': advise_id,
            'all_adviserquery': adviserquery
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_view.html')
        self.response.write(template.render(template_values))



class AdviserEdit(webapp2.RequestHandler):
    def get(self, advise_id):
        adviserquery = Adviser.query().fetch()
        advise_id = int(advise_id)
        template_values ={
            'id': advise_id,
            'all_adviserquery': adviserquery
        }
        template = JINJA_ENVIRONMENT.get_template('adviser_edit.html')
        self.response.write(template.render(template_values))

    def post(self, advise_id):
        advise_id = int(advise_id)
        adviser = Adviser.get_by_id(advise_id)
        adviser.Title = self.request.get('Title')
        adviser.First_Name = self.request.get('First_Name')
        adviser.Last_Name = self.request.get('Last_Name')
        adviser.Email = self.request.get('Email')
        adviser.Phone_Number = self.request.get('Phone_Number')
        adviser.Department = self.request.get('Department')
        adviser.put()
        self.redirect('/adviser/success')


class Thesis(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    Thesis_title = ndb.StringProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    date1 = ndb.StringProperty(indexed=False)
    schoolyear = ndb.StringProperty(indexed=False)
    status = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class ThesisNew(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
        self.response.write(template.render())
    
    def post(self):
        thesis = Thesis()
        thesis.Thesis_title = self.request.get('Thesis_title')
        thesis.description = self.request.get('description')
        thesis.date1 = self.request.get('date1')
        thesis.schoolyear = self.request.get('schoolyear')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/thesis/success')

class ThesisSuccessPass(webapp2.RequestHandler):
    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('thesis_success.html')
        self.response.write(template.render())

class ThesisList(webapp2.RequestHandler):
    def get(self):

        thesisquery = Thesis.query().order(-Thesis.date).fetch()
        

        values = {
            'thesisquery': thesisquery,
        }


        template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
        self.response.write(template.render(values))

class ThesisView(webapp2.RequestHandler):
    def get(self,thesis_id):
        
        thesisquery = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        values = {
            'thesisquery': thesisquery,
            'id': thesis_id
        }

 
        template = JINJA_ENVIRONMENT.get_template('thesis_view.html')
        self.response.write(template.render(values))

class ThesisEdit(webapp2.RequestHandler):
    def get(self,thesis_id):
        
        thesisquery = Thesis.query().fetch()
        thesis_id = int(thesis_id)

        values = {
            'thesisquery': thesisquery,
            'id': thesis_id
        }

 
        template = JINJA_ENVIRONMENT.get_template('thesis_edit.html')
        self.response.write(template.render(values))

    def post(self, thesis_id):
        thesis_id = int(thesis_id)
        thesis = Thesis.get_by_id(thesis_id)
        thesis.Thesis_title = self.request.get('Thesis_title')
        thesis.description = self.request.get('description')
        thesis.date1 = self.request.get('date1')
        thesis.schoolyear = self.request.get('schoolyear')
        thesis.status = self.request.get('status')
        thesis.put()
        self.redirect('/thesis/success')    
        
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/sign1', Guestbook1),
    ('/sign2', Guestbook2),
    ('/module-1/1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/student/new', StudentNewHandler),
    ('/student/list', StudentListHandler),
    ('/success', SuccessPageHandler),
    ('/student/view/(\d+)', StudentView),
    ('/student/edit/(\d+)', StudentEdit),
    ('/adviser/new', AdviserNew),
    ('/adviser/list', AdviserList),
    ('/adviser/success', SuccessPass),
    ('/adviser/view/(\d+)', AdviserView),
    ('/adviser/edit/(\d+)', AdviserEdit),
    ('/thesis/new', ThesisNew),
    ('/thesis/list', ThesisList),
    ('/thesis/success', ThesisSuccessPass),
    ('/thesis/view/(\d+)', ThesisView),
    ('/thesis/edit/(\d+)', ThesisEdit)
], debug=True)


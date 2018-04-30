#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
import jinja2
import sys

# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class PageHandler(webapp2.RequestHandler):
    def get(self):
        page1 = 'templates%s' % self.request.path
        page = (page1.split(".")[0]).split("/")[1].capitalize()

        if page1 == "templates/":
            template = JINJA_ENVIRONMENT.get_template('templates/index.html')
            self.response.write(template.render({'title': 'Tricia Chua', 'home': 'Home'}))
        else:
            try:
                template = JINJA_ENVIRONMENT.get_template('templates%s' % self.request.path)
                if page == "Index":
                    self.response.write(template.render({'title': 'Tricia Chua', 'home': 'Home'}))
                else:
                    self.response.write(template.render({'title': page}))
            except:
                template = JINJA_ENVIRONMENT.get_template('templates/index.html')
                self.response.write(template.render({'title': '404 Not Found', 'home': 'Returned to Home'}))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/login.html')
        self.response.write(template.render({'title': 'Login'})) 

    def post(self):
        entered_name = self.request.get('username')
        entered_pw = self.request.get('password')

        correct_name = "Colleen"
        correct_pw = "pass"

        if entered_name == correct_name and entered_pw == correct_pw:
            template = JINJA_ENVIRONMENT.get_template('templates/loginsuccess.html')
            self.response.write(template.render({'title': 'Logged In', 'hint': 'You did it. Congrats!'})) 
        else:
            template = JINJA_ENVIRONMENT.get_template('templates/login.html')
            self.response.write(template.render({'title': 'Login', 'hint': 'Bad Credentials. Try again.'})) 

            logging.info("Username: " + entered_name + " || " "Password: " + entered_pw)

        
app = webapp2.WSGIApplication([
    ('/login.html', LoginHandler),
    ('/loginsuccess.html', LoginHandler),
    ('/.*', PageHandler)
], debug=True)

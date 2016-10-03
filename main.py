import webapp2
import jinja2
import os
import hashlib
import hmac
import database
from google.appengine.ext import db


#concatenates this secret string to cookies to make it more secure
secret = "jksdhkjsdhn+787897897987896798" 

#joins the path of current direcotry with template
temp_dir = os.path.join(os.path.dirname(__file__),'templates')

#loads the file in jinja environment from temp_dir path
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(temp_dir),autoescape=True)


def render_str(template,**params):
    t = jinja_env.get_template(template)
    return t.render(params)

#hashes the password. comes handy if someone tries to compromise the database
#there is even secure hashing function using salt, but this will be ok for now
def hash_str(s):            
    return hashlib.sha224(s).hexdigest()

def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

#All the classes below inherits from Handler class
class Handler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        super(Handler, self).__init__(request=None, response=None)
        self.request = request
        self.response = response
        uid = self.read_secure_cookie('user_id')
        self.loged_user =  uid and database.User.get_by_id(int(uid)) 

    # render the general string like hello world
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    # render the string with <html></html> tags
    def render_str(self, template, **params):
        params['user'] = self.loged_user
        t = jinja_env.get_template(template)
        return t.render(params)

        # read the file and pass strig to the previous function
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    # set the cookies when the user logs in
    def set_secure_cookie(self, name, val):
        cookie_val = str(make_secure_val(val))
        self.response.headers.add_header('Set-Cookie','%s=%s; Path=/'%(name, cookie_val))

    # reads the hashes cookie form the browser
    def read_secure_cookie(self,name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # logs the user on and sets cookies
    def login(self,user):
        self.set_secure_cookie('user_id',str(user.key().id()))
    #clears all the cookies if the user logs out
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    #renders the game html
class MainHandler(Handler):
    def get(self):
        usr = self.loged_user
        if usr:
            self.render("game.html", logged_user=usr, 
                        win=usr.win, lose=usr.lose,
                        draw=usr.draw)
        else:
            self.render("game.html", logged_user=usr)
    #updates the scores
    def post(self):
        if self.loged_user:
            code = self.request.get('code')
            print code
            if code == '1':
                self.update_lose()
            elif code == '2':
                self.update_win()
            elif code == '3':
                self.update_draw()

    #updates the number of wins
    def update_win(self):
        self.loged_user.win += 1
        self.loged_user.put()
    #updates the loses
    def update_lose(self):
        self.loged_user.lose += 1
        self.loged_user.put()
    #updates the number of draws
    def update_draw(self):
        self.loged_user.draw += 1
        self.loged_user.put()    


class SinupHandler(Handler):
    def get(self):  #renders the signup html
        self.render("signup.html")

    #gets the data from signup and updates the imported database
    def post(self):
        first_name = self.request.get('fullname')
        username = self.request.get('username')
        password = self.request.get('password')
        if(password and username):
            database.User(full_name = first_name, user_name = username,
                            password = hash_str(password.strip()), win = 0, lose = 0, draw = 0).put()
            self.redirect('/')
        else:
            error = "All fields are required." #there is a print error statement in signup.html
            self.render("signup.html", error = error);

class LoginHandler(Handler):
    def get(self):  #if the user is logged in, redirects to home
        if self.loged_user:
            self.redirect('/')
        else:
            self.render("login.html")
    
    #checks the username and password during login. prompts the user if the data doesn't match with 
    #the data in User database
    def post(self):
        username = self.request.get('username')
        password = hash_str(self.request.get('password'))
        if(password and username):
            usr = database.User.all().filter('user_name =', username).get()
            if usr:
                if  password != usr.password:
                    error = "Password did not match. Try again. "
                    self.render("login.html", error = error);
                else:
                    self.login(usr)
                    self.redirect('/')
            else:
                error = 'Username not found. Please signup first.'
                self.render("login.html", error = error)
        else:
            error = 'Both fields are required.'
            self.render("login.html", error = error)
#logs out the user
class LogoutHandler(Handler):
    def post(self):
        self.logout()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SinupHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
], debug=True)


'''
	index.py 	I shall do nothing but render the interface
'''

import os
import random

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import web2hunter as WH
from preparefood import preparefood, customfood

class MainHandler(webapp.RequestHandler):
	tPath = os.path.join( os.path.dirname (__file__), "templates" )

	def get(self):
		todo = self.request.get('getname')
		
		if (todo == 'true'):
			if (self.request.headers.get('Referer') != None):
				# stop others from stealing your bandwidth
				#if (self.request.headers.get('Referer').find('web2hunter.appspot.com')!=-1):

					# return a possible domain name
				        sessionkey = self.request.get('sessionkey')
					#seedfood = self.request.get('seedfood')
					
					possiblename = WH.genName(sessionkey)

					while (possiblename == ""):
						possiblename = WH.genName(sessionkey)
			
					# lets sanitize the possible name
					# for sometime we get the response header for some reason -
					# Content-Type: text/html; charset=utf-8 Cache-Control: ... blabla
					# well a foo.split()[-1] would help

					# food for javascript + sanitization
					self.response.out.write (possiblename.split()[-1])
				#else:
					#self.response.out.write ("nothing for you");
			else:
				self.response.out.write ("nothing for you");
		else:
			custom = self.request.get('custom')
			
			if custom == 'search':				
				name = self.request.get('name')
				sessionkey, np = customfood(self,name)
				words = name
				newstitle = None
				newslink = None
				newsdesc = None
			else:
				# prepare food
				try:
					sessionkey, words, news, np = preparefood(self)
					newstitle = news[0]
					newslink = news[1]
					newsdesc = news[2]
					words = " ".join(words)
				except Exception:
					sessionkey = None
					words = None
					newstitle = None
					newslink = None
					newsdesc = None
					np = None
			if np:
				self.redirect("/?rnd=", random.random())
			template_values = {
				'sessionkey': sessionkey,
				'words': words,
				'newstitle': newstitle,
				'newslink': newslink,
				'newsdesc': newsdesc,
				}
			# render the template
			outstr = template.render (
				self.tPath + '/index.html', template_values )
	
			self.response.out.write (outstr)
		

def main():
	application = webapp.WSGIApplication( [('/.*',MainHandler)], debug=True )
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
	main()


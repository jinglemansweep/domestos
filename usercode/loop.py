from domestos.helpers import *

def run(self):
	if self.dt.is_new("second"):
		self.logger.info("New Second")
		
	if self.dt.is_new("minute"):
		self.logger.info("New Minute")
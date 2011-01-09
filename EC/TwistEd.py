from functions import gcdinvert

import EC.Montgomery
class TwistEdCurve:
	a=0
	d=0
	g=0
	def __init__(self, a, d, group):
		self.a=(a)%group
		self.d=(d)%group
		self.g=group
	def toMontgomery(self):
		A = 2*(self.a+self.d) * gcdinvert((self.a-self.d)%self.g, self.g)
		B = 4* gcdinvert((self.a-self.d)%self.g, self.g)
		return MontgomeryCurve(A,B,self.g)
	
	def getPoints(self):
		return [(x,y) for x in range(0,self.g) for y in range(0,self.g) if (self.a*x*x+y*y)%self.g == (1 + self.d*x*x*y*y) %self.g]	
	
	def __repr__(self):
		return self.__str__();
	def __str__(self):
		return "E_{F_{%d},%d,%d}"%(self.g, self.a, self.d)


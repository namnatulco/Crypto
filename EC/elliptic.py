from functions import gcdinvert
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

class MontgomeryCurve:
	A=0
	B=0
	g=0
	def __init__(self, A, B, group):
		self.A=(A)%group
		self.B=(B)%group
		self.g=group
	def toTwistEd(self):
		i = gcdinvert(self.B,self.g)
		print self.B
		print i
		return TwistEdCurve((self.A+2)*i,(self.A-2)*i,self.g)
	def getPoints(self):
		r = [(x,y) for x in range(0,self.g) for y in range(0,self.g) if (self.B*y*y)%self.g == (x*x*x+self.A*x*x+x)%self.g]
		r.append((None,None))
		return r

	def __str__(self):
		return "E_{F_{%d},%d,%d}"%(self.g, self.a, self.d)
	def __repr__(self):
		return self.__str__();

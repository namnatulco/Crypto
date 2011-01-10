
def gcdinvert(e,g):
	from functions import gcdinvert as gcdi
	e=e%g
	if not e:
		return 0
	return gcdi(e,g)

class TwistEdCurve:
	a=0
	d=0
	g=0
	def __init__(self, a, d, group):
		self.a=(a)%group
		self.d=(d)%group
		self.g=group
		
	def isPoint(self,tup):
		(x,y)=tup
		return (self.a*x*x+y*y)%self.g == (1 + self.d*x*x*y*y) %self.g

	def getPoints(self):
		return [(x,y) for x in range(0,self.g) for y in range(0,self.g) if self.isPoint((x,y))]
	
	def doublePoint(self,point):
		return self.addPoints(point,point)
	
	def addPoints(self,p1,p2):
		if not self.isPoint(p1) or not self.isPoint(p2):
			return None
		(x1,y1)=p1
		(x2,y2)=p2
		x3 = ((x1*y2+y1*x2)*gcdinvert((1+self.d*x1*x2*y1*y2)%self.g,self.g))%self.g
		y3 = ((y1*y2-self.a*x1*x2)*gcdinvert((1-self.d*x1*x2*y1*y2)%self.g,self.g))%self.g
		assert ((x3,y3) in self.getPoints()), "Error, (%d,%d) is not on this curve. Inputs: %s and %s. Curve: %s"%(x3,y3,p1,p2, self)
		return (x3,y3)

	
	def toMontgomery(self):
		A = 2*(self.a+self.d) * gcdinvert((self.a-self.d)%self.g, self.g)
		B = 4* gcdinvert((self.a-self.d)%self.g, self.g)
		from EC.Montgomery import MontgomeryCurve
		return MontgomeryCurve(A,B,self.g)

	def toMontgomeryPoints(self,points):
		return [self.toMontgomeryPoint(p) for p in points]
		
	def toMontgomeryPoint(self,p):
		if not self.isPoint(p):
			return None
		if p == (0,1):
			return (None,None)
		elif p==(0,-1):
			return (0,0)
		(x,y)=p
		u=(1+y)*gcdinvert((1-y)    %self.g,self.g)%self.g
		v=(1+y)*gcdinvert(((1-y)*x)%self.g,self.g)%self.g
		return (u,v)

	
	def __repr__(self):
		return self.__str__();
	def __str__(self):
		return "E_{F_{%d},%d,%d}"%(self.g, self.a, self.d)

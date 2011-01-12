"""
This file contains a class that describes Montgomery Curves over Finite Fields.
"""

def gcdinvert(e,g):
	from functions import gcdinvert as gcdi
	e=e%g
	return (gcdi(e,g))%g

"""
MontgomeryCurve represents a Montgomery Curve with parameters A and B.
Since this class is restricted to finite fields, the size of this field g is also needed.
Points are represented by tuples of numbers (integers) or a tuple (None, None) for the point at infinity.
"""
class MontgomeryCurve:
	A=0
	B=0
	g=0
	def __init__(self, A, B, g):
		self.A=(A)%g
		self.B=(B)%g
		self.g=g
	
	"""
	Checks if the given point is on this Montgomery curve.
	"""
	def isPoint(self,tup):
		(x,y)=tup
		return ((self.B*y*y)%self.g == (x*x*x+self.A*x*x+x)%self.g) or (x==None and y==None)
	
	"""
	Fetch all the points on this curve in a list.
	"""
	def getPoints(self):
		r = [(x,y) for x in range(0,self.g) for y in range(0,self.g) if self.isPoint((x,y))]
		r.append((None,None))
		return r

	"""
	Create a Twisted Edwards Curve from this Montgomery curve (over the same Finite Field).
	"""
	def toTwistEd(self):
		i = gcdinvert(self.B,self.g)
		from EC.TwistEd import TwistEdCurve
		return TwistEdCurve((self.A+2)*i,(self.A-2)*i,self.g)
	
	"""
	Transform the given list of points to the Twisted Edwards Curve returned by self.toTwistEd().
	"""
	def toTwistEdPoints(self,points):
		return [self.toTwistEdPoint(p) for p in points]
	
	"""
	Transform the given point on the Montgomery Curve such that it is mapped to the corresponding Twisted Edwards Curve.
	"""
	def toTwistEdPoint(self, point):
		(u,v)=point
		if(u ==None and v==None):
			return (0,1)
		elif(u==0 and v==0):
			return (0,(-1)%self.g)
		return ((u*gcdinvert(v,self.g))%self.g, ((u-1)*gcdinvert((u+1)%self.g,self.g))%self.g)
	
	"""
	Perform addition using the given points on this curve.
	"""
	def addPoints(self, p1, p2):
		(x1,y1)=p1
		(x2,y2)=p2
		if x1==x2:
			return None
		l=(y2-y1)*gcdinvert(x2-x1, self.g)
		
		x3 = (self.A*l*l-self.A-x1-x2)%self.g
		y3 = ((2*x1+x2+self.A)*l-self.B*l*l*l-y1)%self.g
		return (x3,y3)
	"""
	Perform doubling on the given point.
	"""
	def doublePoint(self, p):
		(x1,y1)=p
		l=(3*x1^2+2*self.A*x1+1)*gcdinvert((2*self.B*y1)%self.g,self.g)
		x3 = (self.B*l*l-self.A-x1-x1)%self.g
		y3 = ((2*x1+x1+self.A)*l-self.B*l*l*l-y1)%self.g
		return (x3,y3)

	def __str__(self):
		return "E_{F_{%d},%d,%d}"%(self.g, self.A, self.B)
	def __repr__(self):
		return self.__str__();

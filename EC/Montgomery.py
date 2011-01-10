def gcdinvert(e,g):
	from functions import gcdinvert as gcdi
	e=e%g
	if not e:
		return 0
	return (gcdi(e,g))%g
	
class MontgomeryCurve:
	A=0
	B=0
	g=0
	def __init__(self, A, B, group):
		self.A=(A)%group
		self.B=(B)%group
		self.g=group
	
	def isPoint(self,tup):
		(x,y)=tup
		return ((self.B*y*y)%self.g == (x*x*x+self.A*x*x+x)%self.g) or (x==None and y==None)
	
	def getPoints(self):
		r = [(x,y) for x in range(0,self.g) for y in range(0,self.g) if self.isPoint((x,y))]
		r.append((None,None))
		return r

	def toTwistEd(self):
		i = gcdinvert(self.B,self.g)
		from EC.TwistEd import TwistEdCurve
		return TwistEdCurve((self.A+2)*i,(self.A-2)*i,self.g)
	
	def toTwistEdPoints(self,points):
		return [self.toTwistEdPoint(p) for p in points]
	
	def toTwistEdPoint(self, point):
		(u,v)=point
		if(u ==None and v==None):
			return (0,1)
		elif(u==0 and v==0):
			return (0,(-1)%self.g)
		return ((u*gcdinvert(v,self.g))%self.g, ((u-1)*gcdinvert((u+1)%self.g,self.g))%self.g)
	
	def __str__(self):
		return "E_{F_{%d},%d,%d}"%(self.g, self.A, self.B)
	def __repr__(self):
		return self.__str__();

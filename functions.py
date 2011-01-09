"""
This file contains 'extra' functions and generators.
"""


def divisors(n):
	"""
	(fairly) naive generator for divisors of n.
	Generation is incremental.
	"""
	x=1
	while(x<=(n/2)):
		if n%x==0:
			yield x
		x+=1

def primedivisors(n):
	"""
	find primes dividing n, using a naive method for finding primes.
	this is not practical for numbers that aren't smooth.
	"""
	primelist=[2]
	x=1
	if(n%2==0):
		yield 2
	import math
	end=int(math.ceil(math.sqrt(n)))
	while(x<= end):
		x+=2
		#is x a prime?
		if not True in [x%y==0 for y in primelist]:
			primelist.append(x)
			#does x divide n?
			if(n%x==0):
				yield x

def primepowerdivisors(n):
	"""
	Generate the highest prime powers that divide n.
	Uses the naive generator primedivisors(n).
	"""
	for p in primedivisors(n):
		value=n
		exponent=0
		while(value%p==0):
			value/=p
			exponent+=1
		yield (p**exponent)

def Xgcd(a,b):
	"""
	Performs the extended GCD algorithm and returns (gcd,u,v) such that:
	gcd=u*a + v*b
	"""
	swap=False
	if(b>a):
		swap=a
		a=b
		b=swap
	a=(a, 1, 0)
	b=(b, 0, 1)
	while (b[0]):
		x = (a[0]-(a[0]%b[0]))/b[0] #integer division
		c=(a[0]-x*b[0],a[1]-x*b[1],a[2]-x*b[2])
		a=b
		b=c
	if not swap:
		return (a[0],a[1],a[2])
	else:
		return (a[0],a[2],a[1])

def crt(congruences, N=None):
	"""
	Simple algorithm to compute CRT given a list of tuples as input.
	Optional argument N should be the product of all congruence[i][1] if given.

	This function solves the equation system:
	x=congruences[0][0] mod congruences[0][1]
	x=congruences[1][0] mod congruences[1][1]
	...
	x=congruences[i][0] mod congruences[i][1]
	and returns x.
	"""
	if not N:
		import operator
		#compute N with cool functional code
		N = reduce(operator.mul,[right for (left,right) in congruences])
	result=0
	for item in congruences:
		t=N/item[1]
		(gcd,u,v)=Xgcd(t,item[1])
		#gcd=u*t + v*item[1]
		x=item[0]*(u*t)
		result+=x
	return result

#compute x such that x*element=1 mod groupsize if such an x exists
def gcdinvert(element,groupsize):
	a=(groupsize, 1, 0)
	b=(element, 0, 1)
	while (b[0]):
		x = (a[0]-(a[0]%b[0]))/b[0] #integer division
		c=(a[0]-x*b[0],a[1]-x*b[1],a[2]-x*b[2])
		a=b
		b=c
	if(a[0]!=1): #multiplicative inverse exists iff gcd = 1
		return None
	else:
		return a[2]

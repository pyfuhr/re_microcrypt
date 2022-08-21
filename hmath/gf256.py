class _GF256:
	base_poly = 283
	def __init__(self, n):
		self.n = n

	def __add__(self, other):
		return self.__class__(self.n ^ other.n)

	def __sub__(self, other):
		return self + other

	def __mul__(self, other):
		a, b, c = self.n, other.n, 0
		for i in range(8):
			c ^= (a & 1) * b
			b = (b << 1) ^ ((b >> 7) * self.base_poly)
			a >>= 1
		return self.__class__(c)

	def __pow__(self, other):
		power = self.__class__(1)
		for i in range(other.n):
			power *= self
		return power

	def __int__(self):
		return self.n

	def __str__(self):
		return bin(self.n)[2:]

class GF256(_GF256):
	def __init__(self, n):
		self.n = n

	def __mul__(self, other):
		if self.n == 0 or other.n == 0:
			return self.__class__(0)
		c = _exptbl[(_logtbl[self.n - 1] + _logtbl[other.n - 1]) % 255]
		return self.__class__(c)

	def __invert__(self):
		if self.n == 0: raise ZeroDivisionError()
		c = _exptbl[(-_logtbl[self.n - 1]) % 255]
		return self.__class__(c)

	def __truediv__(self, other):
		return self * ~other

_exptbl = [int(_GF256(3) ** _GF256(i)) for i in range(255)]
_logtbl = [log for log, exp in sorted(enumerate(_exptbl),
									key=lambda x: x[1])]
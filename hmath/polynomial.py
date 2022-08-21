#hmath module by pyfuhr

class Polynomial:
	def __init__(self, num, trunc=False):
		"""
		Polynomial(num) -> return Polynom object
		For example
		Polynomial((3., 4., 6., 0., 1.6)) is equal
		  4    3    2
		3x + 4x + 6x + 1.6

		WARNING
		Polynom class work only with natural number, because
		when computer working with non-integer or negative number
		you can get math error
		"""
		self._poly = []
		first = True
		for item in num:
			# TODO перевернуть
			if trunc and first and item == 0:
				pass
			else:
				first = False
				self._poly.append(item)

	def _getitemsr(self):
		ret = self._poly.copy()
		ret.reverse()
		return ret

	def _getitems(self):
		return self._poly.copy()

	def __len__(self):
		return len(self._poly)

	def __getitem__(self, index):
		if 0 <= index < len(self._poly): return self._poly[index]
		if index < 0 and -index <= len(self._poly): return self._poly[index]
		else: return 0

	def __setitem__(self, index, value):
		if 0 <= index < len(self._poly):  self._poly[index] = value
		if index < 0 and -index <= len(self._poly): self._poly[index] = value
		else: return -1

	def __add__(self, other):
		ret = []
		mx = max(len(self), len(other))
		for index in range(mx):
			ret.append(self[index-mx]+other[index-mx])
		return self.__class__(ret, trunc=True)

	def __xor__(self, other):
		ret = []
		mx = max(len(self), len(other))
		for index in range(mx):
			ret.append(self[index-mx]^other[index-mx])
		return self.__class__(ret, trunc=True)

	def __sub__(self, other):
		ret = []
		mx = max(len(self), len(other))
		for index in range(mx):
			ret.append(self[index-mx]-other[index-mx])
		return self.__class__(ret, trunc=True)

	def __mul__(self, other):
		if type(other) in (int, float):
			c = self._getitems()
			c = list(map(lambda x: x*other, c))
			return self.__class__(c)
		else:
			a, b = self, other
			c = [0 for i in range(len(a)+len(b)-1)]
			for indexa, itema in enumerate(a._getitemsr()):
				for indexb, itemb in enumerate(b._getitemsr()):
					c[indexa+indexb] += itema*itemb
			c.reverse()
			return self.__class__(c)

	def __divmod__(self, other):
		a = self
		b = other
		c = a
		d = self.__class__([])
		for i in range(len(a)-len(b)+1):
			d = d << 1
			if not self.__can_del(c, b):
				continue
			x = b << (len(c) - len(b))
			d[-1] = c[0] / b[0]
			x = x * (c[0] / b[0])
			c = c - x
		return d, c

	def __floordiv__(self, other):
		return divmod(self, other)[0]

	def __mod__(self, other):
		return divmod(self, other)[1]

	def __pow__(self, power, modulo=None):
		if not modulo is None:
			raise Exception('unsuported operation a**x(mod n)')
		if type(power) != int:
			raise NotImplementedError('just int power')
		if power < 0:
			raise NotImplementedError('just greater than 0 power')
		if power == 0:
			return self.__class__((0, ))
		else:
			ret = self
			for i in range(power-1):
				ret = ret * self
		return ret

	def __str__(self):
		ret = ''
		for index, item in enumerate(self._poly):
			if item == 0:
				continue
			if index < len(self._poly)-2:
				ret += '(' + str(item) + 'x^' + str(len(self._poly) - index - 1) + ')+'
			elif index == len(self._poly)-2:
				ret += '(' + str(item) + 'x)+'
			else:
				ret += '(' + str(item) + ')+'
		if ret:
			return ret[:-1]
		return '0'

	@staticmethod
	def __can_del(dvd, dvs):
		a = [True, True]
		mx = max(len(dvd), len(dvs))
		if dvd[-mx] == 0:
			a[0] = False
		if dvs[-mx] == 0:
			a[1] = False
		if not a[0] and a[1]:
			return False
		return True

	def __lshift__(self, other:int):
		a = self._getitems()
		for i in range(other):
			a.append(0)
		return self.__class__(a)
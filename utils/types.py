class BitVector:
	def __init__(self, byte_len:int=1):
		self.__vector = bytearray(b'\x00'*byte_len)

	def __getitem__(self, item:int):
		n = item//8
		i = item%8
		return (self.__vector[n]&(1<<i))!=0

	def __setitem__(self, key:int, value:bool):
		n = key//8
		i = key%8
		if value:
			self.__vector[n] |= (1<<i)
		else:
			self.__vector[n] &= ~(1<<i)

	def inverse(self, item:int):
		n = item//8
		i = item%8
		self.__vector[n] ^= (1<<i)

	def set_memory(self, byte_view:bytes):
		self.__vector = bytearray(byte_view)

	def get_memory(self):
		return self.__vector

	def __str__(self):
		return str(self.__vector)
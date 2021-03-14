class camlevels:
	def __init__(self,symbol,date,cpt_relationship,bc,pivot,tc,cpr_width,l5,l4,l3,l2,l1,h1,h2,h3,h4,h5):
		self.symbol=symbol
		self.date=date
		self.cpt_relationship=cpt_relationship
		self.bc=bc
		self.pivot=pivot
		self.tc=tc
		self.cpr_width=cpr_width
		self.L5=l5
		self.L4=l4
		self.L3=l3
		self.L2=l2
		self.L1=l1
		self.H1=h1
		self.H2=h2
		self.H3=h3
		self.H4=h4
		self.H5=h5

	def printRecord(self):
		print("Cam levels for symbol  ", self.symbol , " are : ")
		print(self.date)
		print(self.cpt_relationship)
		print(self.bc)
		print(self.pivot)
		print(self.tc)
		print(self.cpr_width)
		print(self.L5)
		print(self.L4)
		print(self.L3)
		print(self.L2)
		print(self.L1)
		print(self.H1)
		print(self.H2)
		print(self.H3)
		print(self.H4)
		print(self.H5)


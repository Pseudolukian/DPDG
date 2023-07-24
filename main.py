from fakegenerator import FakeGenerator
from exporter import Exporter
f_g = FakeGenerator(sex= "F", country="USA", age=[30,70])
gen = f_g.generator()
exp = Exporter(data = gen)

print(exp.xls())
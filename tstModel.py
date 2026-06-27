
from model.model import Model

mymdl = Model()

mymdl.buildGraph(5,"2016-01-03","2016-01-30")

print(mymdl.getGraphDetails())
from processor import Processor
from parser import Parser


proc = Processor()
pars = Parser(processor=proc, file_path="program.txt")
pars.run()
proc.run()

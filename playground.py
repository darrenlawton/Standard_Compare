# https://medium.com/@_chriz_/development-of-a-structure-aware-pdf-parser-7285f3fe41a9
# Raw Data > Parsing > Modelling > Application

'''
class StructuredDocument:
  metadata: dict
  sections: List[Section]
class Section:
  content:  TextElement
  children: List[Section]
  level:    int0
class TextElement:
  text:     LTTextContainer # the extracted paragraph from pdfminer
  style:    Style
'''

# 'artefacts/APS_113_January_2013.pdf'

from pdfstructure.hierarchy.parser import HierarchyParser
from pdfstructure.source import FileSource
from pdfstructure.printer import PrettyStringPrinter

parser = HierarchyParser()

# specify source (that implements source.read())s
path = 'artefacts/reduced_APS_113_January_2013.pdf'
source = FileSource(path)

# analyse document and parse as nested data structure
document = parser.parse_pdf(source)

pretty_string_printer = PrettyStringPrinter()
pretty_string = pretty_string_printer.print(document)
print(pretty_string)
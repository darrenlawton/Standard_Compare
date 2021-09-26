# https://medium.com/@_chriz_/development-of-a-structure-aware-pdf-parser-7285f3fe41a9
# Raw Data > Parsing > Modelling > Application

# 'artefacts/APS_113_January_2013.pdf'

from pdfminer import high_level

print(high_level.extract_text('artefacts/APS_113_January_2013.pdf'))


from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
import re, unicodedata

for page_layout in extract_pages(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', laparams=LAParams(line_margin=0.03), page_numbers=[2,3,4,5]):
    for element in page_layout:
        print(element)
        # if isinstance(element, LTTextContainer):
        #     page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))
        #     content = re.sub(r"\d+", "", element.get_text().replace(".", ""))
        #
        #     print(f"content: {content}, page {page_number}")
        #
        #     check = element.get_text().split(".")
        #     print([unicodedata.normalize("NFKD", x) for x in check])

'''
1) determine boundaries for header and footers (noting, footer boundary more critical)
    - using coordinates, select candidate text boxes (with values) 
    - then check for similarity against surrounding pages to confirm header and footer
    - return y boundaries for "in text" 
2) parse from point where "table of contents" begins
    - will need to do some cleaning using regex  here
'''
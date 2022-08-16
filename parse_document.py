from queue import Empty
import re
import unicodedata
from difflib import SequenceMatcher

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer

from margin_analysis import get_margins

# global parameters
TOC_TOCKEN = 'table of contents'
LINE_MARGIN = 0.025
SIMILARITY_THRESHOLD = 0.8


def validate_string():
    return None

'''
Parse table of contents pages

Args:
    param1 (str): file path string
    param2 (list): page number/s for table of contents
Returns:
    dict: key is page number, and value is processed topic string
 
'''
def parse_contents_page(pdf_file, content_pages: list):
    contents = {}

    # Get header and footer boundaries
    margins = get_margins(pdf_file, content_pages[0])

    # Parse contents page, and extract topic and page number
    for page_layout in extract_pages(pdf_file=pdf_file, laparams=LAParams(line_margin=LINE_MARGIN),
                                     page_numbers=content_pages):
        content = ''
        for element in page_layout:
            if margins['header'] > element.y0 > margins['footer'] \
                    and isinstance(element, LTTextContainer) and element.get_text().strip() != ""\
                    and SequenceMatcher(None, TOC_TOCKEN, element.get_text().strip().lower()).ratio() \
                    < SIMILARITY_THRESHOLD:

                check_list = [unicodedata.normalize("NFKD", x).strip() for x in
                              element.get_text().strip().split(".") if x != '']

                # Remove special characters
                content = content + re.sub('[^A-Za-z]+', "", element.get_text().replace(".", ""))
                page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))

                # Assess multi line topics
                if page_number:
                    contents[page_number[-1]] = content
                    content = '' 

                #print("{} on {}".format(content, page_number))
    
    return contents

#print(parse_contents_page(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1]))
#print(parse_contents_page(pdf_file='artefacts/rbnz_tableofcontents.pdf', content_pages=[0,1]))
#parse_contents_page(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])

'''

Args:
    param1 (str): file path string
    param2 (list): page number/s for table of contents
Returns:
 
'''
def parse_document(pdf_file, content_pages: list):

    toc_dict = parse_contents_page(pdf_file, content_pages)

    for k, v in toc_dict.items():
        print(k)

    return None



parse_document(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1])
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
import re
from margin_analysis import get_margins

# global parameters
line_margin=0.025

'''
2) parse from point where "table of contents" begins
    - will need to do some cleaning using regex  here
'''


def parse_contents(pdf_file, content_pages: list):
    # Get header and footer boundaries, decrement page number by one
    margins = get_margins(pdf_file, content_pages[0])

    for page_layout in extract_pages(pdf_file=pdf_file, laparams=LAParams(line_margin=line_margin), page_numbers=content_pages):
        for element in page_layout:
            if margins['header'] > element.y0 > margins['footer']\
                    and isinstance(element, LTTextContainer) and element.get_text().strip() != "":
                print(element)
    # if isinstance(element, LTTextContainer):
    #     page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))
    #     content = re.sub(r"\d+", "", element.get_text().replace(".", ""))
    #
    #     print(f"content: {content}, page {page_number}")
    #
    #     check = element.get_text().split(".")
    #     print([unicodedata.normalize("NFKD", x) for x in check])


parse_contents(pdf_file='artefacts/reduced_APS_113_January_2013.pdf',  content_pages=[1])
#parse_contents(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])
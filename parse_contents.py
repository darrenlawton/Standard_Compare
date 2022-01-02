import re
import unicodedata
from difflib import SequenceMatcher

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer

from margin_analysis import get_margins

# global parameters
toc_token = 'table of contents'
line_margin = 0.025
similarity_threshold = 0.8


def validate_string():
    return None


def parse_contents(pdf_file, content_pages: list):
    contexts = {}

    # Get header and footer boundaries
    margins = get_margins(pdf_file, content_pages[0])

    for page_layout in extract_pages(pdf_file=pdf_file, laparams=LAParams(line_margin=line_margin),
                                     page_numbers=content_pages):
        multi_line = False
        for element in page_layout:
            if margins['header'] > element.y0 > margins['footer'] \
                    and isinstance(element, LTTextContainer) and element.get_text().strip() != ""\
                    and SequenceMatcher(None, toc_token, element.get_text().strip().lower()).ratio() \
                    < similarity_threshold:

                check_list = [unicodedata.normalize("NFKD", x).strip() for x in
                              element.get_text().strip().split(".") if x != '']

                content = re.sub(r"\d+", "", element.get_text().replace(".", ""))
                page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))



parse_contents(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1])
#parse_contents(pdf_file='artefacts/rbnz_tableofcontents.pdf', content_pages=[0,1])
#parse_contents(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])

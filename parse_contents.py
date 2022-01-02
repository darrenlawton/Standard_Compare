import re
from difflib import SequenceMatcher

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer

from margin_analysis import get_margins

# global parameters
toc_token = 'table of contents'
line_margin = 0.025
similarity_threshold = 0.8

'''
2) parse from point where "table of contents" begins
    - will need to do some cleaning using regex  here
'''


def parse_contents(pdf_file, content_pages: list):
    # Get header and footer boundaries, decrement page number by one
    margins = get_margins(pdf_file, content_pages[0])

    for page_layout in extract_pages(pdf_file=pdf_file, laparams=LAParams(line_margin=line_margin),
                                     page_numbers=content_pages):
        for element in page_layout:
            if margins['header'] > element.y0 > margins['footer'] \
                    and isinstance(element, LTTextContainer) and element.get_text().strip() != ""\
                    and SequenceMatcher(None, toc_token, element.get_text().strip().lower()).ratio() \
                    < similarity_threshold:
                page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))
                content = re.sub(r"\d+", "", element.get_text().replace(".", ""))
                print(f"content: {content}, page {page_number}")

    #     check = element.get_text().split(".")
    #     print([unicodedata.normalize("NFKD", x) for x in check])


#parse_contents(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1])
parse_contents(pdf_file='artefacts/rbnz_tableofcontents.pdf', content_pages=[0,1])
# parse_contents(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])

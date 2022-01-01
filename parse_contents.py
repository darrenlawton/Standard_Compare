from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
import re
from difflib import SequenceMatcher

# for page_layout in extract_pages(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', laparams=LAParams(line_margin=0.03), page_numbers=[2,3,4,5]):
#    for element in page_layout:
#        print(element)
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


def calc_similarity(target_text, page_data):
    score = 0
    for text in page_data:
        score += SequenceMatcher(None, target_text, text).ratio()
    return score


def assess_candidates(candidates, page_number, page_layouts):
    """
    Takes in a list of y coordinates (candidates), the target page number and surrounding page data
    Returns y coordinate that captures the header or footer
    """
    scores = []
    for candidate in candidates:
        page_data = []
        target_text = None
        for page, elements in page_layouts.items():
            for element in elements:
                # By matching on y coordinate, implicitly ensures geometric similarity
                if element.y0 == candidate:
                    if page == page_number:
                        target_text = re.sub(r'\d', '@', element.get_text())
                    else: page_data.append(re.sub(r'\d', '@', element.get_text()))
        scores.append(calc_similarity(target_text, page_data))
    return candidates[scores.index(max(scores))]


def get_header_footer(pdf_file, page_number, line_margin=0.03):
    """
    Takes in a pdf file path and page number, and returns the y boundaries of any header and footer as a dict
    Implementing https://www.hpl.hp.com/techreports/2002/HPL-2002-129.pdf
    """
    n_neighbours = 8

    # Determine numbers of pages in document to set min and max pages
    pdf = open(pdf_file, 'rb')
    parser = PDFParser(pdf)
    document = PDFDocument(parser)
    n_pages = resolve1(document.catalog['Pages'])['Count']

    min_page = max(page_number - n_neighbours, 0)
    max_page = min(page_number + n_neighbours, n_pages)

    # Extract elements for each page in relevant range, and store in dictionary
    dict_page_layout = dict()
    for page in range(min_page, max_page):
        elements = []
        for page_layout in extract_pages(pdf_file='artefacts/reduced_APS_113_January_2013.pdf',
                                         laparams=LAParams(line_margin=line_margin),
                                         page_numbers=[page]):
            for element in page_layout:
                if isinstance(element, LTTextContainer) and element.get_text().strip() != "":
                    elements.append(element)
        if elements is not None: dict_page_layout[page] = elements

    # Get header and footer candidates from input page
    y0_set = list(map(lambda elem: elem.y0, dict_page_layout[page_number]))
    y0_set.sort(reverse=True)
    header_candidates = y0_set[0:2]
    footer_candidates = y0_set[len(y0_set) - 2:len(y0_set)]

    # Determine header boundary
    header_boundary: float = assess_candidates(header_candidates, page_number, dict_page_layout)
    # Determine footer boundary
    footer_boundary: float = assess_candidates(footer_candidates, page_number, dict_page_layout)

    return {"Header": header_boundary, "Footer": footer_boundary}


print(get_header_footer(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', page_number=2))

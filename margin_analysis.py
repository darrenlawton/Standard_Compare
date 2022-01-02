import re
from difflib import SequenceMatcher

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.pdfparser import PDFParser

# global parameters
similarity_threshold = 0.8
n_neighbours = 8


def calc_similarity(target_text, page_data):
    score = []
    for text in page_data:
        score.append(SequenceMatcher(None, target_text.strip(), text.strip()).ratio())
    return sum(score) / (len(score) or 1)


def assess_candidates(candidates, page_number, page_layouts, header_flag):
    """
    Takes in a list of y and x coordinates (candidates), the target page number and surrounding page data
    Returns coordinates that captures the header or footer
    """
    scores = []

    # if header, then reverse order of candidates because if equal score we'd want the lowest boundary
    if header_flag:
        candidates.reverse()

    for candidate in candidates:
        page_data = []
        target_text = None
        for page, elements in page_layouts.items():
            for element in elements:
                # By matching on starting coordinate, implicitly ensures geometric similarity
                if element.y0 == candidate[0] and element.x0 == candidate[1]:
                    if page == page_number:
                        target_text = re.sub(r'\d', '@', element.get_text())
                    else:
                        page_data.append(re.sub(r'\d', '@', element.get_text()))
        scores.append(calc_similarity(target_text, page_data))

    # Assess against threshold to determine if actually a header or footer
    if max(scores) < similarity_threshold and header_flag:
        return max(candidates)
    elif max(scores) < similarity_threshold and header_flag:
        return min(candidates)
    else:
        return candidates[scores.index(max(scores))]


def get_margins(pdf_file, page_number, line_margin=0.025):
    """
    Takes in a pdf file path and page number, and returns the y boundaries of any header and footer as a dict
    Implementing https://www.hpl.hp.com/techreports/2002/HPL-2002-129.pdf
    """
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
        for page_layout in extract_pages(pdf_file=pdf_file,
                                         laparams=LAParams(line_margin=line_margin),
                                         page_numbers=[page]):
            for element in page_layout:
                if isinstance(element, LTTextContainer) and element.get_text().strip() != "":
                    elements.append(element)
        if elements is not None: dict_page_layout[page] = elements

    # Get header and footer candidates from input page
    coord_list = sorted(list(map(lambda elem: [elem.y0, elem.x0], dict_page_layout[page_number])),
                        key=lambda y: y[0], reverse=True)

    header_candidates = coord_list[0:3]
    footer_candidates = coord_list[len(coord_list) - 3:len(coord_list)]

    # Determine header boundary
    header_boundary: float = assess_candidates(header_candidates, page_number, dict_page_layout, True)[0]
    # Determine footer boundary
    footer_boundary: float = assess_candidates(footer_candidates, page_number, dict_page_layout, False)[0]

    return {"header": header_boundary, "footer": footer_boundary}

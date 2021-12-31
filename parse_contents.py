from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import resolve1
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
import re, unicodedata

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


def header_footer(pdf_file, page_number, line_margin=0.03):
    '''
    Takes in a pdf file path and page number, and returns the y boundaries of any header and footer as a dict
    Implementing https://www.hpl.hp.com/techreports/2002/HPL-2002-129.pdf
    '''
    n_neighbours = 8

    # Determine numbers of pages in document to set min and max pages
    pdf = open(pdf_file, 'rb')
    parser = PDFParser(pdf)
    document = PDFDocument(parser)
    n_pages = resolve1(document.catalog['Pages'])['Count']

    min_page = max(page_number - n_neighbours, 1)
    max_page = min(page_number + n_neighbours, n_pages)

    # Extract elements for each page in relevant range, and store in dictionary
    dict_page_layout = dict()
    for page in range(min_page, max_page + 1):
        elements = []
        for page_layout in extract_pages(pdf_file='artefacts/reduced_APS_113_January_2013.pdf',
                                    laparams=LAParams(line_margin=line_margin),
                                    page_numbers=[page]):
            for element in page_layout:
                elements.append(element)
        if elements is not None: dict_page_layout[page] = elements

    # Get header and footer candidates from input page
    set_y0 = list(map(lambda elem: elem.x0, dict_page_layout[page_number]))

    return {"Header": None, "Footer": None}


header_footer(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', page_number=2)

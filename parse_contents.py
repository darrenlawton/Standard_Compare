from queue import Empty
import re
import unicodedata
from difflib import SequenceMatcher

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer

from margin_analysis import get_margins

# global parameters
toc_key_words = ['table of contents', 'appendix', 'attachments']
line_margin = 0.025
similarity_threshold = 0.9


def is_key_word(check_word):
    key_word_found = [word for word in toc_key_words
                      if SequenceMatcher(None, word, check_word.strip().lower()).ratio() >= similarity_threshold]
    return len(key_word_found) > 0


def validate_row(row_list, row_string):
    content_chars = re.sub(r'\d+', '', row_string)
    content_nums = re.findall(r'\b\d+\b', row_string)
    if len(row_list) == 2:
        content = row_list[0]
        page_number = row_list[1]
    elif len(row_list) == 1:
        content = row_list[0]
        page_number = None

    return content, page_number


<<<<<<< HEAD
def parse_contents_page(pdf_file, content_pages: list):
    contents = {}
=======
def parse_contents(pdf_file, content_pages: list):
    contents = {}  # Dictionary where key is subject, and value is page number
>>>>>>> bc059d069bacbfad5e00222903a37e74ed2a9843

    # Get header and footer boundaries
    margins = get_margins(pdf_file, content_pages[0])

    # Parse contents page, and extract topic and page number
    for page_layout in extract_pages(pdf_file=pdf_file, laparams=LAParams(line_margin=line_margin),
                                     page_numbers=content_pages):
<<<<<<< HEAD
        content = ''
=======
        traversing_content = ''
>>>>>>> bc059d069bacbfad5e00222903a37e74ed2a9843
        for element in page_layout:
            if margins['header'] > element.y0 > margins['footer'] \
                    and isinstance(element, LTTextContainer) and element.get_text().strip() != '' \
                    and not is_key_word(element.get_text()):
                # Want to validate the topic and page here:
                # One topic (that with consistency) and one page
                # No page number, but not a genuine topic (e.g. appendi x) -> will filter out above
                # No page number, because goes to next line
                row_list = [unicodedata.normalize('NFKD', x).strip() for x in
                            element.get_text().strip().split('.') if x != '']
                row_string = element.get_text().replace('.', '')

                content, page_number = validate_row(row_list, row_string)
                traversing_content = traversing_content + ' ' + content

                if page_number is not None:
                    contents[traversing_content.strip()] = page_number
                    traversing_content = '' # Reset concatenation

<<<<<<< HEAD
                # Remove special characters
                content = content + re.sub('[^A-Za-z]+', "", element.get_text().replace(".", ""))
                page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))
=======
    return contents
>>>>>>> bc059d069bacbfad5e00222903a37e74ed2a9843

                # Assess multi line topics
                if page_number:
                    contents[page_number[-1]] = content
                    content = '' 

                #print("{} on {}".format(content, page_number))
    
    return contents

<<<<<<< HEAD
#parse_contents_page(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1])
parse_contents_page(pdf_file='artefacts/rbnz_tableofcontents.pdf', content_pages=[0,1])
#parse_contents_page(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])
=======
# parse_contents(pdf_file='artefacts/reduced_APS_113_January_2013.pdf', content_pages=[1])
# parse_contents(pdf_file='artefacts/rbnz_tableofcontents.pdf', content_pages=[0,1])
# parse_contents(pdf_file='artefacts/boe_test_doc.pdf',  content_pages=[2])
>>>>>>> bc059d069bacbfad5e00222903a37e74ed2a9843

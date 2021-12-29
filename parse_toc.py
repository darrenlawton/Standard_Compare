from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTTextContainer
import re

for page_layout in extract_pages(pdf_file='artefacts/tableofcontents.pdf', laparams=LAParams(line_margin=0.03)):
    for element in page_layout:
        if isinstance(element, LTTextContainer):
            page_number = re.findall(r'\b\d+\b', element.get_text().replace(".", ""))
            content = re.sub(r"\d+", "", element.get_text().replace(".", ""))

            print(f"content: {content}, page {page_number}")


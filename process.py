import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

data = 'dataset/Catalano2001_Chapter_TheBitSecurityOfPaillierSEncry.pdf'


def pdf2str(filepath: str) -> str:
    with open(filepath, 'rb') as fp:
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.

        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)

    return retstr.getvalue()


words = word_tokenize(pdf2str(data))
words = [word.lower() for word in words]
stop_words = set(stopwords.words('english'))
stop_words.add(',')
stop_words.add('.')
stop_words.add('(')
stop_words.add(')')
words = [word for word in words if word not in stop_words]
counts = Counter(words)
print(counts)

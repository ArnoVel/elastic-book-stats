import PyPDF2 as ppdf
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from elasticsearch import Elasticsearch

from utils import time_function, _pprint

### FOR NOW:
## Can iterate over dirs & files => get all books w/ type
## Can extract each page from each book == > get a string
## NEXT STEP: put a string or a JSON with numpages, pagenum & etc

## old PyPDF2, which doesn't work
# def _read_pdf(path_to_pdf):
#     _fp = open(path_to_pdf, 'rb')
#     _pdf_reader = ppdf.PdfFileReader(_fp)
#
#     return _pdf_reader


def _read_pdf(pdf_path):
    _fp = open(pdf_path, 'rb')

    _doc, _parser = PDFDocument(), PDFParser(_fp)

    _parser.set_document(_doc)
    _doc.set_parser(_parser) ; _doc.initialize('')

    _rsc_manag = PDFResourceManager() ; _la_params = LAParams()
    _la_params.char_margin, _la_params.word_margin = 1.0, 1.0

    _device = PDFPageAggregator(_rsc_manag, laparams=_la_params)
    _interpreter = PDFPageInterpreter(_rsc_manag, _device)

    return _doc, _interpreter, _device

def _iterate_dirs(dir_path):
    ''' scans for every dir, and all files in each dir
        returns all files as list, dir name as str.
        In short, we'll return all dir_path/dirname/fn1
        by returning 'dirname' as str & [fn1, fn2, fn3, ... ] as list
    '''
    for dir_entry in os.scandir(dir_path):
        if dir_entry.is_dir():
            contents = [ sub_entry.name for sub_entry in os.scandir(dir_entry.path) if sub_entry.is_file()]
            yield dir_entry.name, contents

def _get_all_pdfs(start=0, max_num=None):
    ''' assumes a ./data/pdf/ structure & pdf files in subfolders
    '''
    break_flag = False ; count = 0
    curr_path = os.path.dirname(os.path.realpath(__file__)) # careful, no / at end
    dirpath = curr_path + '/data/pdf/'
    for dname, contents in _iterate_dirs(dirpath):
        for pdf_name in contents:
            if count >= start:
                pdf_type = dname
                pdf_path = dirpath + dname + '/' + pdf_name
                if max_num is not None and count < max_num:
                    yield pdf_name, pdf_type, pdf_path
                elif max_num is None:
                    yield pdf_name, pdf_type, pdf_path
                else:
                    break_flag = True
                    break
            else:
                pass
            count += 1
        if break_flag:
            break

def _display_string(num):
    return num * '-=-'


def _print_page_header(idx):
    print(_display_string(20))
    print( _display_string(10) + f'  Page #{idx}  ' + _display_string(10) )

def _print_book_header(name):
    print(_display_string(20))
    print( _display_string(10) + f'  Book {name}  ' + _display_string(10) )

def is_pdfminer_text(layout_object):
    return (isinstance(layout_object, LTTextBox) or
            isinstance(layout_object, LTTextLine))

def _concat_page(layout):
    page_text = ''
    for _obj in layout:
        if is_pdfminer_text(_obj):
            page_text += _obj.get_text()
    return page_text

def _iterate_pages_as_str(doc, interpreter, device):
    ''' takes a pdfminer object and generates each page as a string
        no option to only iterate starting at `start` and stopping at `stop` yet..
    '''

    for i, page in enumerate(doc.get_pages()):

        interpreter.process_page(page) ; layout = device.get_result()
        yield i, _concat_page(layout)

def _get_author(doc, interpreter, device, end_str='\n', give_numpages=False):
    ''' finds where substring 'author' is first mentioned, and gives
        the appropriate sentence.
        Useful for an approximate notion of what the author is.
    '''
    for i, page in _iterate_pages_as_str(doc, interpreter, device):
        _author_pos = page.lower().find('author')

        if _author_pos != -1:
            stop = page.find(end_str, _author_pos)
            _author_str = page[_author_pos:stop]
            # cleanup if it's a 'author: xxxxxx' type string
            _author_str = _author_str if not ':' in _author_str else _author_str[_author_str.find(':')+1:]
            return _author_str

    else:
        return None

def _get_numpages(path_to_pdf):
    ''' as using pdfminer is too slow to get numpages,
        we use PyPDF2 under the hood to count using the base func
    '''
    _fp = open(path_to_pdf, 'rb')
    _pdf_reader = ppdf.PdfFileReader(_fp)
    return _pdf_reader.numPages

@time_function
def _pdf_to_json(pdf_name, pdf_type, pdf_path):
    ''' puts the whole pdf into a json with:
        _pages : { num: page_str for num,page_str in all_pages}
        _title : title_str
        _author_str : _get_author(pdf)
        _num_pages : _get_numpages(pdf_path)
    '''
    _doc, _interpreter, _device = _read_pdf(pdf_path)
    _json = {}
    _json['_author_str'] = _get_author(_doc, _interpreter, _device).replace('\t', ' ')
    _json['_num_pages'] = _get_numpages(pdf_path)
    _json['_book_type'] = pdf_type
    _pdf_name = pdf_name if '.pdf' not in pdf_name else pdf_name[ 0 : pdf_name.find('.pdf') ]
    _json['_name'] = _pdf_name.replace('-', ' ')
    _json['_pages'] = [ page for i, page in _iterate_pages_as_str(_doc, _interpreter, _device) ]
    return _json

def _json_to_index(pdf_json, id):
    ''' creates a _type in the book-index
        with basic information.
        Avoid not setting id, as it creates a uid
        for every entry, allowing massive amounts
        of duplicates
    '''
    es = Elasticsearch()

    # apparently no _type field anymore, specify as a field

    es.index(   index='book-index',
                body= pdf_json,
                id=id
                )




if __name__ == '__main__':
    start = 0 ; id = start
    for pdf_name, pdf_type, pdf_path in _get_all_pdfs(start=start):
        # pdfr = _read_pdf(pdf_path)
        # _doc, _interpreter, _device = _read_pdf(pdf_path)
        _print_book_header(pdf_name) ; print('has the id: ', id)

        _json = _pdf_to_json(pdf_name, pdf_type, pdf_path)

        _pprint(_json) ; #_json_to_index(_json, id) ; id += 1

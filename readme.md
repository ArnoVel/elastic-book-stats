# PDF Parsing and Analysis using PDFMiner, ElasticSearch

The goal is to download e-books for free from the internet and index them by parsing them using `PDFMiner` to map them to strings.

Machine learning & visualization on the strings will probably be done at some point in the future ...


## PDF Parsing

Using both [PDFMiner](https://pypi.org/project/pdfminer3k/), and [PyPDF2](https://pypi.org/project/PyPDF2/), map each pdf to a list of strings describing its pages, as well as basic metadata about length, author description, the type of book & name.

## PDF Analysis

Using [ElasticSearch](https://www.elastic.co/), we create and index and compute various statistics on the aggregated dataset.

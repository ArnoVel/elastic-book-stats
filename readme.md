# PDF Parsing and Analysis using PDFMiner, ElasticSearch

The goal is to download e-books for free from the internet and index them by parsing them using `PDFMiner` to map them to strings.

Machine learning & visualization on the strings will probably be done at some point in the future ...


## PDF Parsing

Using both [PDFMiner](https://pypi.org/project/pdfminer3k/), and [PyPDF2](https://pypi.org/project/PyPDF2/), map each pdf to a list of strings describing its pages, as well as basic metadata about length, author description, the type of book & name.

## PDF Analysis

Using [ElasticSearch](https://www.elastic.co/), we create and index and compute various statistics on the aggregated dataset.


# Technical Details

## Creating the index locally & running tests on your machine

Given the documents in pdf form, one can index them with elk by running `basic_parse_store` after removing the comment symbol (`#`) at the following line:

```python
    _pprint(_json) ; #_json_to_index(_json, id) ; id += 1
```

The function `json_to_index(..)` maps the extracted pdf (as a json file) to its index.
Only use when the index does not yet exist or has been erased.

## Install requirements

This project is small but uses specific libraries. For the python3 dependencies, use the `requirements.txt` file; I also have jupyter-specific dependencies which I haven't listed, but one is the [`ipynb`](https://github.com/ipython/ipynb) package

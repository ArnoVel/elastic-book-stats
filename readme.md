# PDF Parsing and Analysis using PDFMiner, ElasticSearch

The goal is to download e-books for free from the internet and index them by parsing them using `PDFMiner` to map them to strings.

Machine learning & visualization on the strings will probably be done at some point in the future ...


## PDF Parsing

Using both [PDFMiner](https://pypi.org/project/pdfminer3k/), and [PyPDF2](https://pypi.org/project/PyPDF2/), map each pdf to a list of strings describing its pages, as well as basic metadata about length, author description, the type of book & name.

## PDF Analysis

Using [ElasticSearch](https://www.elastic.co/), we create and index and compute various statistics on the aggregated dataset.


# Technical Details

## Creating the index locally & running tests on your machine

Given the documents in pdf form, one can index them with elk by running `basic_parse_store` methods such as `generate_store_all`, which first calls
the routine `pdf_to_pickle` to store extracted pages, author string, theme, etc as rows in a pandas DataFrame.
For example the following calls:

```python
pdf_to_pickle()
  books_df = pd.read_pickle('./data/dataframe/books_df.pkl')
  j = 0
  for i,row in books_df.iterrows():
      pages, j = book_to_pages(row.to_dict(), j)
      bulk_index(pages)
  ```
stores into an index named `page-index` each page, with its attached book name, book num_pages, theme etc.
The function `json_to_index(..)` maps the extracted pdf (as a json file) to its index.
Only use when the index does not yet exist or has been erased.

## Install requirements

This project is small but uses specific libraries. For the python3 dependencies, use the `requirements.txt` file; I also have jupyter-specific dependencies which I haven't listed, but one is the [`ipynb`](https://github.com/ipython/ipynb) package

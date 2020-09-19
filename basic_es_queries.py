from elasticsearch import Elasticsearch
from collections import defaultdict
from utils import time_function, _pprint
from test.test_words import df_to_list, emotion_to_df
from addict import Dict

es = Elasticsearch() # assumes localhost:9200

def _check_all(addendum=''):
    ''' useful for small indexes: lists everything '''
    return es.search(   index='book-index'+addendum,
                        body= {
                            'query' : {
                                'match_all' : {}
                            }
                        })

def _num_docs(addendum=''):
    return es.count(   index='book-index'+addendum,
                        body= {
                            'query' : {
                                'match_all' : {}
                            }
                        }).get('count')
def _tail(num_docs_tail, addendum=''):
    ''' gets the tail, i.e the last `num_docs_tail` documents in terms of id'''

    num_docs = _num_docs()
    return es.search(       index='book-index'+addendum,
                            body= {
                                'query' : {
                                    'bool' : {
                                        'should' : [
                                            {'match_all' : {} }
                                        ],
                                        'filter' : [
                                            {   'range' : { '_id' : { 'gt' : num_docs - num_docs_tail }}}
                                        ]
                                    }
                                }
                                })

def _delete_all(addendum=''):
    ''' in case we need to wipe the index..'''
    es.delete_by_query(   index='book-index'+addendum,
                            body= {
                                'query' : {
                                    'match_all' : {}
                            }
                        })

def _search(body, addendum=''):
    return es.search(index='book-index'+addendum,
                    body=body)


# _pprint(_check_all('-page'), depth=6) # 5 depth does not display text..

def page_get_book(book_name):
    assert book_name in [ book.lower() for book in page_get_titles() ]
    body = Dict()
    body.query.bool.must.match = { "_name": book_name}
    return es.search(index='page-index', body=body)

def page_get_titles():
    body = Dict()
    body.size = 0
    body.aggs.titles.terms.field =  '_name.keyword'
    body.aggs.titles.terms.size = 10*page_num_docs() # put a limit +inf
    return [ d.get('key') for d in es.search(index='page-index', body=body)\
                                                        .get('aggregations')\
                                                        .get('titles')\
                                                        .get('buckets') ]

def page_book_get_between(low, high):
    body = Dict()
    body.query.bool.must = {
                        "range": {
                            "_num_pages": {
                                "gte": low,
                                "lte": high
                            }
                        }
                    }
    return es.search(index='page-index', body=body)

def page_num_docs():
    body = Dict()
    body.query.match_all = {}
    return es.count(index='page-index', body=body).get('count')

def check_get_book(name):
    res = page_get_book(name)
    _pprint(res.get('hits').get('hits'), depth=2)
    print('is the number of hits (=',res.get('hits').get('total'),') equal to the number of pages (=',res.get('hits').get('hits')[0].get('_source').get('_num_pages'), ')')

### Left to code: bit on filtering by emotion
if __name__ == '__main__':
    # res = page_get_titles()
    check_get_book('hamlet')

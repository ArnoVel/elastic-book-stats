from elasticsearch import Elasticsearch

from utils import time_function, _pprint

es = Elasticsearch() # assumes localhost:9200

def _check_all():
    ''' useful for small indexes: lists everything '''
    return es.search(   index='book-index',
                        body= {
                            'query' : {
                                'match_all' : {}
                            }
                        })

def _num_docs():
    return es.count(   index='book-index',
                        body= {
                            'query' : {
                                'match_all' : {}
                            }
                        }).get('count')
def _tail(num_docs_tail):
    ''' gets the tail, i.e the last `num_docs_tail` documents in terms of id'''

    num_docs = _num_docs()
    return es.search(       index='book-index',
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

def _delete_all():
    ''' in case we need to wipe the index..'''
    es.delete_by_query(   index='book-index',
                            body= {
                                'query' : {
                                    'match_all' : {}
                            }
                        })

_pprint(_check_all(), depth=5) # 5 depth does not display text..

print(_num_docs())
# print(_tail(3))

# _pprint(es.get(index='book-index', id=12), depth=2)
# q_poto = es.search(     index='book-index',
#                         body= {
#                             'query' : {
#                                 'match' : { '_name' : 'phantom' }
#                             }
#                         })
#
# _pprint(q_poto, depth=5)

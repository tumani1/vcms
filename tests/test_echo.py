from models import db

from models import Countries,Cities,Users
import zerorpc 

from tests import create_test_user

def test_echo():

    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    assert 'hello' ==  c.route({'api_group':'test',
                                'api_method':'echo',
                                'http_method':'put',
                                'token':'foobar',
                                'query_params':{
                                    'message':'hello'
                                },
                            })
    
    
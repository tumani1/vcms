import zerorpc
import unittest
from create_test_user import create
from models import GlobalToken,Users
from models import db
from zerorpcserver.server import mashed_routes, authorize

@db
def get_token_by_id(user_id,session = None):
    gt = session.query(GlobalToken).filter(GlobalToken.user_id == user_id)

    gta = [gte for gte in gt]
    assert len(gta) == 1

    return gta[0].token

class ZeroRpcServiceAuthTestCase(unittest.TestCase):

    user_id = None
    token = None
    session_token = None

    
    def setUp(self):
        self.cl = zerorpc.Client()
        self.cl.connect("tcp://127.0.0.1:4242")
        variable = create()
        self.user_id = variable
        self.token = get_token_by_id(self.user_id)
        
            
    def test_echo(self):
        Auth_IPC_pack = {'api_group':'auth',
                    'api_method':'session',
                    'http_method':'get',
                    'token':self.token,
                    'x_token': None,
                    'query_params':{}}

        auth_resp = self.cl.route(Auth_IPC_pack)

        session_token = auth_resp['session_token']
        
        IPC_pack = {'api_group':'test',
                    'api_method':'echo_auth',
                    'http_method':'get',
                    'x_token': session_token,
                    'query_params':{'message':'hello'}}
        resp = self.cl.route(IPC_pack)

        #resp = mashed_routes[('test','echo_auth','get')](**{'auth_user':db(lambda session: session.query(Users).first())(),'message':'hello'})
        print "Before assert \n", IPC_pack, '\n resp', resp
        self.assertEqual({'message': "Hello,Test"}, resp)

        
    def tearDown(self):
        self.cl.close()
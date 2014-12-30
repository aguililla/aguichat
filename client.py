import socket, sys, threading, time, getpass, pickle, message

S_HOST = "localhost"
S_PORT = 6666
TIMEOUT = .5

class Client(object):
    
    def __init__(self, gui=None):
        #Initialize socket to connect to server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(TIMEOUT)
        self.gui = gui

    #Takes values as input, connects to server socket, sends login message and
    #waits for response
    def login(self):
        if self.gui:
            pass
        else:
            self.name = raw_input('Nombre: ')
            self.pwd = getpass.getpass()
        m_login = Message(m_type=LOGIN, ':'.join([self.name, self.pwd]))
        m_login.encrypt()
        try:
            self.socket.connect((S_HOST, S_PORT))
            m_ser = pickle.dumps(m_login)
        except socket.error as e:
            print '[-] Socket error: Cannot connect to server', HOST, e
            return False
        except pickle.PickleError as e:
            print '[-] Pickle error: Cannot pickle login message', e
            return False
            
        self.socket.sendall(m_ser)
        print '[*] Autenticando...'
        try:
            m_rec = self.socket.recv(4096)
            m_loaded = pickle.loads(m_rec)
        except socket.timeout as e:
            print '[-] No response from server'
            return False
        except  pickle.UnpicklingError as e:
            print '[-] Error loading message', e
            return False
        if m_loaded.m_type = LOGIN_ACCEPT:
            return True
        else:
            return False
    
    
            

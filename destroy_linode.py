import os
from linode_api4 import LinodeClient
from config import params
from config import protected_linodes


client = LinodeClient(params['API_KEY'])
protected = protected_linodes

if __name__ == '__main__':
    for linode in client.linode.instances():
        if linode.label in protected:
            pass
        else:
            print "Deleting proxy: {}".format(linode.ipv4[0])
            linode.delete()
    os.remove("LINODE PROXY LIST.txt")
    os.remove("LINODE PROXY PASSWORDS.txt")

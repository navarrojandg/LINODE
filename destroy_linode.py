from linode_api4 import LinodeClient
from config import params
from config import protected_linodes


client = LinodeClient(params['API_KEY'])
protected = protected_linodes

if __name__ == '__main__':
    for item in client.linode.instances():
        if item.label in protected:
            pass
        else:
            print "Deleting proxy IP: {}".format(item.ipv4[0])
            item.delete()

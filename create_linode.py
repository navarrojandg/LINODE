from linode_api4 import LinodeClient
from config import params
from multiprocessing.dummy import Pool as ThreadPool
import os


class NewProxy():
    def __init__(self, region, ltype):
        self.client = LinodeClient(API_KEY)
        self.region = region
        self.ltype = ltype
        self.image = "linode/ubuntu16.04lts"
        self.stackscript = 68166

    def create(self):
        new_linode, password = self.client.linode.instance_create(
            self.ltype,
            self.region,
            image=self.image,
            stackscript=self.stackscript,
            stackscript_data={
                "squid_user":"{}".format(AUTH_USER),
                "squid_password":"{}".format(AUTH_PASS)
            }
        )
        print('{}:3128:{}:{}'.format(new_linode.ipv4[0], AUTH_USER, AUTH_PASS))
        with open('LINODE PROXY LIST.txt', 'a+') as f:
            f.write('{}:{}:{}:{}\n'.format(
                new_linode.ipv4[0],
                3128,
                AUTH_USER,
                AUTH_PASS
            ))
        with open('LINODE PROXY PASSWORDS.txt', 'a+') as f:
            f.write('{} \t{}\n'.format(new_linode.ipv4[0], password))


def set_region():
    region_list = LinodeClient(API_KEY).regions()
    for i in range(len(region_list)):
        print('{} | {}'.format(i, region_list[i]))
    r = input('Please select an available region: ')
    return region_list[r]


if __name__ == '__main__':
    #EDIT PARAMS IN CONFIG FILE FIRST
    API_KEY = params['API_KEY']
    AUTH_USER = params['AUTH_USER']
    AUTH_PASS = params['AUTH_PASS']
    #USER SETS QTY AS WELL AS REGION, LINODE TYPE IS AUTO SET TO NANODE
    count = int(input("How many proxies would you like to create? "))
    region = set_region()
    print("CREATING {} | {} PROXIES PLEASE WAIT".format(count, region))
    os.remove("LINODE PROXY LIST.txt")
    os.remove("LINODE PROXY PASSWORDS.txt")
    ltype = LinodeClient(API_KEY).linode.types()[0]
    proxylist = []
    for i in range(count):
        proxylist.append(NewProxy(region, ltype))
    pool = ThreadPool()
    proxies = pool.map(lambda x: x.create(), proxylist)
    print("Proxy list has been exported to LINODE PROXY LIST.txt")

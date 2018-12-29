from linode_api4 import LinodeClient
from config import params

API_KEY = params['API_KEY']
AUTH_USER = params['AUTH_USER']
AUTH_PASS = params['AUTH_PASS']

class NewProxy():
    def __init__(self, region, ltype):
        self.client = LinodeClient(API_KEY)
        self.region = region
        self.ltype = ltype
        self.image = "linode/ubuntu16.04lts"
        self.stackscript = 68166


class NewProxy():
    def __init__(self):
        self.API_KEY = API_KEY
        self.client = LinodeClient(API_KEY)
        self.region = None
        self.ltype = None
        self.image = "linode/ubuntu16.04lts"
        self.stackscript = 68166
        self.count = raw_input('How many proxies would you like to make?: ')
        self.set_region()
        self.set_type()

    def set_region(self):
        region_list = self.client.regions()
        for i in range(len(region_list)):
            print('{} {}'.format(i, region_list[i]))
        r = input('Please select an available region: ')
        self.region = region_list[r]

    def set_type(self):
        type_list = self.client.linode.types()
        for i in range(len(type_list)):
            print('{} {}'.format(i, type_list[i]))
        t = input('Please select an available linode type: ')
        self.ltype = type_list[t]

    def create_linodes(self):
        for i in range(int(self.count)):
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
            print('Creating Proxy {}...'.format(new_linode.ipv4[0]))
            with open('LINODE PROXY LIST.txt', 'a+') as f:
                f.write('{}:{}:{}:{}\n'.format(
                    new_linode.ipv4[0],
                    3128,
                    AUTH_USER,
                    AUTH_PASS
                ))
            with open('LINODE PROXY PASSWORDS.txt', 'a+') as f:
                f.write('{} \t{}\n'.format(new_linode.ipv4[0], password))


if __name__ == '__main__':
    my_proxies = NewProxy()
    my_proxies.create_linodes()
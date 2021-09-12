from ldap3 import Server,Connection,ALL,SUBTREE,ALL_ATTRIBUTES,MODIFY_REPLACE,MODIFY_ADD,MODIFY_DELETE, SAFE_SYNC, NTLM
import time
import re
from passlib.hash import  ldap_salted_sha1 as ssha

class LdapInit():
    def __init__(self, ldap_server=None, ldap_user=None, ldap_pwd=None):
        self.ldap_server = ldap_server
        self.ldap_user = ldap_user
        self.ldap_pwd = ldap_pwd

    def ldap_conn(self):
        server = Server(self.ldap_server)
        conn = Connection(server, self.ldap_user, self.ldap_pwd, client_strategy=SAFE_SYNC, auto_bind=True)
        return conn

class LdapOps(LdapInit):
    def __init__(self, ldap_server=None, ldap_user=None, ldap_pwd=None):
        super().__init__(ldap_server, ldap_user, ldap_pwd)

    def ldap_get_uid(self, ldap_search_base):
        uidlist = []
        conn = self.ldap_conn()
        status, result, response, _ = conn.search(ldap_search_base, '(objectclass=*)', attributes=['*'])
        for i in response:
            searchObj = re.search('uid=\w+', i['dn'])
            if searchObj:
                uidlist.append(searchObj.group().strip('uid='))
        return uidlist

    def ldap_add_user(self, uid, ou):
        conn = self.ldap_conn()
        # print(conn.add('cn=test03,ou=jenkins,dc=demo,dc=com', 'inetorgperson',
        #          {'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': 1111}))
        print(conn.add('uid=' + uid + ',' + ou, ['account', 'simpleSecurityObject', 'top'],
                                {'userPassword': ssha.encrypt('123456',salt_size=12)}))

    def ldap_del_user(self, uid, ou):
        conn = self.ldap_conn()
        print(conn.delete('uid=' + uid + ',' + ou))

    def ldap_add_group(self, ou):
        conn = self.ldap_conn()
        print(conn.add(ou, 'organizationalUnit'))

    def ldap_del_group(self, ou):
        conn = self.ldap_conn()
        print(conn.delete(ou))

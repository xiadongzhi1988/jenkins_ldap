import myldap
from myldap import ldapuser
import sys


ldap_server = '10.10.111.159'
ldap_user = 'cn=admin,dc=demo,dc=com'
ldap_pwd = '123456'
ldap_search_base = 'ou=jenkins,dc=demo,dc=com'

# print(len(sys.argv))

if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], 'user', 'ou')
    quit(111)
# uid = sys.argv[1]
# ou = sys.argv[2]
# l = ldapuser.LdapOps(ldap_server, ldap_user, ldap_pwd)
# l.ldap_add_user(uid, ou)
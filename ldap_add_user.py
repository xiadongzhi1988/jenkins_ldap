import myldap
from myldap import ldapuser
import sys


# ldap_server = '10.10.111.159'
# ldap_user = 'cn=admin,dc=demo,dc=com'
# ldap_pwd = '123456'
ldap_search_base = 'ou=jenkins,dc=demo,dc=com'



if len(sys.argv) < 3:
    print('Usage:', sys.argv[0], 'user1', 'user2', '...', 'ou=demo,dc=demo,dc=com')
    quit(111)
else:
    ou = sys.argv[-1]
    l = ldapuser.LdapOps()
    for i in range(1, len(sys.argv) - 1):
        l.ldap_add_user(sys.argv[i], ou)


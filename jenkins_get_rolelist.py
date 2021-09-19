import myjenkins
from myjenkins import jenkinsrole



role_type = 'projectRoles'
j = jenkinsrole.JenkinsRole()
all_role = j.get_all_roles(role_type)
for role in all_role.keys():
    print(role)
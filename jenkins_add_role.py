import myjenkins
from myjenkins import jenkinsrole


# j = jenkinsrole.JenkinsRole('10.10.111.201', 'admin')
# j.host = "10.10.111.201"
# j.port = 8080
# j.username = "admin"
# j.token = '116c82f41b96860fd566d04ec7244d1965'


role_type = 'projectRoles'
permissions = 'com.cloudbees.plugins.credentials.CredentialsProvider.Update,hudson.model.Item.Create,hudson.model.Run.Delete,hudson.model.Item.Workspace,com.cloudbees.plugins.credentials.CredentialsProvider.Delete,com.cloudbees.plugins.credentials.CredentialsProvider.ManageDomains,hudson.model.Run.Replay,hudson.model.Item.Configure,org.jenkins.plugins.lockableresources.LockableResourcesManager.View,hudson.model.Item.Cancel,hudson.model.Item.Delete,hudson.model.Item.Read,com.cloudbees.plugins.credentials.CredentialsProvider.View,com.cloudbees.plugins.credentials.CredentialsProvider.Create,hudson.model.Item.Build,org.jenkins.plugins.lockableresources.LockableResourcesManager.Unlock,hudson.plugins.jobConfigHistory.JobConfigHistory.DeleteEntry,hudson.scm.SCM.Tag,hudson.model.Item.Move,org.jenkins.plugins.lockableresources.LockableResourcesManager.Reserve,hudson.model.Item.Discover,hudson.model.Run.Update'


role_name_pattern = {
'item_bpm':'.*bpm.*',
'item_bucket':'.*bucket.*',
'item_cp':'.*cp.*',
'item_crm':'.*crm.*',
'item_design':'.*design.*',
'item_dms':'.*dms.*',
'item_guimo':'.*guimo.*',
'item_hrm':'.*hrm.*',
'item_idm':'.*idm.*',
'item_mdm':'.*mdm.*',
'item_paas':'.*paas.*',
'item_portal':'.*portal.*',
'item_project':'.*project.*',
'item_rest':'.*rest.*',
'item_subscription':'.*subscription.*',
'item_webrtc':'.*webrtc.*',
'item_workflow':'.*workflow.*'
}

for role_name, role_pattern in role_name_pattern.items():
    res_code = j.add_role(role_type, role_name, permissions, role_pattern)
    print(res_code)


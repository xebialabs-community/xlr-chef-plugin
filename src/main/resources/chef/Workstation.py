#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import os, re, sys, traceback

import java.lang.String as String

from com.xebialabs.overthere import CmdLine
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from com.xebialabs.overthere.local import LocalConnection

class Workstation(object):
    def __init__(self, workstation_config):
        self.cmd_line = CmdLine()
        self.chef_sdk_path = workstation_config['chef_sdk_path']
        self.client_key  = Workstation.format_key(workstation_config['client_key'])
        if workstation_config['os'] :
            self.os = "UNIX"
        else:
            self.os = "WINDOWS"
        self.chef_server_url = workstation_config['chef_server_url']
        self.node_name = workstation_config['node_name']
        self.log_level = workstation_config['log_level']
        self.log_location = workstation_config['log_location']
        self.cookbook_path = workstation_config['cookbook_path']
        self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
        self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()

    @staticmethod
    def get_workstation(workstation_config):
        return Workstation(workstation_config)

    @staticmethod
    def format_key(key):
        chef_key = re.sub("---- .*", "----\n", key)
        footer = re.sub(".* ----", "----", key)
        body = re.sub(".*--- ", "", key)
        body = re.sub(" ---.*", "", body)
        for l in body.split():
            chef_key = "%s%s\n" % (chef_key, l)
        chef_key = "%s%s\n" % (chef_key, footer)
        return chef_key

    @staticmethod
    def zip_workspace(workspace_path, connection):
        zip_script = "#!/bin/bash\ncd %s\ntar -czf /tmp/chef.tgz ." % workspace_path
        zip_script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), 'zip.script'))
        OverthereUtils.write(String(zip_script).getBytes(), zip_script_file)
        zip_script_file.setExecutable(True)
        command = CmdLine()
        command.addArgument(zip_script_file.getPath())
        return connection.execute(command)

    @staticmethod
    def process_flag_with_arguments(arguments, flag):
        if arguments is not None and arguments: return "%s %s" % (flag, arguments)
        return ""

    @staticmethod
    def process_boolean_flag(variables, name, value):
        if variables[name]: return value
        return ""

    @staticmethod
    def process_unix_authentication(variables):
        # Handle authentication, identity_file takes precedence.
        if variables['identity_file'] is not None and variables['identity_file']:
            authentication_option = "--identity-file %s" % variables['identity_file']
        else:
            authentication_option = "--ssh-password '%s'" % variables['ssh_password']
        return authentication_option

    @staticmethod
    def process_additional_options(options):
        if options is not None and options: return options
        return ""

    def chef_bootstrapunix(self, variables):
        sudo_param = Workstation.process_boolean_flag(variables, "sudo", "--sudo")
        sudo_password_param = Workstation.process_boolean_flag(variables, "sudo_password", "--sudo-password")
        run_list_param = Workstation.process_flag_with_arguments(variables['run_list'], "--run-list")
        authentication_option = Workstation.process_unix_authentication(variables)
        return self.execute_knife_command("bootstrap %s --ssh-user %s %s %s %s --node-name %s %s --yes" \
            % (variables['address'], variables['ssh_user'], authentication_option, sudo_param, sudo_password_param, variables['node_name'], run_list_param), 'chef_bootstrapunix.script', variables['options'], True)

    def chef_bootstrapwindows(self, variables):
        run_list_param = Workstation.process_flag_with_arguments(variables['run_list'], "--run-list")
        return self.execute_knife_command("bootstrap windows winrm %s --winrm-user %s --winrm-password '%s' --node-name %s %s --yes"
            % (variables['address'], variables['username'], variables['password'], variables['node_name'], run_list_param),
            'chef_bootstrapwindows.script', variables['options'], True)

    def chef_cookbooklist(self, variables):
        return self.execute_knife_command("cookbook list", 'chef_cookbooklist.script', variables['options'], True)

    def chef_nodelist(self, variables):
        return self.execute_knife_command("node list", 'chef_nodelist.script', variables['options'], True)

    def chef_clientlist(self, variables):
        return self.execute_knife_command("client list", 'chef_clientlist.script', variables['options'], True)

    def chef_deleteoperation(self, target, variables):
        return self.execute_knife_command("%s delete %s --yes" % (target, variables['node_name']), 'chef_delete.script', variables['options'], True)

    def chef_deletenode(self, variables):
        return self.chef_deleteoperation("node", variables)

    def chef_deleteclient(self, variables):
        return self.chef_deleteoperation("client", variables)

    def chef_applycookbook(self, variables, is_unix=True):
        if is_unix:
            os_specific_command = "ssh"
            os_chef_client_command = "'sudo chef-client'"
        else:
            os_specific_command = "winrm"
            os_chef_client_command = "'chef-client'"
        command ="%s --yes 'name:%s' %s --yes --%s-user %s --%s-password '%s'" \
            % (os_specific_command, variables['node_name'], os_chef_client_command, os_specific_command, variables['username'], os_specific_command, variables['password'])
        return self.execute_knife_command(command, 'chef_applycookbook.script', variables['options'], True)

    def chef_applycookbookunix(self, variables):
        return self.chef_applycookbook(variables, True)

    def chef_applycookbookwindows(self, variables):
        return self.chef_applycookbook(variables, False)

    def chef_setrunlist(self, variables):
        return self.execute_knife_command("node run_list set %s 'recipe[%s]'" % (variables['node_name'], variables['run_list']), 'chef_setrunlist.script', variables['options'], True)

    def chef_shownode(self, variables):
        return self.execute_knife_command("node show %s" % variables['node_name'], 'chef_shownode.script', variables['options'], True)


    def execute_knife_command(self, command, script_name, options=None, zip_workspace=False):
        connection = None
        try:
            options = Workstation.process_additional_options(options)
            connection = LocalConnection.getLocalConnection()
            workspace_path = self.create_chef_tmp_workspace(connection)
            knife_command = "#!/bin/bash\ncd %s\n%s/bin/knife %s %s" % (workspace_path, self.chef_sdk_path, command, options)
            script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), script_name))
            OverthereUtils.write(String(knife_command).getBytes(), script_file)
            script_file.setExecutable(True)
            command = CmdLine()
            command.addArgument(script_file.getPath())
            output_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
            error_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
            exit_code = connection.execute(output_handler, error_handler, command)
            if zip_workspace:
                self.zip_workspace(workspace_path, connection)
            return [exit_code, output_handler]
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)
        finally:
            if connection is not None:
                connection.close()

    def create_chef_tmp_workspace(self, connection):
        try:
            tmp_workspace_file = connection.getTempFile('tmp_workspace')
            workspace_path = re.sub('tmp_workspace', '', tmp_workspace_file.getPath())
            workspace_directory = connection.getFile(workspace_path)
            connection.setWorkingDirectory(workspace_directory)
            new_path = "%s.chef" % workspace_path
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            self.generate_knife_rb(new_path, connection)
            chef_key_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(new_path), 'chefkey.pem'))
            OverthereUtils.write(String(self.client_key).getBytes(), chef_key_file)
            script="""#!/bin/bash\ncd %s\n%s/bin/knife ssl fetch\n%s/bin/knife ssl check""" % (workspace_path, self.chef_sdk_path, self.chef_sdk_path)
            script_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(workspace_path), 'ssl.script'))
            OverthereUtils.write(String(script).getBytes(), script_file)
            script_file.setExecutable(True)
            self.cmd_line.addArgument(script_file.getPath())
            connection.execute(self.stdout, self.stderr, self.cmd_line)
            return workspace_path
        except Exception:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1)

    def generate_knife_rb(self, path, connection):
        knife_contents ='''current_dir = File.dirname(__FILE__)
  log_level %s
  log_location %s
  node_name "%s"
  client_key "#{current_dir}/chefkey.pem"
  chef_server_url "%s"
  Cookbook_path %s''' % (self.log_level, self.log_location, self.node_name, self.chef_server_url, self.cookbook_path)
        knife_rb_file = connection.getFile(OverthereUtils.constructPath(connection.getFile(path), 'knife.rb'))
        OverthereUtils.write(knife_contents, knife_rb_file)

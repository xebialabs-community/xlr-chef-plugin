#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import re
import java.lang.String as String
from java.io import PrintWriter
from java.io import StringWriter
from com.xebialabs.overthere import CmdLine
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from com.xebialabs.overthere.local import LocalConnection

class ChefClient( object ):
   def __init__(self, chefCI ):
      self.cmdLine = CmdLine()
      self.chefPath = chefCI['chefPath']
      if chefCI['os'] :
         self.os = "UNIX"
      else:
         self.os = "WINDOWS"
      # End if
      self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
      self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()
   #
   @staticmethod
   def createDXClient( chefCI ):
      return ChefClient( chefCI )
   # End createDKClient
   #
   @classmethod
   def knife( self, search, cmd, attribute ):
      print "kife"
      # knife ssh 'role:web' 'sudo chef-client' --ssh-user rbroker --ssh-password 'merlin1' --attribute publicip
   # End knife
   #
   @classmethod
   def bootstrapUnix( self, address, nodeName, knifeFile, chefKey, sudo, sudoPassword, sshUser, sshPassword, identity, runList ):
      if sudo :
         sudoParm = "--sudo"
      else:
         sudoParm = ""
      # End if
      if sudoPassword :
         sudoPassParm = "--use-sudo-password"
      else:
         sudoPassParm = ""
      # End if
      connection = None
      try:
         if (type(runList).__name__ <> 'NoneType' and len(runList) > 0):
            runOpt = "--run-list '%s'" % runList
         else:
            runOpt = ""
         # End if
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
tar -czf /tmp/chef.tgz .
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife bootstrap %s --ssh-user %s --ssh-password '%s' %s %s --node-name %s %s
""" % ( scriptPath, knifeFile, chefKey, self.chefPath, self.chefPath, self.chefPath, address, sshUser, sshPassword, sudoParm, sudoPassParm, nodeName, runOpt)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End bootstrapUnix
   #
   @classmethod
   def bootstrapWindows( self, address, nodeName, runList):
      print "bootstrap Windows"
      # knife bootstrap windows winrm ADDRESS --winrm-user USER --winrm-password 'PASSWORD' --node-name node1-windows --run-list 'recipe[learn_chef_iis]'
   # End bootstrapWindows

   @classmethod
   def deleteNode( self, knifeFile, chefKey, nodeName ):
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife node delete --yes %s
""" % ( scriptPath, knifeFile, chefKey, self.chefPath, self.chefPath, self.chefPath, nodeName)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
         
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def

   @classmethod
   def deleteClient( self, knifeFile, chefKey, nodeName ):
      connection = None
      try:
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife client delete --yes %s
""" % ( scriptPath, knifeFile, chefKey, self.chefPath, self.chefPath, self.chefPath, nodeName)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
      
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def


   @classmethod
   def getCookbookList( self, knifeFile, chefKey, options ):
      connection = None
      try:
         if (type(options).__name__ <> 'NoneType' and len(options) > 0):
            options = " %s " % options
         else:
            options = ""
         # End if
         connection = LocalConnection.getLocalConnection()
         scriptFile = connection.getTempFile('chef', '.bat')
         scriptPath = re.sub('chef.bat', '', scriptFile.getPath())
         script="""#!/bin/bash
cd %s
KNIFERB='%s
'
CHEFKEY='%s
'
mkdir .chef
tar -czf /tmp/chef.tgz .
echo "$KNIFERB" > .chef/knife.rb
echo "$CHEFKEY" > .chef/chefkey.pem
%s/bin/knife ssl fetch
%s/bin/knife ssl check
%s/bin/knife cookbook list %s
""" % ( scriptPath, knifeFile, chefKey, self.chefPath, self.chefPath, self.chefPath, options)
         OverthereUtils.write( String( script ).getBytes(), scriptFile )
          
         scriptFile.setExecutable(True)
         print "Execute file %s" % ( scriptFile.getPath() )
         self.cmdLine.addArgument( scriptFile.getPath() )
         exitCode = connection.execute( self.stdout, self.stderr, self.cmdLine )
         self.printStdOut()
         self.printStdErr()
      except Exception, e:
         print "Caught Exception "
         stacktrace = StringWriter()
         writer = PrintWriter( stacktrace, True )
         e.printStackTrace(writer)
         self.stderr.handleLine(stacktrace.toString())
         return 1
      finally:
         if connection is not None:
            connection.close()
         # End if
      # End try
      return exitCode
   # End def


   @classmethod
   def printData(self, data):
      print data
   # End def

   @classmethod
   def printException(self, e):
      print e
   # End def

   @classmethod
   def getStdout(self):
      return self.stdout.getOutput()
   # End getStdout

   @classmethod
   def getStdoutLines(self):
      return self.stdout.getOutputLines()
   # End getStdoutLines

   @classmethod
   def printStdOut(self):
      print "#===== STD Out ====\n\n"
      tmpData = self.getStdoutLines()
      for val in tmpData:
         print "%s\n" % val
      self.data = tmpData[len(tmpData)-1]
      print "#===== STD Out ====\n\n"
   # End printStdOut

   @classmethod
   def getStderr(self):
      return self.stderr.getOutput()
   # End getStderr

   @classmethod
   def getStderrLines(self):
      return self.stderr.getOutputLines()
   # End getStderrLines

   @classmethod
   def printStdErr(self):
      print "#===== STD Err ====\n\n"
      tmpData = self.getStderrLines()
      for val in tmpData:
         print "%s\n" % val
      print "#===== STD Err ====\n\n"
   # End printStdOut

   @classmethod
   def getData(self):
      return self.data
   # End getData
# End ChefClient
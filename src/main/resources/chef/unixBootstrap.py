#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#
import sys, traceback

from chef.ChefClient import ChefClient

if chefClient is None:
   print "No server provided."
   sys.exit(1)

chefDXClient = ChefClient.createDXClient(chefClient)

try:
   errorCode = chefDXClient.bootstrapUnix( address, nodeName, knifeFile, sudo, sudoPassword, sshUser, sshPassword, identity, runList )
   data = chefDXClient.getData()
except Exception, e:
   traceback.print_exc(file=sys.stdout)
   print chefDXClient.print_error( e )
   print "Failed to bootstrap %s" % (nodeName)
   sys.exit(1)



#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys
from chef.Workstation import Workstation

result = Workstation.get_workstation(chef_workstation).node_list(options)

if result[0] <> 0:
    sys.exit(result[0])
else:
    output_handler = result[1]
    nodes = []
    for node in output_handler.getOutputLines():
        nodes.append(node)
    output = nodes

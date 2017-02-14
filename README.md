#XL Release Chef Plugin

## Preface
This document describes the functionality provide by the `xlr-chef-plugin`

## Overview
This module offers tasks to apply Chef cookbooks on a remote hosts.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.


## Chef Tasks

### Bootstrap Unix Tasks
The bootstrap unix task bootstraps a unix server into your chef server

![ChefBootstrapUnix](images/ChefBootstrapUnix.png)

### Delete Client
The delete client task deletes the client from your chef server

![ChefDeleteClient](images/ChefDeleteClient.png)

### Delete Node
The delete node tasks deletes the node from your chef server

![ChefDeleteNode](images/ChefDeleteNode.png)

### Get Cookbook List
Get a list of the cookbooks in the Chef Server

![ChefCookbookList](images/ChefCookbookList.png)

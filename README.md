#XL Release Chef Plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-chef-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-chef-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/09848434df324f96afd8517e05f4b0c1)](https://www.codacy.com/app/zvercodebender/xlr-chef-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-chef-plugin&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-chef-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-chef-plugin)

## Preface
This document describes the functionality provide by the `xlr-chef-plugin`

## Overview
This module offers a basic interface to Chef functionality on a Chef server as well as Chef Nodes.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

## Workstation CI
The Chef plugin can connect to multiple Chef servers or connect to the same server with different shared credentials. In this configuration, the XL Release Server is acting as a Chef Workstation, and needs to have access to the ![Chef DK](https://downloads.chef.io/chefdk). The Configuration Item for the Chef Workstation screen looks like the following:

![WorkstationSharedConfigurationItem](images/ChefSharedConfiguration.png)

## Chef Tasks

### Bootstrap Unix Task
The Bootstrap Unix task bootstraps a unix node into your Chef server.

![ChefBootstrapUnix](images/ChefBootstrapUnix.png)

### Bootstrap Windows Task
The Bootstrap Windows task bootstraps a windows node into your Chef server.

![ChefBootstrapWindows](images/ChefBootstrapWindows.png)

### Client List
The Client List task returns a list of clients from your Chef server.
![ChefClientList](images/ChefClientList.png)

### Node List
The Node List task returns a list of nodes from your Chef server.
![ChefNodeList](images/ChefNodeList.png)

### Show Node
The Show Node task returns the details of a specified node from your Chef server.
![ChefShowNode](images/ChefShowNode.png)

### Delete Client
The Delete Client task deletes the client from your Chef server.
![ChefDeleteClient](images/ChefDeleteClient.png)

### Delete Node
The Delete Node task deletes the node from your Chef server.
![ChefDeleteNode](images/ChefDeleteNode.png)

### Cookbook List
The Cookbook List task retrieves a list of the cookbooks in the Chef server.
![ChefCookbookList](images/ChefCookbookList.png)

### Set Runlist
The Set Runlist task sets the run_list for a specified node.
![ChefSetRunlist](images/ChefSetRunlist.png)

### Apply Cookbook Unix
The Apply Cookbook Unix task applies a cookbook to a specified unix node.
![ChefApplyCookbookUnix](images/ChefApplyCookbookUnix.png)

### Apply Cookbook Windows
The Apply Cookbook Windows task applies a cookbook to a specified windows node.
![ChefApplyCookbookWindows](images/ChefApplyCookbookWindows.png)

---

## References:
* [https://docs.chef.io/](https://docs.chef.io/)
* [https://docs.chef.io/knife_data_bag.html](https://docs.chef.io/knife_data_bag.html)
* [https://gist.github.com/jtimberman/1302749](https://gist.github.com/jtimberman/1302749)
* [http://misheska.com/blog/2013/06/16/getting-started-writing-chef-cookbooks-the-berkshelf-way/](http://misheska.com/blog/2013/06/16/getting-started-writing-chef-cookbooks-the-berkshelf-way/)


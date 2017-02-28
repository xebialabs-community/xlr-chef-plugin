#XL Release Chef Plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-chef-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-chef-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/09848434df324f96afd8517e05f4b0c1)](https://www.codacy.com/app/zvercodebender/xlr-chef-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-chef-plugin&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-chef-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-chef-plugin)

## Preface
This document describes the functionality provide by the `xlr-chef-plugin`

## Overview
This module offers tasks to apply Chef cookbooks on a remote hosts.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

## Chef CI
The Chef plugin can connect to multiple Chef servers or connect to the same server with different shared credentials.  The Configuration Item for a Chef server screen looks like the following:

![ChefSharedConfigurationItem](images/ChefSharedConfigurationItem.png)


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

---

## References:
* [https://docs.chef.io/](https://docs.chef.io/)
* [https://docs.chef.io/knife_data_bag.html](https://docs.chef.io/knife_data_bag.html)
* [https://gist.github.com/jtimberman/1302749](https://gist.github.com/jtimberman/1302749)
* [http://misheska.com/blog/2013/06/16/getting-started-writing-chef-cookbooks-the-berkshelf-way/](http://misheska.com/blog/2013/06/16/getting-started-writing-chef-cookbooks-the-berkshelf-way/)


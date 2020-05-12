#!/bin/bash
# Get the Intel Repository public key and install it.  We will do the following from 
# /tmp since both users and root have read/write in /tmp.  You can use any other 
# directory where you have read/write as both user and sudo user:

# use wget to fetch the Intel repository public key

cd /tmp

wget https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB

# add to your apt sources keyring so that archives signed with this key will be trusted.

sudo apt-key add GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB

# remove the public keyA

rm GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB

# Configure the APT client to use Intel's repository:
echo "deb https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list

# Alternatively, if add-apt-repository utility is installed, you can use something like:
sudo add-apt-repository "deb https://apt.repos.intel.com/oneapi all main"

# Download package info for oneAPI Toolkit and components. 
sudo apt-get update

# Install the desired package.  Determine which Intel® oneAPI Toolkit package or packages 
# you require.  A Table of Packages is at the top of this page.   If you are on a 
# company intranet or behind a firewall make sure to set environment variables http_proxy 
# and https_proxy appropriate to #allow yum access the repository servers using https protocol.
# To install a Toolkit, for example the Intel® oneAPI Base Toolkit, the meta package name is 
# "intel-basekit" and it can be installed with the following:

sudo apt-get install intel-basekit

#repeat 'apt-get install ...' for each toolkit you need
sudo apt-cache pkgnames intel | grep kit$

# Other installation options (toolkits and individual components) are available in 
# the form of # meta-packages.

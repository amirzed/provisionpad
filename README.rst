************
ProvisionPad
************

ProvisionPad is a very simple command line tool that enables 
developers/data-scientists start secure sandboxes that can be 
accoessed only using their personal ssh-key.

It configures the local machine so you can connect to the remote sandbox using 

`VS Code <https://code.visualstudio.com/download>`_

prerequisites
-------------

You need to have your AWS Access Keys (Access Key ID and Secret Access Key). 
If you dont already have them you can get it thourgh AWS management console:

- Log in to AWS management console.
- Click on user menue
- Click on My Security Credentials
- Section Access keys for CLI, SDK, & API access you can create one.

*You do not need to worry about the following if you have root access (owner) or admin access to the AWS account.*
Before you can use/test this library you need to have AWS user account with the following permissions:

- AmazonEC2FullAccess 
- IAMFullAccess 
- AmazonVPCFullAccess 

Getting Started
---------------

For Windows users you need to install Python first and add it to your path so you can execute commands from CMD.
After that you can install it using (not added to PyPI yet):

.. code-block::

    git clone https://github.com/amirzed/provisionpad
    cd /path/to/cloned/directory
    pip install .






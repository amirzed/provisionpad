************
ProvisionPad
************

ProvisionPad is a very simple command line tool that enables 
developers/data-scientists start secure sandboxes that can be 
accoessed only using their personal ssh-key. (Will be configurable pretty soon to provide more options)

It configures the local machine so you can connect to the remote sandbox using 

`VS Code <https://code.visualstudio.com/download>`_

prerequisites
-------------

You need to have your AWS Access Keys (Access Key ID and Secret Access Key).
See AWS requirements below for more information. 

Installing ProvisionPad
-----------------------

For Windows users you need to install Python first and add it to your path.
It has been tested on Windows 10, macOS 10.14 (Mojave), and Ubuntu 18
After that you can install it using (not added to PyPI yet):

.. code-block::

    git clone https://github.com/amirzed/provisionpad
    cd /path/to/cloned/directory
    pip install .

Getting Started
---------------

To initiate your sandbox environment type the following in terminal

.. code-block::

    ppad initiate

It will ask for aws access credentials, as well 
as the name you want to use for the environement. 
The name will be used for tagging the resources created on AWS. 
You can specify an AWS image and AWS region to use or leave it blank. 
If you leave them blank defaults will be used. You just need to run the command above only once at the begining.

.. code-block::

    ppad create sandboxname sandboxtype

for example:

.. code-block::

    ppad create boxfortest m4.large

You can check and see how many running or stopped instances you have using:

.. code-block::

    ppad stat

You can stop a running instance manually using 

.. code-block::

    ppad stop theinstancename

where the instance name can be obtained using `ppad stat`

You can start a running instance using 

.. code-block::

    ppad start theinstancename

You can terminate a running instance using 

.. code-block::

    ppad terminate theinstancename

For more information on commands 

.. code-block::

    ppad --help

Conneting to the Remote Host
----------------------------

To ssh into the given server simple use

.. code-block::

    ssh theinstancename

To connect to the instance using VS Code you can use Visual Studio Code 
`Remote - SSH <https://code.visualstudio.com/docs/remote/ssh>`_ extension 

After installing the extension reload the Windows

`Ctrl+Shift+P reload window` then 
`Ctrl+Shift+P Remote-SSH:Connect to Host` 
and select the instance name from the menue

To access terminal on remote using VS Code simply use `Ctrl+``




AWS Cost Saving
---------------

Notice that provisioned instances will stop automatically after 20 minutes 
of low cpu activity, i.e. if the idle time percentage was over 98% and the 
gradient of cpu usage is less than 0.001. *more options will be added to this section pretty soon*

AWS requirements
----------------

If you dont already AWS access credentials you can get it thourgh AWS management console:

- Log in to AWS management console
- Click on user menue
- Click on My Security Credentials
- Section Access keys for CLI, SDK, & API access you can create one.

*You do not need to worry about the following if you have root access 
(owner) or admin access to the AWS account.*
Before you can use/test this library you need to have AWS user account with 
the following permissions:

- AmazonEC2FullAccess 
- IAMFullAccess 
- AmazonVPCFullAccess 



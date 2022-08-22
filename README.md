# ProvisionPad [![Join the Community](https://img.shields.io/badge/Join%20the%20community-blueviolet.svg)](https://spectrum.chat/provisionpad/)  [![Open Issues](https://img.shields.io/github/issues-raw/provisionpad/provisionpad.svg)](https://github.com/provisionpad/provisionpad/issues) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/provisionpad/provisionpad/blob/master/LICENSE)

<img src="https://i.ibb.co/88kHGrt/logo-1x.png" />

Connect to AWS EC2 instances right from your terminal.

ProvisionPad takes care of all the tedious details of setting up secure EC2 instances and adding proper configuration to your local machine so you can start, stop and connect to your instances directly from your Terminal/editor.

- Start and stop EC2 instances directly from your terminal without the hassle.
- Use your local VS Code editor or Terminal to access, edit and run the code on EC2 instances.
- Automatically stop inactive instances.


<img src="https://i.ibb.co/KqgLQwf/terminal-border.png" />


## Prerequisites

- AWS Access Key ID and Secret Access Key (See the last section if you don't know how to get them)

- Python installed locally


## Installing ProvisionPad

```
pip install provisionpad
```

## Getting Started


To initiate the environment:

```
propad initiate
```

After initiating the environment you can create an EC2 instance using:

```
propad create
```

To stop the instance:
```
propad stop [instancename]
```

To get a list of all your running/stopped instances:
```
propad stat
```

You can start a stopped instance using

```
propad start [instancename]
```

You can terminate a running instance using

```
propad terminate [instancename]
```

For more information on commands

```
propad --help
```

## Connecting to the Remote Host

To ssh into an instance simply use

```
ssh [instancename]
```


## Connecting through VS Code
To connect to the instance using VS Code, install the [Visual Studio Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview).

`Ctrl+Shift+P reload window` then
`Ctrl+Shift+P Remote-SSH:Connect to Host`
and select the instance name from the menu

To access terminal on remote using VS Code simply use `Ctrl+``


## AWS Cost Saving

Instances created with ProvisionPad will stop automatically after 20 minutes
of low CPU activity, i.e. if the idle time percentage was over 98% and the
gradient of CPU usage is less than 0.001. *more options will be added*

## How to get your AWS Access Key ID and Secret Access Key

If you don't have AWS access credentials you can get them through AWS management console:

- Log in to AWS management console
- Click on user menu
- Click on My Security Credentials
- Section Access keys for CLI, SDK, & API access you can create one.

Before you can use/test this library you need to have AWS user account with
the following permissions (You already have these permissions if you have root access
(owner) or admin access to the AWS account.):

- AmazonEC2FullAccess
- IAMFullAccess
- AmazonVPCFullAccess

## Contributing

Feel free to create issues or pull requests.

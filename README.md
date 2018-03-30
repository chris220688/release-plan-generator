# Release Plan Generator

This application was designed to serve as a deployments pipeline by generating a release plan for a specific environment set up.

In a word that is already taken over by automated deployments and sophisticated pipelines this approach does seem odd and unrealistic, so you better look for a modern alternative! If you are however stuck in a situation (like myself) where updating your pipelines and making your lives easier is not an option, then I hope you might find it useful.

The application is splitted in three major modules:
1. Environments (i.e staging, production)
2. Boxes (i.e webserver, appserver)
3. Modules (i.e application modules, configuration modules, static modules)

Each environment can have multiple boxes and each box multiple modules (applications).

All three modules have separate configuration files which should be self explanatory.

The steps it performs are listed below:

1. Instantiates an environment with boxes and modules (as per configuration files)
2. Parses the artifacts from the 'artifacts' directory and matches them to the modules
3. Generates linux commands for the following tasks:
	a. Create backup directories in the remote boxes
	b. Take backups of the modules to be deployed
	c. Transfer the artifacts to the remote boxes
	d. Deploy the artifacts
	e. Run any SQL scripts
	f. Rollback the release
4. Dumbs the commands in the 'output' directory

Although it might look a bit too specific, I tried to make it as abstract as possible so that it can be used for different environments with only a few alterations (mainly in the configuration files).

For now it only generates an output with commands, but it shouldn't be very complicated to extend it so that it can also execute the plan. (Consider python's subprocess, paramiko)


### Requirements

Python3 is required to run this application.


### USAGE

1. Make sure you have set up the environment, boxes and modules configuration files to serve your specific environment.

2. Add the artifacts you want to deploy in the artifacts directory.

3. Add the sql scripts that you want to deploy in the artifacts directory.

4. Run the application from the root directory with the following command:

```
$ bin/generate_commands -e staging -a module_1 module_2 -s module_1-static -c module_1 module_2
```
5. For arguments information run:
```
$ bin/generate_commands -h
```
6. The app will try to match the artifacts with the applications that you listed

7. Once it is done, check the output directory for the "commands.txt" file


### Authors

Chris Liontos

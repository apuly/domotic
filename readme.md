Domotic is a combined set of software application that enabled domotic modules to send their data and request information from a centralized datapoint.
The goal of this project is to have privacy friendly software for making domotic data available to the user.

Domotic consists of 3 tools:
	DomoticControl, which domotic modules connect to in order to send data
	postgresql, for storing data
	postgrest, for making the data availble to third party application

DomoticControl has been designed to easily and quickly extend functionality by adding more plugins.

Domotic is supported on Ubuntu 20.10 and build around docker.
Running build.sh will install docker, docker-compose and the needed docker modules.
Note: python3 needs to be installed to automatically install the correct verion of docker-compose.
If python is not present, it will install the version made available by apt.
The apt version might be outdated, and not properly start domotic.

The DomoticControl application is design to be placed in a secure network environment, so not available from the internet.
Any connection with the internet should be made from postgrest (https://postgrest.org/en/stable/)


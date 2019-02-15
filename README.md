# Placement_algorithm
## Introduction
Increasing demand on different network services makes network operators and big companies to increasethe number and variety of complex proprietary hardware. The combination of increasing operational costs,complex integration and maintenance of such hardware is strong limitation of increasing services. Networkfunction vitalization introduces the different way to architect networks. This technology aims to convertdifferent  network  hardware  with  specific functions  as  a  virtual  services  that  are  running  on the  generalpurpose servers (GPS), network nodes such that those services could be moved to a different locations inthe network instead of needing the installation of new equipment.To make available the transition from the various complex proprietary hardware to easy managed software(virtual  functions/services)  on  the  GPS,  Network  Function  Virtualization  platforms  as  OpenStack appeared. While services require to be properly managed, coordinated, arranged and resources require to be aggre-gated, problems related to automation of network, storage, performance and provisioning appear. Frequentlyautomation closely relates to an orchestration (coordination of the resources and networks needed to set upcloud-based services, applications). Correspondingly the entity responsible for orchestration tasks withoutrequiring direct human interaction is defined as orchestrator.To be able to perform orchestration tasks OpenStack includes the orchestration (Manegement and Or-chestration) service based on MANO framework. Normally orchestrators could be responsible(supervision) for multiple OpenStack clusters. 

## In this repository we provide an implementation of placement algorithm for VNF orchestrators. 

## The program can generate a topology based on the described in the paper model or you may feed the topology in the csv file in the next format:

NODE1, NODE2, Latency between NODE1 and NODE2
NODE3, NODE2, Latency between NODE3 and NODE2
NODE4, NODE3, Latency between NODE4 and NODE3

*Note that nodes (NODE1 and NODE2) can have as digits as characters in the name. Latency between nodes is a numeric value.


## Dependecies:

	- pacman -S tk

	- yaourt python-networkx-1.11 1.11-1

 	- yaourt install decorator
	
	- yaourt python-numpy

	- sudo pip install "matplotlib<3"

Autor:
	Dmytro Shytyi.
		site: https://dmytro.shytyi.net
		mail: contact.dmytro@shytyi.net
License: 
	GPL.

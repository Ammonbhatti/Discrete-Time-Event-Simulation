# Discrete-Time-Event-Simulation
Discrete time event simulation of a single queue and single transmitter packet switch.


This code requires the following python packages
to run :
	- numpy
	- matplotlib

***If you do not have these packages run the following commands in the terminal ***
	pip install numpy 
	pip install matplotlib


Running: 
Simply execute the following command to run files in the terminal. 

	python simulation.py
	python experiment_1.py
	pyhton experiment_3.py

Input: 
	No input is required as the program is written
	in the __main__ function. If you want to try different variable settings
	change them in the program itself. All of the relevent variables are defined 
	at the beginning of the program. 
	arrival_rate= 0.1
	departure_rate= 0.2

Outputs (simulation.py): 
Prints the following to the screen: 
	
	- Total time elapsed in the simulation (note different from #of iterations of the event loop)
	- Average Queue Length 
	- Number of packets lost
	- Proportion of time the server is busy 

	The other programs (experiment_1.py and experiment_2.py) display the
	required graphs of arrival_rate vs. (queue_lenth or server_utilization).

Description: 
	An event loop runs SIMULATION_LENTH times. Each time 
	an event is created it is place on the Global Event List(GEL), which
	is implemented as a python list. The GEL is sorted by event time in decreasing 
	order after an event is placed in it. Statistics variables are incremented
	depending on if the events occur or not (for example packet loss). After event loop
	has ended, the program prints the appropriate statistics to the screen. 
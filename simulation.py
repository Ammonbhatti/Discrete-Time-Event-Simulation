# -*- coding: utf-8 -*-


#package used to sample from the arrival and
#departure distributions.
import numpy as np

MAXBUFFER = 50                 #max packets in queue
print("This is a discrete time event simulation of single" )
print("queue and single transmitter router.")
print("The packet interarrival and departure times are exponentially distributed. ")
ARRIVAL_RATE = float(input("Enter an arrival rate: "))         #packets/time interval
DEPARTURE_RATE = float(input("Enter a departure rate: "))
SIMULATION_LENGTH = 100000
GEL = [] 
buffer = []                 #unlimited buffer space if needed. 
   

class Event : 
    def __init__(self, event_type, current_time): 
        self.event_type = event_type
        self.time_interval = np.random.exponential(1/ARRIVAL_RATE) if event_type == 'a'  \
            else np.random.exponential(1/DEPARTURE_RATE)
        self.event_time = current_time + self.time_interval
 
           
if __name__ == "__main__": 
    
    #variables used to calculate statistics 
    current_time = 0.0
    check_time= 0.0         #for debugging
    buffer_size = 0
    packet_loss = 0
    server_not_busy_time= 0.0
    last_packet_departs = 0.0
    first_packet_arrives = 0.0
    total_queue_length = 0.0

    #first arrival event
    GEL.append(Event('a', current_time))
    GEL.sort(key=lambda x: x.event_time, reverse=True)      

    # runtime = simulation_length * sort_time 
    # about n squared log n. 
    for i in range(SIMULATION_LENGTH): 
        current_event = GEL.pop()
        current_time = current_event.event_time
        
        if(current_event.event_type == 'a'): 
            GEL.insert(0, Event('a', current_time))     #make another arrival event
            if(len(buffer) <= 0): 
                GEL.append(Event('d', current_time))
                buffer.insert(0, 'packet' + str(i))
                buffer_size += 1
                first_packet_arrives = current_time
                server_not_busy_time += first_packet_arrives - last_packet_departs
                
            elif(len(buffer) < MAXBUFFER): 
                buffer.insert(0, 'packet' + str(i))
                buffer_size +=1
            else: 
                packet_loss +=1
                #buffer is full, do nothing
                            
        elif(current_event.event_type == 'd'): 
            buffer_size -= 1
            if(len(buffer)> 0): 
                buffer.pop()
                                    
            #If buffer is still not empty
            if(len(buffer)> 0): 
                GEL.append(Event('d', current_time))    
            else:
                #buffer has no packets, and so the 
                #server is not busy
                last_packet_departs = current_time
                                        
        total_queue_length += buffer_size 
        #sort GEL by event_time 
        GEL.sort(key=lambda x: x.event_time, reverse=True)
    
    server_busy_time = current_time - server_not_busy_time
    print("Total time of simulation: ", current_time)
    print("Average Queue Length: ", total_queue_length/current_time)
    print("Packets Lost: ", packet_loss)
    print("Proportion of time server is busy: ",server_busy_time/current_time)
      


"""
Note: 
    The way I calculated server busy time is to accumulate the time 
    the server was not busy. The time the server is not busy is 
    the time between the LAST_PACKET_DEPARTS and the FIRST_PACKET_ARRIVES. 
    
    server_busy_time = total_time - server_not_busy_time. 
    
    Also total_queue_length is divided by SIMULATION_LENGTH instead of current_time, 
    this will give equal weight to all of the different lengths accross time instead
    of having to weight the differnent based on how much simulation time they existed in. 
    
"""























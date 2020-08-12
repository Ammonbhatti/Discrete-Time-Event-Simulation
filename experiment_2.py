# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 17:50:38 2020

"""

import numpy as np
import matplotlib.pyplot as plt

DEPARTURE_RATE = 1          #mu is 1 packet/second
SIMULATION_LENGTH = 100000

class Event : 
    def __init__(self, event_type, current_time): 
        self.event_type = event_type
        self.time_interval = np.random.exponential(1/ARRIVAL_RATE) if event_type == 'a'  \
            else np.random.exponential(1/DEPARTURE_RATE)
        self.event_time = current_time + self.time_interval
 
        
if __name__ == "__main__": 
    
    #information for plotting
    lambda_range = [ 0.2, 0.4, 0.5, 0.6, 0.8, 0.9]
    maxbuffer_range = [1, 20, 30]
    
    for MAXBUFFER in maxbuffer_range: 
        average_queue_lengths = []
        server_busy_times = []
        
        for ARRIVAL_RATE in lambda_range:
            #variables used to calculate statistics 
            
            GEL = [] 
            buffer = []                 #unlimited buffer space if needed. 
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
                #If the buffer is not empty, then the server 
                #is doing work. 
                
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
    
            server_busy_time = (current_time - server_not_busy_time)/ current_time

            server_busy_times.append(server_busy_time)
            average_queue_lengths.append(total_queue_length/SIMULATION_LENGTH)
        
            print("Packet loss for arrival rate: ",ARRIVAL_RATE, " is ", packet_loss )
        plt.plot(lambda_range, average_queue_lengths)
        plt.title("Arrival Rate vs Average Queue Length/ MAXBUFFER = " + str(MAXBUFFER))
        plt.xlabel("Arrival Rate")
        plt.ylabel("Average Queue Length")
        plt.show()
    
        plt.plot(lambda_range, server_busy_times)
        plt.title("Arrival Rate vs Server Time/ MAXBUFFER = " + str(MAXBUFFER))
        plt.xlabel("Arrival Rate")
        plt.ylabel("Server Busy Proportion")
        plt.show()







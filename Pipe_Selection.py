#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 17:14:01 2021

@author: lochan
"""

import wntr
import pandas as pd
import math

# Filepath
input_file = "11.WG_ADD SS-cpsd-24t-o.inp"

# Create network
wnet = wntr.network.WaterNetworkModel(input_file)

# Network description
#wnet.describe(level=0)
#wnet.describe(level=1)

# Pipe and pump name lists
pipe_list = wnet.pipe_name_list
pump_list = wnet.pump_name_list

# Store the start and end nodes of all the pumps in a list
node_list = list()
for i in pump_list:
    pump = wnet.get_link(i)
    node_list.append(pump.start_node_name)
    node_list.append(pump.end_node_name)

# Explore pipes around the pumps that should not be altered
pipes_to_be_unchanged = list() # List to store pipes around the pumps that should stay unaltered

depth = 4 # How far from the pump should the pipes stay unaltered; 1 depth
# level means pipes immediately connected to the pump nodes
for k in range(depth):
    
    for i in pipe_list:
        pipe = wnet.get_link(i)
        
        for j in node_list:
            if pipe.start_node_name == j:
                pipes_to_be_unchanged.append(i)
                continue
            if pipe.end_node_name == j:
                pipes_to_be_unchanged.append(i)
                continue

    pipes_to_be_unchanged = list(set(pipes_to_be_unchanged)) # Remove any duplicates
    
    for i in pipes_to_be_unchanged:
        pipe = wnet.get_link(i)
        node_list.append(pipe.start_node_name)
        node_list.append(pipe.end_node_name)
        
    node_list = list(set(node_list)) # Remove any duplicates

pipes_to_be_unchanged = list(set(pipes_to_be_unchanged)) # Remove any duplicates

# Filter out from the total pipe list the pipes that are eligible for change
pipe_filtered_list = list()

for i in pipe_list:
    switch = True
    for j in pipes_to_be_unchanged:
        if i == j:
            switch = False
            break
    if switch: pipe_filtered_list.append(i)
 
# Store the store the pipes that are eligible to be modified in a Dataframe
pipe_df = pd.DataFrame()
p_name_list = list()
p_diameter = list()
p_status = list()

for i in pipe_filtered_list:
    pipe = wnet.get_link(i)
    if pipe.status == 1: # Ignore pipes that are 'Closed' by default
        p_name_list.append(i)
        p_diameter.append(pipe.diameter)
        p_status.append(pipe.initial_status)
    
pipe_df['Name'] = p_name_list
pipe_df['Diameter'] = p_diameter
pipe_df['Status'] = p_status

# Sort the pipes in descending order by their diameter
sorted_df = pipe_df.sort_values(by = 'Diameter', ascending = False)

# Select the top 10% by diameter
k = math.ceil(0.1*len(sorted_df))
final_selected_pipes_df = sorted_df[:k]

# Export the selected pipes
final_selected_pipes_df.to_csv('./Top10percent.csv')

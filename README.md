# WNTR
Water network simulation using WNTR

# Pipe_Selection.py
Code to select largest 10% pipes in the network.
Pipes to a certain depth (=4) starting from the pumps are first filtered out.
Next, pipes that are 'Closed' by default are filtered out.
Out of the remaining pipes, the top 10% based on their diameter are selected.
See 'Pipe Selection.pdf' for pictorial illustration.

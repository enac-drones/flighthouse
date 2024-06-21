# Work In Progress ! Example to use Tello quadrotors inside ENAC's Indoor Flight Arena

Obtain PGFlow guidance library :

` ... `


A simple use case is defined inside voliere.json file

A simple simulation can be run just to see the use case with :

`python3 simple_sim.py`



## To fly Tellos in real

#### Obtain required libraries :

DJITello from :


` ... `

Motion Capture (ENAC OptiTrack) :

` ... `


## Fly

- Be sure that you have correctly identified vehicle IDs and OptiTrack rigid Body IDs 
- Correct IP addresses for the Tellos
- Case file corresponds to your flight setup, same obstacles, smae vehicle numbers, etc...

Then;

`python3 tello_example.py`

After the flight, the output will be recorded to voliere_output.json file.

You can view the flight trajectory by

`python3 plot.py`

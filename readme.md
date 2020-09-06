# py_light_mas 

![tag:status:status:development](https://raw.githubusercontent.com/PouceHeure/markdown_tags/v1.10/tags/status/status_development/status_development_red.png)

![tag:language:python3](https://raw.githubusercontent.com/PouceHeure/markdown_tags/v1.10/tags/language/python3/python3_blue.png)


- [py_light_mas](#py_light_mas)
  - [architecture](#architecture)
    - [relation](#relation)
    - [sequence](#sequence)
  - [use lib](#use-lib)
    - [create simulation](#create-simulation)
    - [create environnment](#create-environnment)
    - [create agent](#create-agent)
    - [create a network](#create-a-network)
    - [run simulation](#run-simulation)
  - [examples](#examples)
    - [horse ./examples/horse/](#horse-exampleshorse)
    - [robot ./examples/robot/](#robot-examplesrobot)
    - [morse ./examples/morse/](#morse-examplesmorse)

## architecture 

### relation

![relation](.doc/py_light_mas-relation.png)

### sequence

![sequence](.doc/py_light_mas-sequence.png)

## use lib 

### create simulation 

create a new child class of **Simulation**

```python
class YourSimulation(Simulation):
    def __init__(self, ..., **kargs):
        super(YourSimulation, self).__init__(**kargs)
        # create your env and agents here 
        (...)
```

:warning: all agents need to be declared after this call `super(YourSimulation, self).__init__(**kargs)`, during the parent init call Agent class and informe who is the simulation. 


### create environnment 

create a new child class of **Environnemnt**


``` python 
class YourEnvironnement(Environnemnt):
    
    def __init__(self,...,**kargs):
        super(YourEnvironnement,self).__init__(**kargs)

    def on_event_new_tick(self):
        (...)

    def on_event_show(self):
        (...)
```

For the moment, Environnement doesn't have a constructor, so use init with **kwargs is useless, but if Environnemnt evolves and need parameters your code still working. 

### create agent 

create a new child class of **Agent**

``` python 
class YourAgent(Agent): 

    def __init__(self,...,**kargs):
        super(YourAgent,self).__init__(**kargs)

    def on_event_new_message(self,message): 
        (...)

    def on_event_new_signal(self,message): 
        (...)

    def on_event_new_tick(self,env):
        (...)
``` 

### create a network 

you can create a network where do you want 

```python 
network = Network("localhost")
```

if you want to connect an agent to your network 
```python 
agent = YourAgent("agent1")
agent.connect(network)
```

### run simulation 

```python
sim = YourSimulation(...)
# if you want to manage by yourself the loop run 
while(True): 
    (...)
    sim.run() 
    (...)
# if you want to call loop run already implemented 
sim.run_loop()
```

## examples 

:warning: some examples use pygame=1.9.6

### horse [./examples/horse/](./examples/horse/) 
> each horse goes straight until one touch the obstacle 
 
![example-horse](.doc/horse.gif)

### robot [./examples/robot/](./examples/robot/) 
> robots (black rectangles) research resources (blue rectangles). 


![example-robot](.doc/robot.gif)

### morse [./examples/morse/](./examples/morse/) 

> 2 agents are connected at 2 differents network speak together, one sends morse message and the second replies with: 'ok + the same content'

``` bash 
[name: agent_A_01 address: team_A/192.168.0.0 network: ://team_A aid: 0 type: SenderAgent] success connection to: team_A
[name: agent_B_01 address: team_B/192.168.0.0 network: ://team_B aid: 1 type: ReplierAgent] success connection to: team_B
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: __...._.__._..__..
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok __...._.__._..__..
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: _..__...
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok _..__...
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: ._.___.___...___.
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok ._.___.___...___.
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: .____._.______...
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok .____._.______...
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: ....___.
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok ....___.
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: ___.____.___
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok ___.____.___
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: .._.__...
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok .._.__...
from: team_A/192.168.0.0 to: team_B/192.168.0.0 content: __.
from: team_B/192.168.0.0 to: team_A/192.168.0.0 content: ok __.
```
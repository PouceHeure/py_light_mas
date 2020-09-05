# py_light_mas 

![tag:status:status:development](https://raw.githubusercontent.com/PouceHeure/markdown_tags/v1.10/tags/status/status_development/status_development_red.png)

![tag:language:python3](https://raw.githubusercontent.com/PouceHeure/markdown_tags/v1.10/tags/language/python3/python3_blue.png)


## architecture 

![relation](.doc/py_light_mas-relation.png)


### agent 

create a new child class of **Agent**

you should override some event methods: 
```python 
on_event_new_message(self,message)
on_event_new_signal(self,message)
on_event_new_tick(self,env)
```


## examples 

### car [./examples/car/](./examples/car/) 

![example-car](.doc/car.gif)
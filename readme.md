# Satellite Movement Labeler and Visualizer

This project will contain the commits of the process of training and evaluating a model that can visualize satellite movement and label movement. Currently the project is working on retrieving TLE data from [space-track.org](https://www.space-track.org/auth/login) and cleaning it to prepare it for the use in training on a model.


## Goals:

The end goals of this project is to: 
* develop a model that achieves high scores such as accuracy, recall, precision, and F1 on satallite movement tracking, labeling the start and end of longitudial movements, employing various types of models and techniques to maximize performance.
* plot out the movement of the satallite, labeling specific regions that show the starting and the ending of movements, such as shown below (taken from [Thomas Gonzalez-Roberts' paper](https://www.researchgate.net/publication/357551942_Geosynchronous_Satellite_Maneuver_Classification_and_Orbital_Pattern_Anomaly_Detection_via_Supervised_Machine_Learning)):

![Sample display of a satellite's movement](https://cdn.discordapp.com/attachments/1048496883548557403/1191237694710353950/image.png?ex=65a4b58e&is=6592408e&hm=c9c74dd15aeb20c1b153e265eca4c054bbd1403828ea0d77e9dabde6dad7e2ff&)
    where the notation I<E/W> represents the start of the satellite's shift in the East/West direction and E<E/W> represents the end of the satellite's shift in the East/West direction.


## Credits:

* [space-track.org](https://www.space-track.org/auth/login): For publicly available TLE data on the satellites that we used for traing and evaluation.
* [Thomas Gonzalez-Roberts Paper on this project](https://www.researchgate.net/publication/357551942_Geosynchronous_Satellite_Maneuver_Classification_and_Orbital_Pattern_Anomaly_Detection_via_Supervised_Machine_Learning): for reference and information on satellites  

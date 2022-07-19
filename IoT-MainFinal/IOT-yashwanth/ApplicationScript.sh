#!/usr/bin/env bash

gnome-terminal --tab --title="Humidity Sensor" --command="python simHumiditySensor.py"
gnome-terminal --tab --title="Temperature Sensor" --command="python simTemperatureSensor.py"
gnome-terminal --tab --title="Dust Sensor" --command="python simDustSensor.py"
gnome-terminal --tab --title="tb" --command="python simEquTb.py"
gnome-terminal --tab --title="Temperature Act" --command="python simTemperatureAct.py"
gnome-terminal --tab --title="Dust Act" --command="python simDustAct.py"
gnome-terminal --tab --title="Prod Server" --command="python simProdServer.py"
gnome-terminal --tab --title="Dash App" --command="python ../dash/app.py"
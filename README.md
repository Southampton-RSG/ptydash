# ptydash
A dashboard for PtyPy image reconstruction (https://github.com/ptycho/ptypy)

ptydash creates web based modular graph panels that display mqtt device data in graphical image format.

server.py creates a local webpage that hosts the modular graph images that display the required data. 

mqtt.py uses paho.mqtt to feed an mqtt data stream into image_card.py that deciphers strings of information that can then be translated into graphical image data slides, which are then displayed on the local page. 

using a test data broker server, dummy test data is currently being written to the server and then retrieved to create the graphs as no current live data is available.

the format of the data string is: header:, data, header:, data

this will be refined as the format of live data becomes available and the specifics of the data output are known.

mqtt graphical image cards are configurable in the config.json file with hostname and topic_id, where hostname is the mqtt data broker server address and topic_id is the mqtt subscription topic name.


installation procedure.
use of a python v2.7 virtual environment is suggested. 

1. $ install required system level packages - virtualenv
2. $ clone repository: git clone https://github.com/southampton-RSG/ptydash.git
3. $ cd ptydash
4. $ virtualenv -p ptydash venv
5. $ source venv/bin/activate
6. $ pip install -r requirements.txt (may need updating to add other components)

Running.

1. $ python server.py
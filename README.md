# Basic-Gesture-Controlled-Robot-Game
Basic Gesture Controlled Robot for Basic Games


## Team

| **Name / Surname** | **Linkedin** | **GitHub** |
| :---: | :---: | :---: |
| `Bernardo Perrone De Menezes Bulcao Ribeiro ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/b-rbmp/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/b-rbmp) |
| `Roberta Chissich ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/roberta-chissich/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/RobCTs) |


## Brief description
What it does: Utilize motion sensors to control a robot through hand gestures, which could be used for games or simple tasks. 
Sensors: Use a webcam and simple motion detection software to control a robot’s movements with hand gestures. 
Other: The GUI allows users to switch between different modes of operation (e.g., copycat, rock-paper-scissors).


# Running Tablet Flask Server
```bash
   cd tablet
   .\env\Scripts\activate
   flask --app app run -p 5001
```

# Running Pepper Flask Server
```bash
   cd pepper
   .\env\Scripts\activate
   set FLASK_APP=pepper_server.py
   flask run
```

# Running the Robot
```bash
   go to WSL/Ubuntu
   cd /home/hri_software/docker
   ./run.bash
   docker exec -it pepperhri tmux a

   cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64
   ./naoqi &

   cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64
    ./choregraphe &

    connect virtual robot
   get port from edit preferences virtual robot

   Go to Host (OR WINDOWS, but need to convert the export to set)
   export PEPPER_IP=127.0.0.1 and export PEPPER_PORT=33583
   setx PEPPER_IP "127.0.0.1"  and setx PEPPER_PORT "33583"
   and run pepper_cmd - Should show on Choregraphe


```
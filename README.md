# Basic-Gesture-Controlled-Robot-Game
Basic Gesture Controlled Robot for Basic Games


## Team

| **Name / Surname** | **Linkedin** | **GitHub** |
| :---: | :---: | :---: |
| `Bernardo Perrone De Menezes Bulcao Ribeiro ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/b-rbmp/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/b-rbmp) |
| `Roberta Chissich ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/roberta-chissich/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/RobCTs) |


## Brief description
This project involves developing an interactive system for the Pepper robot to engage with users in two specific games: Rock Paper Scissors and Guess My Gesture. The interaction encompasses Pepper's ability to assume various postures, respond to user inputs via speech or touch, and provide feedback based on the game outcomes. The implementation utilizes Pepper's motion capabilities and natural language processing functionalities.  

### Objectives
1) Enable Pepper to perform specific postures for the games.  
2) Develop an interface for Pepper to interact with users through speech recognition and tactile inputs.  
3) Implement the game logic for Rock Paper Scissors and Guess My Gesture.  
4) Provide a smooth and engaging user experience through dialog management.  

### What it does
Utilize motion sensors to control a robot through hand gestures, which could be used for games or simple tasks. 

**Sensors**: Use a webcam and simple motion detection software to control a robot’s movements with hand gestures. 
**Other**: The GUI allows users to switch between different modes of operation (e.g., Guess My Gesture, Rock Paper Scissors).


## Implementation
### Posture Definitions
Several dictionaries define the joint angles for various postures that Pepper will assume during the games. The postures are expressed in degrees for clarity, except for the hand positions.  

**Rock Paper Scissors Postures**: There are three primary postures defined: Rock, Paper, and Scissors. Each posture is represented by a dictionary containing joint angles for the head, shoulders, elbows, wrists, and hands.  

**Child-Specific Postures**: To cater to interactions with children, additional postures are adapted from the standard ones. These postures ensure that the robot maintains a child-friendly appearance and engagement style.  

Two functions convert the posture dictionaries to arrays that can be used by Pepper's motion service. One function converts the joint angles to radians (except for hand positions), and the other extracts the joint names. Then two main functions control Pepper's posture. One sets a normal posture with predefined joint values, and the other sets a custom posture based on the provided dictionary of joint values.  

## Speech Recognition and Interaction
The robot interacts with the user using speech recognition and predefined dialogues. This interaction is managed through a combination of functions that handle speech recognition and response generation.  

**Speech Recognition (ASR) Functions**: These functions manage the speech recognition process, including resetting the ASR state, starting and stopping the listening process, and retrieving the recognized sentences. They also handle user input validation and provide feedback if the input does not match expected choices.  

**Dialog Management Functions**: A set of functions generates appropriate responses based on the interaction context. These functions define the robot's dialogue for various stages of the games, including initial greetings, game instructions, round outcomes, and game over messages.  


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

## Conclusion
This project successfully implements an interactive system for Pepper to play Rock Paper Scissors and Guess My Gesture games with users. The robot can assume predefined postures, recognize user inputs through speech or touch, and provide appropriate feedback. The implementation emphasizes a user-friendly and engaging experience, leveraging Pepper's motion and speech capabilities. Future improvements could include enhancing the speech recognition accuracy and expanding the range of games and interactions.

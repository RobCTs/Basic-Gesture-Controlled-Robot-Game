# Gesture Controlled Robot Game

## Team

| **Name / Surname** | **Linkedin** | **GitHub** |
| :---: | :---: | :---: |
| `Bernardo Perrone De Menezes Bulcao Ribeiro ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/b-rbmp/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/b-rbmp) |
| `Roberta Chissich ` | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/linkedin.png)](https://www.linkedin.com/in/roberta-chissich/) | [![name](https://github.com/b-rbmp/NexxGate/blob/main/docs/logos/github.png)](https://github.com/RobCTs) |


## Brief description
This project involves developing an interactive system for the Pepper robot to engage with users in two specific games: Rock Paper Scissors and Guess My Gesture. The interaction is facilitated through speech recognition and a tablet interface, allowing users to play the games with the robot. The system includes posture definitions for Pepper, speech recognition functions, and dialog management to provide a smooth and engaging user experience. It leverages a Hand Gesture Recognition machine learning model for the Robot to recognize the user's gestures, which in turn allow for the Rock Paper Scissors and Guess My Gesture games to be played.

### Objectives
1) Implement a gesture recognition system to detect user hand gestures.
2) Develop an interface for Pepper to interact with users through speech recognition and a tablet interface.
3) Implement the game logic for Rock Paper Scissors and Guess My Gesture.  
4) Provide a smooth and engaging user experience through dialog management.
5) Personalize the interaction for children by adapting the robot's postures and dialogues.

## Implementation

### Tablet Interface

The tablet interface is implemented using a Flask server that communicates with the Pepper robot through a REST API. The interface allows users to identify themselves, select a game to play, and interact with the robot during the game. The interface includes the following components:

**User Identification**: Users can enter their name and age to personalize the interaction with the robot. The name and age is stored in the server and used to address the user during the game. Also, the age is used to determine whether the user is a child or an adult, which affects the robot's posture.

**Game Selection**: Users can choose between two games: Rock Paper Scissors and Guess My Gesture.

**Game Interaction**: During the game, users can see the status of the game, including the outcome of each round and the instant feedback of the Hand Gesture Recognition model.

**Game Logic**: The game logic is implemented on the server side, where the game state is maintained, and the outcomes of each round are determined based on the user's input and the robot's choice. The Hand Gesture Recognition model is instantiated to recognize the user's gestures and the VideoCapture class is used to capture the webcam feed, to simulate a pepper camera, since the physical robot is not available.

**Game Over**: After the game is completed, users receive a message indicating the winner and the final score and have the option to play again or exit.

### Pepper Server

The Pepper server implements a bridge between the Pepper Tools Interface, which controls the Pepper robot, and external programs, such as the tablet app. The server manages the interaction between the robot and the user, including posture control, speech recognition, and dialog management. The server includes the following components:

**Posture Definitions**: The server defines the joint angles for various postures that Pepper will assume during the games, including Rock Paper Scissors postures and child-specific postures.

**Speech Recognition and Interaction**: The server manages the speech recognition process, including resetting the ASR state, starting and stopping the listening process, and retrieving the recognized sentences. It also generates appropriate responses based on the interaction context, including initial greetings, game instructions, round outcomes, and game over messages.

## Running the Project

### Running Tablet Flask Server
On Windows:
```bash
   cd tablet
   .\env\Scripts\activate
   flask --app app run -p 5001
```

### Running Pepper Flask Server
On Windows:
```bash
   cd pepper
   .\env\Scripts\activate
   set FLASK_APP=pepper_server.py
   flask run
```

### Running the Robot
On WSL/Ubuntu
```bash
   go to WSL/Ubuntu
   cd hri_software/docker
   ./run.bash
   docker exec -it pepperhri tmux a

   cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64
   ./naoqi &

   cd /opt/Aldebaran/choregraphe-suite-2.5.10.7-linux64
   ./choregraphe &
```

### Connecting the Virtual Robot on Choregraphe to the Pepper Server
On WSL/Ubuntu:
1. Open Choregraphe
2. Edit -> Preferences -> Virtual Robot -> Get the port number
On Windows:
3. setx PEPPER_IP "127.0.0.1"  and setx PEPPER_PORT "33583"

## Conclusion
This project demonstrates the development of a Human Robot Interaction system for the Pepper robot to engage with users in two interactive games. The system leverages speech recognition, gesture recognition, and dialog management to provide a smooth and engaging user experience. The implementation includes a tablet interface for user interaction and a Pepper server for posture control, speech recognition, and dialog management. The system allows users to play Rock Paper Scissors and Guess My Gesture games with the robot, providing instant feedback and personalized interactions. Robot postures are personalized based on the age of the participant. The project showcases the potential of interactive systems for robots to engage with users in a fun and interactive way.
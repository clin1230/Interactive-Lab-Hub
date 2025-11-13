# Distributed Interaction

#### Collaborators: Charlotte Lin (hl2575), Zoe Tseng (yzt2), Le-En Huang (lh764) 
Use of AI for this lab: Claude Sonnet4 for image creation and debugging instructions for the code.

---

## Prep

1. Pull the new changes
2. Read: [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) ([video](https://vimeo.com/15932020))

## Overview

Build interactive systems where **multiple devices communicate over a network** using MQTT messaging. Work in teams of 3+ with Raspberry Pis.

**Parts:**
- A: Learn MQTT messaging
- B: Try collaborative pixel grid demo  
- C: Build your own distributed system

---

## Part A: MQTT Messaging

MQTT = lightweight messaging for IoT. Publish/subscribe model with central broker.

**Concepts:**
- **Broker**: `farlab.infosci.cornell.edu:1883`
- **Topic**: Like `IDD/bedroom/temperature` (use `#` wildcard)
- **Publish/Subscribe**: Send and receive messages

**Install MQTT tools on your Pi:**
```bash
sudo apt-get update
sudo apt-get install -y mosquitto-clients
```

**Test it:**

**Subscribe to messages (listener):**
```bash
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/#' -u idd -P 'device@theFarm'
```

**Publish a message (sender):**
```bash
mosquitto_pub -h farlab.infosci.cornell.edu -p 1883 -t 'IDD/test/yourname' -m 'Hello!' -u idd -P 'device@theFarm'
```

> **💡 Tips:**
> - Replace `yourname` with your actual name in the topic
> - Use single quotes around the password: `'device@theFarm'`

**🔧 Debug Tool:** View all MQTT messages in real-time at `http://farlab.infosci.cornell.edu:5001`

![MQTT Explorer showing messages](imgs/MQTT-explorer.png)

**💡 Brainstorm 5 ideas for messaging between devices**

### ✅ Idea 1: Distributed Game Hub

The **Distributed Game Hub** is a multi-device system where each Raspberry Pi acts as a player station. Users can join simple, fast-paced mini-games such as:

- Rock–Paper–Scissors  
- Reaction-Time Challenge  
- Hot Potato  
- Quick-Tap Duel  

#### 🔧 How It Works
- Each Pi provides input through buttons, a joystick, or gesture sensors.
- Player actions are published to shared MQTT topics (e.g., `hub/game/actions`).
- A referee Pi (or distributed logic) listens to incoming actions, evaluates outcomes, and broadcasts results.
- All Pis update their screens at the same time to reflect the final game state.

#### ⭐ Why This Idea
This idea is a strong example of distributed interaction because it demonstrates:
- Real-time messaging between devices  
- Coordinated state synchronization  
- Fast event processing  
- Multi-user participation across separate devices  

The Game Hub can be easily extended by adding new games or input types.

### ✅ Idea 2: Real-Time Voting & Polling System

The **Real-Time Voting System** creates a distributed polling environment across multiple Raspberry Pis. Any device can start a vote, and all Pis instantly receive the poll information.

#### 🔧 How It Works
- One Pi publishes a poll question to a shared topic (e.g., `hub/vote/start`).
- All Pis display the voting options to their users.
- Each Pi publishes its vote to a corresponding topic such as `hub/vote/player3`.
- A tally Pi collects all votes, counts them, and broadcasts the final result.
- Every device displays the outcome of the vote in real time.

#### ⭐ Why This Idea
The voting system demonstrates:
- Message aggregation from multiple devices  
- Shared state updated through MQTT  
- Distributed consensus building  
- Real-time device-to-device coordination  

This model resembles real-world systems such as collaborative panels, meeting polls, or smart-home decision nodes.

### ✅ Idea 3: Shared To-Do / Household Chore Board

The **Shared To-Do Board** is a distributed system where each Raspberry Pi represents a different roommate or household member. Each person can add, update, or complete tasks on their own Pi, and every update is instantly broadcast to all other devices. A central dashboard Pi displays the combined household task list, making it easy to track chores, shared responsibilities, and ongoing tasks.

#### 🔧 How It Works
- Each Pi allows the user to manage their own tasks (add, complete, delete, update status).
- Task updates are published to shared MQTT topics (e.g., `home/todo/player3/update`).
- A dashboard Pi subscribes to all task topics and maintains an aggregated list of everyone's chores.
- All Pis receive updates in real time and refresh their screens to show the current shared state.

#### ⭐ Why This Idea
This idea is practical and relevant for shared living environments because it demonstrates:
- Real-time distributed state sharing  
- Multi-device coordination for shared responsibilities  
- A clear messaging pattern for updates, synchronization, and aggregation  
- A useful real-world application (household chores, shared shopping lists, studio tasks)

The system can be expanded with features such as due dates, reminders, notifications, or color-coded assignments.


### ✅ Idea 4: Distributed Home Security & Activity Log

The **Home Security Log System** gives each Raspberry Pi a specific role—monitoring motion, sound, door open/close, or user-triggered alerts. Events from all Pis are published and collected into a single timeline on a dashboard Pi.

#### 🔧 How It Works
- Each Pi detects or simulates a household event (e.g., motion detected, noise above threshold, door opened).
- Events are published as messages to topics like `home/security/event`.
- The dashboard Pi logs each event with a timestamp and displays an ongoing feed.
- All Pis react to important alerts (e.g., flashing LED for “door opened”).

#### ⭐ Why This Idea
This concept is realistic because it demonstrates:
- Multi-device monitoring of different event types  
- Distributed event publishing and centralized logging  
- Basic alerting and notification mechanisms  
- Scalable design mirroring real smart-home systems  

It can integrate actual sensors for an advanced version.


### ✅ Idea 5: Multi-Desk Productivity & Focus Sync System

The **Focus Sync System** places a Raspberry Pi on each friend’s desk, allowing everyone to share their current work mode (Deep Work, Light Work, Break). Each device displays not only the user’s status but also updates whenever friends switch modes, creating a gentle, ambient way to stay connected and encourage each other during study sessions or work sprints.

#### 🔧 How It Works
- Each Pi has simple inputs for switching modes (Deep Work / Light Work / Break).
- When a user updates their mode, the Pi publishes a message to `team/focus/userX`.
- All Pis show a synchronized view of everyone’s modes (e.g., LEDs, icons, or color themes).
- Optional: When a friend switches to **Deep Work**, others’ Pis can show a short encouraging message like “Charlotte started focusing — join in!”

#### ⭐ Why Multiple Pis Are Needed
- Friends are physically located at **different desks or rooms**, so each Pi provides local, ambient feedback.
- A single Pi cannot represent multiple users across different locations.
- Multiple devices create a **distributed encouragement network**, where each person’s focus status boosts motivation for the whole group.
- This mirrors real-world multi-desk setups, study groups, or remote collaboration environments.

---

## Part B: Collaborative Pixel Grid

<details>
	<summary><strong>Instructions (Click to Expand)</strong></summary>

Each Pi = one pixel, controlled by RGB sensor, displayed in real-time grid.

**Architecture:** `Pi (sensor) → MQTT → Server → Web Browser`

**Setup:**

1. **Sensor**

#### Light/Proximity/Gesture sensor (APDS-9960)
We use this sensor [Adafruit APDS-9960](https://www.adafruit.com/product/3595) for this exmaple to detect light (also RGB)
 
<img src="https://cdn-shop.adafruit.com/970x728/3595-06.jpg" width=200>

Connect it to your pi with Qwiic connector


<img src="imgs/IMG_0270.jpg" height="200" />
We need to use the screen to display the color detection, so we need to stop the running piscreen.service to make your screen available again

```bash
# stop the screen service
sudo systemctl stop piscreen.service
```

if you want to restart the screen service
```bash
# start the screen service
sudo systemctl start piscreen.service
```
 
2. **Server** (one person on laptop):
```bash
cd "Lab 6"  
source .venv/bin/activate
pip install -r requirements-server.txt
python app.py
```

2. **View in browser:**
   - Grid: `http://farlab.infosci.cornell.edu:5000`
   - Controller: `http://farlab.infosci.cornell.edu:5000/controller`

3. **Pi publisher** (everyone on their Pi):
```bash
# First time setup - create virtual environment
cd "Lab 6"
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-pi.txt

# Run the publisher
python pixel_grid_publisher.py
```

Hold colored objects near sensor to change your pixel!

![Pixel grid with two devices](imgs/two-devices-grid.png)

</details>

**📸 Include: Screenshot of grid + photo of your Pi setup**

![Screenshot 2025-11-12 at 16.50.59 (1)](https://hackmd.io/_uploads/S1TfzYzxZg.png)
![IMG_3285](https://hackmd.io/_uploads/r158zFze-l.jpg)
![IMG_3287](https://hackmd.io/_uploads/S1qUMYzebl.jpg)
![IMG_3289](https://hackmd.io/_uploads/H1FUMKfgZx.jpg)

---

## Part C: Make Your Own

## Game Hub

### **1. Project Description**

A fun interactive game where a **central moderator Pi** runs the game logic and each player interacts with their own Raspberry Pi equipped with a sensors or buttons.  


---

### `Rock Paper Scissors` game

1. Moderator starts → publishes `game/mode = rps`.  
2. Each player selects their move via sensor/button → publishes `game/player/{id}/action = rock/paper/scissors`.  
3. Moderator Pi collects all moves → computes winner → publishes `game/winner`.  
4. Players’ Pis display winner feedback (through Pi TFT display).  

The Game Hub structure allows additional mini-games to be added easily later by defining new MQTT topics and logic.

### 2. Architecture Diagram

#### 🕹️ Hardware Setup

- **1 - Moderator Raspberry Pi** (1 person)
  - Controls all game logic
  - Tracks timing and starting game sessions
- **2 - Player Raspberry Pis** (multiple players)
  - input : Each pi (player) equipped with a `Adafruit mpr121 touch sensors`
  - output feedback : through `Pi TFT` display

#### 🔗 Network & Data Flow

All Raspberry Pis are connected to Wi-Fi and communicate through a shared **MQTT broker**.

#### MQTT Topic Structure
- `game/mode`
- `game/state`
- `game/player/{id}/action`
- `game/winner`

#### Message Flow
Inputs → MQTT messages → Moderator computes → Publishes results → Players display feedback.

#### How to Run This


1. Run server/controller first - 

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python moderator_rps.py
```

2. Modify player ID `PLAYER_ID=<your-playerID>`

3. Run client pis - 

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python player_rps.py
```

sample logs for player -

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python game.py 
Player player2 connected!
Player player2 ready!
Touch an electrode to play:
  - Electrode 0: Rock
  - Electrode 1: Paper
  - Electrode 2: Scissors
Waiting for game to start...

[SEND] paper

==================================================
*** YOU WIN! ***
==================================================


>>> New round starting! Choose your move...
[SEND] scissors

==================================================
You LOST. player1 won.
==================================================


>>> New round starting! Choose your move...
```

sample logs for game moderator - 

```
(venv) pi@raspberrypi:~/Interactive-Lab-Hub/Lab 6 $ python moderator_rps.py

Starting a new round!
Moderator connected!
[RECV] player2 -> paper
[RECV] player1 -> rock
All moves received: {'player2': 'paper', 'player1': 'rock'}

==================================================
RESULT: player2 WINS! (paper beats rock)
==================================================


Starting a new round!
[RECV] player2 -> scissors
[RECV] player1 -> rock
All moves received: {'player2': 'scissors', 'player1': 'rock'}

==================================================
RESULT: player1 WINS! (rock beats scissors)
==================================================
```

### **3. Build Documentation**

Photos of each Pi + sensors

MQTT topics used

Code snippets with explanations

### **4. User Testing**


**Photos**

- waiting for game to start
<img src="https://hackmd.io/_uploads/Hy8G-qMgZl.jpg" width="400">
- new round
<img src="https://hackmd.io/_uploads/Sk8MWqfgZx.jpg" width="400">
- game result
<img src="https://hackmd.io/_uploads/BkUMbcGlZl.jpg" width="400">

[Video Demo](https://youtu.be/FyOj0FAjtRE)

**What did they think before trying:**
(Irene Wu, Jessica Hsiao) thought it was a great idea because the game allows players to interact and compete regardless of physical distance,  as long as their Pis are connected, they can still play together in real time.

**What surprised them:**
They were surprised by how smoothly the game synchronized inputs between players and how quickly the results were announced through the MQTT server. They didn’t expect such low latency in communication between multiple Pis.

> for debugging and hardward issues, we added logs that show each player their selection during gameplay

**What would they change:**
They suggested that **each player**'s Adafruit PiTFT display should show the **current game status**, including what each player chose (rock, paper, or scissors), and the final winner, instead of only showing results on the server console.

> we then added the results screen to display results for each player

## **5. Reflection**

**What worked well?**

The MQTT-based communication worked reliably : each Raspberry Pi was able to send its touch sensor input to the central server almost instantly. The server successfully aggregated player choices and determined the game results in real time. The setup was flexible enough to allow all players to be located in different physical spaces while still feeling connected in the same game session.

**Challenges with distributed interaction**

The main challenge was ensuring consistent timing and synchronization between players. Because each Pi publishes independently, the server had to handle late or missing inputs gracefully. Network latency and Wi-Fi connectivity also introduced occasional delays or dropped messages, which affected how quickly results appeared. Debugging across multiple Pis simultaneously added extra complexity.


**How did sensor events work?**

Each Adafruit MPR121 touch sensor reliably detected touch events from specific electrodes mapped to Rock (0), Paper (1), and Scissors (2). When a touch was registered, the corresponding Pi immediately published the event to the MQTT topic. This created a simple but effective way to capture physical interactions and translate them into digital game actions.

**What would you improve?**

Adding a round timer or “ready” indicator could help synchronize inputs better. Also, implementing a simple Flask or Dash web dashboard could make the game more visual and engaging, showing player icons, choices, and results in real time.

---

## Code Files

**Server files:**
- `app.py` - Pixel grid server (Flask + WebSocket + MQTT)
- `mqtt_viewer.py` - MQTT message viewer for debugging
- `mqtt_bridge.py` - MQTT → WebSocket bridge
- `requirements-server.txt` - Server dependencies

**Pi files:**
- `pixel_grid_publisher.py` - Example (RGB sensor → MQTT)
- `requirements-pi.txt` - Pi dependencies

**Web interface:**
- `templates/grid.html` - Pixel grid display
- `templates/controller.html` - Color picker
- `templates/mqtt_viewer.html` - Message viewer

---

## Debugging Tools

**MQTT Message Viewer:** `http://farlab.infosci.cornell.edu:5001`
- See all MQTT messages in real-time
- View topics and payloads
- Helpful for debugging your own projects

**Command line:**
```bash
# See all IDD messages
mosquitto_sub -h farlab.infosci.cornell.edu -p 1883 -t "IDD/#" -u idd -P "device@theFarm"
```

---

## Troubleshooting

**MQTT:** Broker `farlab.infosci.cornell.edu:1883`, user `idd`, pass `device@theFarm`

**Sensor:** Check `i2cdetect -y 1`, APDS-9960 at `0x39`

**Grid:** Verify server running, check MQTT in console, test with web controller

**Pi venv:** Make sure to activate: `source .venv/bin/activate`


---

## Submission Checklist

Before submitting:
- [ ] Delete prep/instructions above
- [ ] Add YOUR project documentation
- [ ] Include photos/videos/diagrams  
- [ ] Document user testing with non-team members
- [ ] Add reflection on learnings
- [ ] List team names at top

**Your README = story of what YOU built!**

---

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)

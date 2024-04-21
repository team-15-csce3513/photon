![logo](https://github.com/team-15-csce3513/photon/assets/102569626/11f706d9-e817-4725-9b40-e111e3f0dc05)

# PHOTON LASER TAG TEAM-15

Created a Photon Laser Tag System for a Software Engineering course at the University of Arkansas. 

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine.

In order to run the program, be sure to have the following installed on your machine:

```bash
$ pip install -r requirements.txt
```

### Installing


To download the project download the project as a zip file.

1. Clone the repository to your local machine:

    
    (https://github.com/team-15-csce3513/photon.git)
    

2. Navigate to the project directory:

    ```bash
    cd photon/src
    ```
3. Please create a [Supabase](https://supabase.com/) account and initiate a new project with a table named `users`. After setting up your project, go to the project settings and copy the `Project URL` and `service_role` key from the `API` tab. These values should be set as environment variables on your local machine, we have our own .env file provided as a guide to you. You should be able to use your own supabase credentials by replacing the lines of code in the .env file.

Change the name of the .env.example file name to .env and add the Supabase URL and key as shown below.

```bash
SUPABASE_URL='enter_your_url_here'
SUPABASE_KEY='enter_your_key_here'
```

### Running the Program

Be sure to open two terminals one will be for traffic_generator.py and one will be for main.py.

In the traffic_generator, this file generates UDP traffic to act as the Photon Lasertag Equipment.
To run the traffic_generator file, follow the steps below:

```bash
python3 traffic_generator.py
```

When compiling the traffic_generator.py, the program will prompt you to enter 2 equipment IDs for each team. 
For example, you can use the numbers shown:

![generator](https://github.com/team-15-csce3513/photon/assets/118322907/c23002b9-25d2-486a-98b7-d6c36ee17502)


When prompted the `Awaiting game start signal` output, move on to the second terminal opened for running main.py:

To run the main Python file (`main.py`), follow these steps:

```bash
python3 main.py
```
When entering the Equipment ID's in the player entry console, be sure to enter the same numbers you entered in the traffic generator console. While in the player entry console, use the tab key to switch between fields. After registering players for one team, select the other team's first equipment ID field using the mouse and continue. To finalize player registration and proceed to the countdown screen, click Continue or press F5 key. Press F12 key to clear all player entries in the console.


## How do you play?
### 1. Player-Entry Screen:
   
After running: 
```bash 
python3 main.py 
```
You will see the Player Entry Screen pop up on the screen. You enter the player information, and as you enter one thing you click `TAB` to register it and move to the next data for one player. Equipment id needs to be the same as the one entered in traffic_generator but the userID can be any integer. You can make any string your username, but if the username you are entering already exists in the database, it prompts you to enter a new one. And if you use a pre-existing userID, it automatically fills the username from the database.
    
Once you enter player information for both teams, and feel like you need to restart, click `Clear` else click on `Continue` to move to next page.
   
   ![Photon_ A Laser Tag System (kali-linux) 4_19_2024 11_06_00 AM](https://github.com/team-15-csce3513/photon/assets/102569626/ff6e5a44-64a3-493b-b07f-6b320d0ae282)

### 2. Countdown:

Once you click `coninue`, the userID's get registered in the supabase, countdown screen begins by displaying players on both teams and goes on for 30 seconds before starting the game.

   ![Photon_ A Laser Tag System (kali-linux) 4_19_2024 11_06_09 AM](https://github.com/team-15-csce3513/photon/assets/102569626/e3480fdd-7428-4ab5-830e-89e9f8321850)

### 3. Starting Traffic Generator:
After the countdown runs ends, using this traffic generator, you are able to give the commands to the players registered in the supabase to shoot each other. To give the command to shoot, you enter 'n' indicating that you don't want to exit the game. Each time you give the command, you wait till you see the command go through and a player shoots the other team.

![image](https://github.com/team-15-csce3513/photon/assets/102569626/f2e029cd-34f4-458e-a8e6-7b300771a0d3)


### 4. Player Action Screen:
Just like a regular laser tag game, points are given to players who hit someone on the other team. In the center, it displays which player shot and who got hit. As game goes on, the points get accumulated for each team, and after 10 hits, whichever player hits the base gets a "*B*" next to their name to indicate that they hit the other team's base.
   ![image](https://github.com/team-15-csce3513/photon/assets/102569626/2e03c1b7-b927-4109-b40b-44458e1f860c)
   
### 5. Ending Traffic Generator
To end the game, you enter 'y' and end the traffic generator for that session.

![image](https://github.com/team-15-csce3513/photon/assets/102569626/7f6e301e-3189-43d7-8c8c-ea34186d1e85)

### 6. Game Result:
Once the timer runs out, whichever team has the most points wins the game, and get displayed on the results screen. In a situation where both teams scored same points, the game displays that it was in fact a tie. 
 Once the session ends, you get the option to either exit it or restart, which brings you back to the player entry screen. You go through the same process, and replay with scores starting at 0.
   ![image](https://github.com/team-15-csce3513/photon/assets/102569626/d13d7308-882d-4403-a1da-77b54c73c872)

## TEAM CONTRIBUTORS
-------------------------------------
|  Full Name      | Github Username |
|-----------------|-----------------|
|Aaliyah Garcia   |   [aaliyahgarcia](https://github.com/aaliyahgarcia) |
|Giovanni Huesca  |   [GioWPS](https://github.com/GioWPS)        |
|Nadine Filat     |   [nadinefilat](https://github.com/nadinefilat)     |
|Pranav Mahesh    |   [pmahesh29](https://github.com/pmahesh29)|
-------------------------------------

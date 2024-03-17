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
3. Please create a [Supabase](https://supabase.com/) account and initiate a new project with a table named `users`. After setting up your project, go to the project settings and copy the `Project URL` and `service_role` key from the `API` tab. These values should be set as environment variables on your local machine, we have our own .env file provided as a guide to you. You should be able to to use your own supabase credentials by replacing the lines of code in the .env file.

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


#### TEAM CONTRIBUTORS
-------------------------------------
|  Full Name      | Github Username |
|-----------------|-----------------|
|Aaliyah Garcia   |   [aaliyahgarcia](https://github.com/aaliyahgarcia) |
|Giovanni Huesca  |   [GioWPS](https://github.com/GioWPS)        |
|Nadine Filat     |   [lilnadine](https://github.com/lilnadine)     |
|Pranav Mahesh    |   [pmahesh29](https://github.com/pmahesh29)|
-------------------------------------


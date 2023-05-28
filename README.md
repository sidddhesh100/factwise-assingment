Project-Management-Tool 

This is CRUD application is used to manage users, teams, boards, task and there details. This application contains several api which we are used for the project management. This application has 3 modules which mentioned below with brief description:

1. User
    This is first module of the project where the user's related operation are get performed which incldes creating a new user, we get the details of the and if needed then we update the user details also.

2. Team
    After creating a user in the system the next step is to assing that user into the specific team but before assinging the user in any team first we have to create that team if it's not exist in the system. Also we can update the team, add the users into and every team will have one admin from the users and every user can have only one team.

3. Board
    This is the important module of the project where we create a boards and task for the team and also manage those created boards and task, One team can have multiple boards and and one user can have multiple task from that board.



The tech stack used: Python, Flask and MongoDB

In this project I have created a total 18 api from which 6 api's for board and task management, 5 api's for the user management and remaining 7 api for the team management all these api's endpoint and logic behind this are as follow
1. User
    i. /create_user
        This api end point is used to create a new user. Its takes user name, disaply_name and description details and in this details the user name should be unique if that user name alredy exist in the system then it will not create that and will show you an error and will ask you to change the user name and after succesfully completing this it will returns the successful response

    ii. /get_user_list
        This api end-point does not required any input. This will check the if users are available or not if they are available in system then it will return all the users and their details as response

    iii. /describe_user
        This api end-point takes user id as query params on the basis of that I am finding the user in the system and will return user's description as response

    iv. /update_user
        This api end-point we can used to update the details of the existing user. This takes user id, and user object which contains users details which we have to update and after successfully updating this it will returns the successful response

    v. /get_team_details_for_user
        This api end-point is used to get the team details of that user from the system this taking  user id as query param and returning the user's team details if he is assing to any team

2. Team
    i. /create_team
        This api endpoint is used to create a new team in the system the team name must be unique if that team name is already exist then system will not allows you to create new team it will ask you to change the team name

    ii. /get_team_list
        This api end-point dose not required any input it will return all the available team from the system

    iii. /describe_team
        This will help us to know the team description by taking team id as a query parameter.

    iv. /update_team
        This will help us to update the team details of which are name, descriptiona and the admin of the team will return the succesful response

    v. /add_users_to_team
        This api end-point is used to add the user's to the team and  if the user's get added then it will successful response.

    vi. /remove_users_from_team
        This end-point is opposite of this /add_users_to_team end point. This will help us to remove the users from the team

    vii. /list_team_user
        This will take team id as a query param and will return all the user details from respected team

3. Board
    i. /create_board
        This end-point will help us to create a new board and the board name should be unique

    ii. /close_board
        This is used to close board but before closing the board it will check all the task from the board is complete then only it will allow you to close the board

    iii. /add_task
        This end-point is help us to create or add a task in the board

    iv. /update_task_status
        We are tacking the task status in e stages such open, in-progess and closed. The first default stage is open if we want to change that stage another then we can use this end-point by giving task id and and task as an input and if task is exist then it will change the status and will return the success response

    v. /list_boards
        This is taking team id as a query param and returnig the all the task details which that team had

    vi. /export_board
        This api end-point is export the board as text file and will store it in ouput file the name of the file will be board id with .txt suffix and it will return file name as response



exmplain file structure?
modules -team, user, board
ID logic
db structure
and dont forget to mentioned swagger documentation, validation
Why I chose Flask and Mongodb?

==================================================
Project Management Tool
This CRUD application is used to manage users, teams, boards, tasks, and their details. It contains several APIs that are used for project management. The application has three modules with the following brief descriptions:

1. User Module
The User module is responsible for user-related operations, including creating a new user, retrieving user details, and updating user information.

Create User API (/create_user): This API is used to create a new user. It requires user name, display name, and description as input. The user name should be unique, and if it already exists in the system, an error will be returned.
Get User List API (/get_user_list): This API retrieves a list of all users and their details from the system.
Describe User API (/describe_user): This API takes a user ID as a query parameter and returns the user's description.
Update User API (/update_user): This API is used to update the details of an existing user. It requires the user ID and the updated user object.
Get Team Details for User API (/get_team_details_for_user): This API takes a user ID as a query parameter and returns the team details of the user if they are assigned to any team.
2. Team Module
The Team module handles team-related operations, including creating teams, retrieving team details, updating teams, and managing team members.

Create Team API (/create_team): This API is used to create a new team in the system. The team name must be unique, and if it already exists, the creation will be rejected.
Get Team List API (/get_team_list): This API retrieves a list of all available teams from the system.
Describe Team API (/describe_team): This API takes a team ID as a query parameter and returns the team's description.
Update Team API (/update_team): This API is used to update team details such as name, description, and admin. It requires the team ID and the updated team object.
Add Users to Team API (/add_users_to_team): This API is used to add users to a team.
Remove Users from Team API (/remove_users_from_team): This API is used to remove users from a team.
List Team Users API (/list_team_user): This API takes a team ID as a query parameter and returns the details of all users in the team.
3. Board Module
The Board module is responsible for creating and managing boards and tasks within teams.

Create Board API (/create_board): This API is used to create a new board within a team. The board name must be unique.
Close Board API (/close_board): This API is used to close a board. However, before closing the board, it checks if all tasks within the board are completed.
Add Task API (/add_task): This API is used to create or add a task to a board.
Update Task Status API (/update_task_status): This API is used to update the status of a task. The task status can be changed between "Open," "In Progress," and "Closed."
List Boards API (/list_boards): This API takes a team ID as a query parameter and returns the details of all boards and tasks within that team.
Export Board API (/export_board): This API exports a board as a text file and stores it in the output file. The name of the file will be the board ID with a .txt suffix, and the API returns the file name as a response.
Tech Stack
The project is developed using Python, Flask, and MongoDB.

Please note that this is a hypothetical README.md file, and the described API endpoints and logic may not be fully functional or implemented.
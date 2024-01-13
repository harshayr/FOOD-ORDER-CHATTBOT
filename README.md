<h1>FOOD ORDERING CHATBOT </h1>

## Overview

The Food Order Chatbot is a conversational AI designed to simplify the food ordering process. This chatbot allows users to browse a menu, place orders, and receive updates on their order status. It aims to enhance the user experience by providing a seamless and interactive ordering platform.

I have created a dummy sql-database for storing information of placed order each order get assign by unique order id using that id we can extract information about particuler order when customer wants to track order


## Technologies 

* Mysql database for storing information of all placed orders for tracking pupose 

* [Dialogflow](https://dialogflow.cloud.google.com) provides basic framwork for chatbot

* [ngrok](https://ngrok.com/download) to get https url to connect dialogflow with backend

## Features

* Menu Exploration: Users can view the available menu items and their descriptions.
* Order Placement: Place orders for desired items directly through the chatbot.
* Order Tracking: Receive real-time updates on the status of placed orders.
* Customization: Customize orders based on preferences and dietary restrictions.

## Requirements

* [Dialogflow](https://dialogflow.cloud.google.com) account and agent set up using dialogflow.txt.
* Create account on ngrok and download [ngrok](https://ngrok.com/download)
* Python environment to handle backend processing (if applicable).

## Setup & Usage

* Dialogflow Setup:
Create a new agent or import the provided dialogflow.txt file.
Ensure that you have turned on webhook call for all intent by going into each intent scroll dwon and turn on webhook call
Train the agent with necessary intents and entities.

* Backend Setup (if applicable):
Clone the repository.
Install required Python packages.
Set up the backend server and link it with Dialogflow using appropriate webhooks i.e ngrok.
Step1: First clone the repository using
```sh
git https://github.com/harshayr/FOOD-ORDER-CHATTBOT.git
```

Step2: go into current working directory and move ngrok file manualy to this folder
```sh
cd FOOD-ORDER-CHATTBOT
```

Step3: Install prerequisites by pasting below command to your terminal
```sh
pip install -r requirment.txt
```

Step4: Open terminal and go into current working directory using step2 command and after use 
```sh
ngrok http 5000
```

Step5: Copy forwarding https url which will look like (Forwarding = https://7280-103-199-193-46ngrok-free.app)
 
Step6: Past that url into dialogflow fulfillment webhook section and save

Step7: Import database from db folder into mysql

step8: Go to integrations and select web demo copy url and paste in other tab and now you can see a chatbot interface where you can paste a link and get information about product according to your need 

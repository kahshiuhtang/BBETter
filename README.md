# NBA Sports Betting 

## Description

Attempt to use ML techniques predict what are the best sports bets to take.

## Pipeline

1) User enters in a sports bet (or multiple)

2) User chooses a model 

3) Model runs and returns the percentage of bet hitting

4) Calculate the expected value of parlay or bet

5) Show the user

## Training Pipeline

1) Pull data from NBA data site

2) Train model on the new data

3) Update the model used for user pipeline

## Website Features

* Visualization of old data

* Receiving Sports Bet Probability

## Plan

There are two main goals I have in mind:

1) Create a DL model to predict the stats from a given matchup for a player. I think RNN is the best path for this step

2) Use XGBoost to do the same task, or some other tree-based ML technique

Firstly, I need to collect and download the data from NBA_api. NBA_api is really only good for data that is rather small. I will create a RNN and swap the head layer because I will use a dataset of pure games to train those layers. Also, I would need to reduce down the dimensions because there are way too many columns, perhaps using PCA. I am not sure about the training aspect, but it should be doable locally. I want to be able to continuously update the model, so perhaps I will need to buy more SSD storage for my local machine. This will require its own head layer.

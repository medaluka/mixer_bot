# mixer_bot Discord Bot README

## Introduction

This Discord bot is designed to manage team compositions and map selections for your 5v5 CS2 games.
It includes commands for mixing teams, selecting maps.

## Features

- **Mix Teams**: Randomly mix 10 players into two teams.
- **Mix Maps**: Randomly select a map from a predefined pool or user-provided list.
- **Mix All**: Mix players into two teams of 5 and select a random map from the predefined pool.

## Setup and Configuration

### Prerequisites

- Python 3.7+
- Discord.py library
- Flask library


### USAGE:

!mix_teams or !mix_team - Mix 10 provided players into two random teams of 5.
ex. !mix_teams Alice Bob Carol Dave Eve Frank Grace Heidi Ivan Judy

!mix_map or !mix_maps - Select a random map from a predefined pool or from a user-provided list.
predefined map pool: Dust2 Mirage Inferno Nuke Train Vertigo Ancient Anubis Cache
ex. !mix_map Dust2 Mirage Inferno Nuke - returns 1 random map from provided list (Dust2 Mirage Inferno Nuke)
ex. !mix_map - returns 1 random map from a predefined map pool (Dust2 Mirage Inferno Nuke Train Vertigo Ancient Anubis Cache)

!mix_all - Mix 10 provided players into two teams of 5 and select a random map from the predefined map pool.
ex. !mix_all Alice Bob Carol Dave Eve Frank Grace Heidi Ivan Judy

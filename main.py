"""
Main Entry Point for the Misioneros y Canibales Problem.

The problem consists of three missionaries and three cannibals who need to cross a river using a boat that can carry at most two people. The goal is to get all missionaries and cannibals across the river without ever leaving more cannibals than missionaries on either side of the river.

## Rules
1. The boat can carry one or two people.
2. At no point should the number of cannibals exceed the number of missionaries on either side of the river.
3. The objective is to move all missionaries and cannibals from one side of the river to the other.
"""
from src import game

def main():
    app = game.Game()
    app.run()

if __name__ == "__main__":
    main()

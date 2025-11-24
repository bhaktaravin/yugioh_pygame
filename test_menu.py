#!/usr/bin/env python3
"""
Simple test script to run the Yu-Gi-Oh main menu
"""
from menu.game import Game

if __name__ == "__main__":
    print("Starting Yu-Gi-Oh! Duelist of the Roses - Main Menu Test")
    game = Game()
    game.run()

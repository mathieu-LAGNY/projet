#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:07:25 2020

@author: mathieu
"""

"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "test",
    version = "0.5",
    description = "description interface",
    executables = [Executable("interface.py")],
)
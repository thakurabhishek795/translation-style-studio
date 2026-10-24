#!/usr/bin/env python3
"""
LinguaStyle Studio - Startup Launcher
Run this script to start the local Translation Style & Memory Studio:
    python3 run.py [PORT]
"""

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.server import run_server

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)

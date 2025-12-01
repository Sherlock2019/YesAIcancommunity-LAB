#!/usr/bin/env python3
"""Lottery Wizard page – renders the provided standalone UI inside Streamlit."""

from streamlit.components.v1 import html
import streamlit as st

st.set_page_config(
    page_title="🎱 Lottery Wizard",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# The UI/JS bundle was provided verbatim by product/design. Keep it in sync with
# their handoff so the Streamlit page stays pixel-perfect.
LOTTERY_WIZARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lottery Wizard - EuroMillions Edition</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #764ba2;
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .scraping-section {
            background: #e8f4f8;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid #b8d4e3;
        }

        .scraping-section h3 {
            color: #2c5282;
            margin-bottom: 15px;
        }

        .url-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #b8d4e3;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 10px;
        }

        .scraped-data {
            max-height: 300px;
            overflow-y: auto;
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border: 1px solid #ddd;
        }

        .draw-entry {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
            font-family: monospace;
        }

        .draw-entry:hover {
            background: #f5f5f5;
        }

        .draw-date {
            font-weight: bold;
            color: #2c5282;
            min-width: 100px;
        }

        .draw-numbers {
            display: flex;
            gap: 8px;
        }

        .number-ball-small {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .panel {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .panel h2 {
            color: #495057;
            margin-bottom: 15px;
            font-size: 1.5em;
        }

        .lottery-grid {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 10px;
            margin: 20px 0;
        }

        .number-ball {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            border: 3px solid transparent.

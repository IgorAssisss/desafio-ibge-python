# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 22:44:05 2026

@author: Assis
"""

import requests

url = "https://mynxlubykylncinttggu.supabase.co/auth/v1/token?grant_type=password"

headers = {
    "Content-Type": "application/json",
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im15bnhsdWJ5a3lsbmNpbnR0Z2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUxODg2NzAsImV4cCI6MjA4MDc2NDY3MH0.Z-zqiD6_tjnF2WLU167z7jT5NzZaG72dWH0dpQW1N-Y"
}

payload = {
    "email": "igor.silva2511@gmail.com",
    "password": "@Janela2511"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
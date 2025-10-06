from flask import Flask, request, jsonify, redirect
import os
from app import create_app

# Vercel serverless entry: create app and run WSGI app
app = create_app()

# simple health route
@app.route('/api/health')
def health():
    return jsonify({'status':'ok'})

# redirect root to /api/ (optional)
@app.route('/')
def root():
    return redirect('/api/health')
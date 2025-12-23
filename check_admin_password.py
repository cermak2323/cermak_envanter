#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('instance/envanter_local.db')
cursor = conn.cursor()

# Get admin user
cursor.execute('SELECT id, full_name, username, password, password_hash FROM envanter_users WHERE username="admin" LIMIT 1')
result = cursor.fetchone()

if result:
    print('[ADMIN USER FOUND]')
    print(f'ID: {result[0]}')
    print(f'Full Name: {result[1]}')
    print(f'Username: {result[2]}')
    print(f'Password (stored): {result[3]}')
    print(f'Password Hash: {result[4]}')
    print()
    print('Not: Password is hashed and encrypted. If stored password is empty, use the hash.')
else:
    print('[INFO] No admin user found. Checking all users:')
    cursor.execute('SELECT id, full_name, username, password FROM envanter_users')
    users = cursor.fetchall()
    for user in users:
        print(f'  - ID {user[0]}: {user[1]} (username: {user[2]}, pass: {user[3]})')

conn.close()

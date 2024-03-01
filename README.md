# Live-Chatapp

Live-Chatapp is a real-time chat application built with Django and WebSocket technology. It enables users to communicate seamlessly without the need for page refreshes, utilizing features such as online status, last seen status, and typing indicators.

## Overview
Live-Chatapp revolutionizes the chatting experience by leveraging WebSocket technology to provide instant communication between users. With features like online status updates, last seen notifications, and typing indicators, it offers a dynamic and interactive chatting environment.

## Features
- Real-time messaging using WebSocket technology.
- Online status indication for active users.
- Last seen status updates for offline users.
- Typing indicators for ongoing conversations.
- Simple user account creation and login functionality.

## Installation
To run Live-Chatapp locally, follow these steps:

1. Clone the repository:
https://github.com/Pritimayasahoo/Live-Chatapp.git

2. Navigate to the chat_project directory:
cd chat_project

3. Install dependencies:
pip install -r requirements.txt

4. Install and configure Memurai as the Redis alternative:
- Download and install Memurai from [Memurai website](https://www.memurai.com/download/).
- Configure the Django application to use Memurai as the channel layer. (Refer to Django Channels documentation for details.)

5. Apply database migrations:
python manage.py migrate

6. Start the development server:
python manage.py runserver



## Usage
1. Access the application at `http://localhost:8000` in your web browser.
2. Sign up for a new account using your email and password.
3. Log in to start chatting with other users in real-time.
4. Experience the seamless messaging experience with instant updates on online status, last seen status, and typing indicators.

## Tech Stack
- Django
- Django Channels
- HTML
- CSS
- JavaScript
- Memurai (Redis alternative for Windows)







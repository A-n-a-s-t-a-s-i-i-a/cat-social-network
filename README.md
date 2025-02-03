# Cat Network

Welcome to **Cat Network**, a Django-based social media platform tailored for cat enthusiasts!  
Users can create accounts, share posts, follow other users, and engage with content through likes and comments.

## Features

- **User Profiles**: Custom user model (`CatUser`) that includes fields like age, breed (with a variety of cat breeds to choose from), bio, and profile picture.
- **Posts**: Users can create, update, and delete posts, complete with images.
- **Comments**: Commenting system to foster interaction on posts.
- **Likes**: Like or unlike posts to show appreciation.
- **Followers**: Follow other users to keep up with their latest posts.
- **Search**: Search functionality for finding posts by title or users by username.

## Models Overview

- **CatUser**: Extends Django’s `AbstractUser`. Includes additional fields like `age`, `breed`, `bio`, and `profile_picture`. Users can also have followers.
- **Post**: Represents a user’s post, containing a `title`, `body` and `image`. 
- **Comment**: Attached to posts, allowing users to leave feedback.
- **Like**: Represents a relationship between a user and a post they like.

## Views

- Class-based views for listing, creating, updating, and deleting posts and comments.
- Custom views for handling likes and following/unfollowing users.

## Forms

- **CatUserCreationForm**: Extends Django’s `UserCreationForm` to include additional fields for user registration.
- **PostSearchForm** and **CatSearchForm**: Simple search forms to filter posts and users.

## URLs

- URL patterns to navigate through posts, comments, and user profiles.
- Authentication URLs included for login/logout.

## Getting Started

### Clone the repository:
```sh
git clone https://github.com/A-n-a-s-t-a-s-i-i-a/cat-social-network.git
```

### Install dependencies:
```sh
pip install -r requirements.txt
```

### Apply migrations:
```sh
python manage.py migrate
```

### Create a superuser:
```sh
python manage.py createsuperuser
```

### Run the development server:
```sh
python manage.py runserver
```

## Test User:

login: ruby

pass: user2025


## Link to project
https://cat-social-network.onrender.com/

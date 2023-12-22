# Travel Diary Web Application

## Description
Travel Diary is a web-based application that allows users to document their travel experiences. Users can create an account, log in, add new travel entries, and view their past adventures.

## Features
- **User Authentication**: Secure login and registration system.
- **Add Travel Entries**: Users can add details about their travel experiences.
- **View Personal Diary**: Users can view all their travel stories in one place.
- **User Settings**: Users can update their account settings and view their activity statistics.

## Installation
The application can be used via [http://traveldiary.pythonanywhere.com/](http://traveldiary.pythonanywhere.com/) or installed locally by performing the following steps

### Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/travel-diary.git
   cd travel-diary
   ```

2. **Set up a Virtual Environment (Optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**
   ```bash
   python db_schema.py -c all  # This script should set up your database schema
   ```

5. **Run the Application**
   ```bash
   flask run
   ```

## Usage

- **Register**: New users need to register by providing a username, email, and password.
- **Login**: Users can log in with their username and password.
- **Add Entry**: Logged-in users can add new travel stories.
- **View Diary**: Users can view all their travel stories.
- **Profile**: Users can change their password and view account statistics.

## Contributing
Contributions to the Travel Diary app are welcome. Please fork the repository and submit a pull request.

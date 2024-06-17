# Password Manager

## Overview
The Password Manager is a Python application that allows users to securely store, retrieve, and generate passwords. The passwords are encrypted and stored in an SQLite database. The application uses the `cryptography` library for encryption and `colorama` for enhanced terminal output.

## Features
- **Add New Passwords**: Store service names, usernames, and passwords securely.
- **Retrieve Passwords**: Retrieve and decrypt passwords for specific services.
- **Generate Passwords**: Generate strong random passwords upon user request.
- **Encryption**: Securely encrypts passwords before storing them in the database.
- **Colorful Output**: Enhanced readability with colored terminal output.

## Installation

### Prerequisites
- Python 3.12
- Pip (Python package installer)

### Install Required Libraries
Run the following command to install the required Python libraries:

```sh
pip install cryptography colorama

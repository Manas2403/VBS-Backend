# Project Setup Guide

This guide will walk you through the steps to set up the project environment, install dependencies, run the backend server, create a superuser for Django admin, and set up environment variables.

## Python Environment Setup

### Prerequisites

-   Python version >= 3

### Creating a Python Virtual Environment

1. **Create a New Directory**: Open a terminal and navigate to the directory where you want to create the project.

2. **Create a Virtual Environment**: Run the following command to create a new Python virtual environment:

```bash
   python3 -m venv myenv
```

## Activate the Virtual Environment: Activate the virtual environment using the appropriate command for your operating system:On Windows:

```bash
myenv\Scripts\activate
```

On Unix/macOS:

```bash
source myenv/bin/activate
```

## Clone the Repository: Begin by cloning the project repository to your local machine.

```bash
git clone <repository-url>
```

## Navigate to the Project Directory: Move into the project directory.

```bash
cd <project-directory>
```

## Install Dependencies: Execute the following command to install the required dependencies.

```bash
pip install -r requirements.txt
```

## Once the dependencies are installed, you can start the backend server by running:

```bash
python manage.py runserver
```

### Creating a Superuser for Django Admin

```bash
python manage.py createsuperuser
```

### Setting Up Environment Variables

-   Create a .env File: Create a new file named .env in the root directory of your project.
-   Add Variables: Add all the environment variables required for your project to the .env file in the format VARIABLE_NAME=value

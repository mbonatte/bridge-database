# Interactive Bridge Visualization Web Application

## Overview
This repository contains the code for a web application designed to visualize and provide detailed information about bridges, including data on their construction, location, collapse mechanisms, and flood characteristics. The application includes interactive map features and detailed bridge pages.

## Features
- Interactive map using Leaflet.js to view all bridges and their basic information.
- Detailed pages for each bridge with structured information and photos.
- Responsive design for both desktop and mobile viewing.

## Setup
1. Clone this repository to your local machine.
2. Ensure Python is installed, and then set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
flask --app api\index.py run
```

5. Open a web browser and navigate to http://localhost:5000 to view the app.

## Dependencies
- Flask for backend server.
- Leaflet.js for interactive map functionality.
- OpenStreetMap for base map layers.

## Configuration
Before running the application, you need to set up the necessary environment variables. Create a .env file in the root directory of your project and populate it with your sensitive credentials and configuration settings. Here's an example of what the contents of your .env file should look like:
```bash
NOTION_TOKEN=your_notion_token_here
DATABASE_ID=your_database_id_here
```
The application relies on these environment variables to function properly, so this step is crucial for the setup.

## Contact
For any queries regarding this project, please contact:
- Maurício Bonatte at mbonatte@ymail.com
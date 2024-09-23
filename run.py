# Import the 'os' module to interact with the operating system, such as accessing environment variables
import os

# Import key functions from Flask:
# - Flask: used to create the Flask application instance
# - render_template: used to render HTML templates
# - request: used to handle form data and incoming requests (GET, POST)
# - flash: used to display one-time messages to users (typically for form submission feedback)
from flask import Flask, render_template, request, flash

# Import the 'json' module to work with JSON data (reading and parsing the company data from a file)
import json

# Check if the 'env.py' file exists (usually for storing environment variables locally),
# and if it does, import it to access environment-specific settings like SECRET_KEY.
if os.path.exists("env.py"):
    import env

# Create the Flask application instance
app = Flask(__name__)

# Set the secret key from an environment variable for securely signing session data and flash messages
app.secret_key = os.environ.get("SECRET_KEY")

# Define the route for the homepage
@app.route("/")
def index():
    # Render the "index.html" template when the homepage is accessed
    return render_template("index.html")

# Define the route for the "About" page
@app.route("/about")
def about():
    # Initialize an empty list to hold company data
    data = []
    
    # Open and load the "company.json" file, which contains company info
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
    
    # Pass the company data and title to the "about.html" template
    return render_template("about.html", page_title="About", company=data)

# Define a dynamic route for individual team member pages using their name
@app.route("/about/<member_name>")
def about_member(member_name):
    # Initialize an empty dictionary to hold member details
    member = {}
    
    # Open and load the "company.json" file, which contains team member info
    with open("data/company.json", "r") as json_data:
        data = json.load(json_data)
        
        # Iterate over each object in the company data
        for obj in data:
            # If the URL matches the member_name, assign their data to 'member'
            if obj["url"] == member_name:
                member = obj
    
    # Render the "member.html" template with the specific member's details
    return render_template("member.html", member=member)

# Define the route for the "Contact" page, supporting GET and POST methods
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # Check if the form was submitted via POST method
    if request.method == "POST":
        # Flash a success message to the user with their name
        flash("Thanks {}, we have received your message!".format(
            request.form.get("name")))
    
    # Render the "contact.html" template with the "Contact Us" title
    return render_template("contact.html", page_title="Contact Us")

# Define the route for the "Careers" page
@app.route("/careers")
def careers():
    # Render the "careers.html" template with the "Careers" title
    return render_template("careers.html", page_title="Careers")

# Run the Flask application
if __name__ == "__main__":
    app.run(
        # Set the host and port from environment variables, with defaults
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        # Enable debug mode for development (disable in production)
        debug=True
    )

# create_env.py

def create_env_file():
    # Define the content of the .env file
    env_content = """
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=universities
CSV_URL=https://api.mockaroo.com/api/501b2790?count=100&key=8683a1c0
    """
    
    # Write the content to a .env file
    with open(".env", "w") as env_file:
        env_file.write(env_content.strip())
    
    print(".env file created successfully!")

if __name__ == "__main__":
    create_env_file()

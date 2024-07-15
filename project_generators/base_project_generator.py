import os


class BaseProjectGenerator:
    def generate(self, project_name: str) -> str:
        """
        Given a project name, create a new dir and a generic Dockerfile.
        Returns the path to the Dockerfile.
        """
        # Create the project directory
        project_dir = os.path.join(os.getcwd(), 'my_solutions', project_name)
        src_dir = os.path.join(project_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)

        # Define a generic Dockerfile content
        dockerfile_content = """
        # Use an official runtime as a parent image
FROM <runtime_image>

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any dependencies
RUN <install_command>

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD [ "<start_command>" ]
        """

        # Write the Dockerfile to the project directory
        dockerfile_path = os.path.join(project_dir, 'Dockerfile')
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content.strip())

        # Create a README file with guidelines
        readme_content = f"""
        # {project_name}

## Project Setup

1. **Install Dependencies**: Ensure you have Docker installed.
2. **Build the Docker Image**: Run the following command in the project directory:
```
docker build -t {project_name.lower()} .
```
3. **Run the Docker Container**: Start the container using the command:
```
docker run -p 5000:5000 {project_name.lower()}
```

## Dockerfile Guide

- `<runtime_image>`: Replace this with the base image for your chosen language (e.g., `python:3.9-slim`).
- `<install_command>`: Replace this with the command to install your project dependencies (e.g., `pip install -r requirements.txt`).
- `<start_command>`: Replace this with the command to start your application (e.g., `flask run --host=0.0.0.0`).

Adjust the Dockerfile according to your specific project requirements.
        """

        readme_path = os.path.join(project_dir, 'README.md')
        with open(readme_path, 'w') as readme:
            readme.write(readme_content.strip())

        return project_dir

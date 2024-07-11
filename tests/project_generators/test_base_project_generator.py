import os
import shutil
import pytest

from project_generators.base_project_generator import BaseProjectGenerator


@pytest.fixture(scope="function")
def setup_teardown():
    """
    Fixture to set up and tear down the test environment.
    """
    generator = BaseProjectGenerator()
    project_name = 'TestAPIProject'
    project_dir = os.path.join(os.getcwd(), project_name)
    yield generator, project_name, project_dir
    # Clean up
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)


def test_generate_creates_directory(setup_teardown):
    """
    Test if the generate method creates the project directory.
    """
    generator, project_name, project_dir = setup_teardown
    generator.generate(project_name)
    assert os.path.isdir(project_dir)


def test_generate_creates_dockerfile(setup_teardown):
    """
    Test if the generate method creates a Dockerfile in the project directory.
    """
    generator, project_name, project_dir = setup_teardown
    dockerfile_path = generator.generate(project_name)
    assert os.path.isfile(dockerfile_path)
    with open(dockerfile_path, 'r') as file:
        content = file.read()
    assert 'FROM <runtime_image>' in content
    assert 'WORKDIR /app' in content
    assert 'COPY requirements.txt ./' in content
    assert 'RUN <install_command>' in content
    assert 'EXPOSE 5000' in content
    assert 'CMD [ "<start_command>" ]' in content


def test_generate_creates_readme(setup_teardown):
    """
    Test if the generate method creates a README.md file with guidelines.
    """
    generator, project_name, project_dir = setup_teardown
    generator.generate(project_name)
    readme_path = os.path.join(project_dir, 'README.md')
    assert os.path.isfile(readme_path)
    with open(readme_path, 'r') as file:
        content = file.read()
    assert f'# {project_name}' in content
    assert '## Project Setup' in content
    assert 'docker build -t' in content
    assert 'docker run -p 5000:5000' in content
    assert '## Dockerfile Guide' in content
    assert '<runtime_image>' in content
    assert '<install_command>' in content
    assert '<start_command>' in content

# Use an official Python runtime as the base image
ARG VARIANT="3.10"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}


# Definet the path to the virtual environment
ARG VENV_PATH="/home/vscode/venv"  

# Copy the requirements.txt file to the container
COPY requirements.txt /tmp/pip-tmp/

# Create a virtual environment and activate it
RUN su vscode -c "python -m venv ${VENV_PATH} \
&& ${VENV_PATH}/bin/pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
&& rm -rf /tmp/pip-tmp \ 
&& source ${VENV_PATH}/bin/activate"

# Set the entrypoint to activate the virtual environment
#ENTRYPOINT ["/bin/bash", "-c", "source venv/bin/activate && exec \"$@\"", "--"]

# Set the default command to run when the container starts
#CMD ["python", "app.py"]

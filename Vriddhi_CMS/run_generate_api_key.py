# run_generate_api_key.py

from django.core.management import execute_from_command_line

# Specify the command you want to run as if you were running it from the command line
command = 'generate_api_key'

# Build the command line arguments (replace 'your_project_name' with your actual project name)
args = ['manage.py', command]

# Execute the command
execute_from_command_line(args)


from github import Github

from github import Github, BadCredentialsException, UnknownObjectException

access_token = 'вбей свои данные хуесос'

original_repo_name = 'torvalds/linux'
your_fork_name = 'lap-does-things/linux'
branch_name = 'goida'
base_branch = 'master'  
file_path = 'README'  
commit_message = 'Minor change in the file'
pull_request_title = 'A public letter to Linus'
pull_request_body = """
Dear Linus (not calling u by your last name)
============

Open-Source as a state of software is and always has been aimed at breaking counties' boundaries and allowing progress without interference of politics and discrimination.
If you wish the kernel not abide such principles, on which you settled yourself a long time ago, it should not be marketed as "Open-Source"

After all, how "Open-Source" is it, when you outright cut off a significant part of your backing solely based on your prejudice towards Russian folk?

To all of the insulted ones, as a former RU citizen, I express my apologies for the state we have driven this community to.
And to you, Linus, I wish you find your peace someday, and remember what got you started on the idea of free software. Free - as in freedom.

Goiyda, bratia!
"""

try:
    g = Github(access_token)

    original_repo = g.get_repo(original_repo_name)
    print(f"Accessing original repository: {original_repo_name}")

    your_fork = g.get_repo(your_fork_name)
    
    base_ref = your_fork.get_git_ref(f'heads/{base_branch}')
    print(f"Base branch '{base_branch}' found with SHA: {base_ref.object.sha}")

    your_fork.create_git_ref(ref=f'refs/heads/{branch_name}', sha=base_ref.object.sha)
    print(f"Branch '{branch_name}' created successfully in your fork.")

    file_content = your_fork.get_contents(file_path)
    updated_content = file_content.decoded_content.decode() + "\n# New line added" 

    your_fork.update_file(file_path, commit_message, updated_content, file_content.sha, branch=branch_name)
    print(f"File '{file_path}' updated successfully in branch '{branch_name}'.")

    pull_request = original_repo.create_pull(title=pull_request_title, body=pull_request_body, base=base_branch, head=f'{your_fork.owner.login}:{branch_name}')
    
    print(f'Pull request created: {pull_request.html_url}')

except BadCredentialsException:
    print("Invalid credentials. Please check your access token.")
except UnknownObjectException as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
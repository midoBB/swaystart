import i3ipc
import time

def find_windows(i3):
    thunderbird = None
    todoist = None
    for con in i3.get_tree():
        if con.app_id == "thunderbird":
            thunderbird = con
        elif con.window_class == "Todoist":
            todoist = con
    return thunderbird, todoist

def adjust_layout():
    # Connect to i3
    i3 = i3ipc.Connection()

    # Get the current workspace
    current_workspace = i3.get_tree().find_focused().workspace().num

    # Wait for both windows to be available
    thunderbird, todoist = None, None
    while not thunderbird or not todoist:
        thunderbird, todoist = find_windows(i3)
        if not thunderbird or not todoist:
            print("Waiting for Thunderbird and Todoist windows...")
            time.sleep(3)

    print("Both windows found. Proceeding with layout adjustment.")

    # Move Thunderbird to workspace 7
    thunderbird.command('move container to workspace 7')

    # Move Todoist to workspace 7
    todoist.command('move container to workspace 7')

    # Focus on workspace 7
    i3.command('workspace 7')

    # Create a horizontal split
    i3.command('split h')

    # Move Thunderbird to the left
    thunderbird.command('move left')

    # Move Todoist to the right
    todoist.command('move right')

    # Resize Thunderbird to take up 67% of the screen
    thunderbird.command('resize set 67 ppt')

    # Make sure both windows are visible
    i3.command('layout splitv')

    # Return to the original workspace
    i3.command(f'workspace {current_workspace}')

if __name__ == "__main__":
    adjust_layout()

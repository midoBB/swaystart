import sys
import time
import i3ipc


def find_windows(i3, thunderbird_name, todoist_name):
    thunderbird = None
    todoist = None
    for con in i3.get_tree():
        if con.app_id == thunderbird_name:
            thunderbird = con
        elif con.window_class == todoist_name:
            todoist = con
    return thunderbird, todoist


def is_layout_correct(i3, thunderbird, todoist):
    workspace = thunderbird.workspace().num if thunderbird else None
    # Check if both are on the same workspace
    if (
        workspace is not None
        and todoist.workspace().num == workspace
        and thunderbird.rect.width / (thunderbird.rect.width + todoist.rect.width) > 0.66
    ):
        return True
    return False


def adjust_layout(thunderbird_name, todoist_name):
    # Connect to i3
    i3 = i3ipc.Connection()

    # Wait for both windows to be available
    thunderbird, todoist = None, None
    while not thunderbird or not todoist:
        thunderbird, todoist = find_windows(i3, thunderbird_name, todoist_name)
        if not thunderbird or not todoist:
            print("Waiting for Thunderbird and Todoist windows...")
            time.sleep(3)
    print("Both windows found. Proceeding with layout adjustment.")

    # Check if the layout is already correct
    if is_layout_correct(i3, thunderbird, todoist):
        print("Layout is already correct. No changes needed.")
        return

    # Get the current workspace
    current_workspace = i3.get_tree().find_focused().workspace().num

    # Move Thunderbird to workspace 7
    thunderbird.command("move container to workspace 7")

    # Move Todoist to workspace 7
    todoist.command("move container to workspace 7")

    # Focus on workspace 7
    i3.command("workspace 7")

    # Create a horizontal split
    i3.command("split h")

    # Move Thunderbird to the left
    thunderbird.command("move left")

    # Move Todoist to the right
    todoist.command("move right")

    # Resize Thunderbird to take up 67% of the screen
    thunderbird.command("resize set 67 ppt")

    # Make sure both windows are visible
    i3.command("layout splitv")

    # Return to the original workspace
    i3.command(f"workspace {current_workspace}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <thunderbird_name> <todoist_name>")
        thunderbird_name = "thunderbird-esr"
        todoist_name = "Todoist"
        adjust_layout(thunderbird_name, todoist_name)
        sys.exit(0)
    thunderbird_name = sys.argv[1]
    todoist_name = sys.argv[2]
    adjust_layout(thunderbird_name, todoist_name)
    sys.exit(0)

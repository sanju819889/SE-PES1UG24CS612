
"""Manage IT helpdesk tickets with validation and security checks."""

import json
import os
import shutil
import subprocess
from datetime import datetime
from itertools import count

tickets = {}
_ticket_ids = count(101)
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket and record its creation."""
    try:
        priority = int(urgency)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Urgency must be an integer from 1 to 5."
        ) from error

    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    if audit_trail is None:
        audit_trail = []

    ticket_id = next(_ticket_ids)
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    audit_trail.append(
        f"{user} raised #{ticket_id} at {datetime.now().isoformat()}"
    )
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")

    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")

    tickets[ticket_id]["notes"].append(note)


def close_ticket(ticket_id, password):
    """Close a ticket when the configured admin password is valid."""
    if not ADMIN_PASSWORD:
        raise RuntimeError(
            "Set the HELPDESK_ADMIN_PASSWORD environment variable first."
        )

    if password != ADMIN_PASSWORD:
        return False

    if ticket_id not in tickets:
        return False

    del tickets[ticket_id]
    return True


def unresolved_high_priority():
    """Return IDs of unassigned high-priority tickets."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a host once without invoking a shell."""
    if not hostname or hostname.startswith("-"):
        raise ValueError("Provide a valid hostname or IP address.")

    ping_executable = shutil.which("ping")
    if ping_executable is None:
        raise RuntimeError("The ping executable is not available.")

    return subprocess.run(
        [ping_executable, "-n", "1", hostname],
        shell=False,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    ).returncode


def save_tickets(file="tickets.json"):
    """Save all current tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(tickets, output_file, indent=4)


def main():
    """Run a demonstration of the helpdesk ticket system."""
    ticket_one = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")

    try:
        raise_ticket("joe", "vpn", "-7")
    except ValueError as error:
        print(f"Invalid ticket rejected: {error}")

    assign_ticket(ticket_one, "Tech-Kiran")
    print("Unassigned high priority:", unresolved_high_priority())

    level = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ).strip() or "3"

    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as error:
        print(f"Ticket not created: {error}")

    if ADMIN_PASSWORD:
        close_ticket(ticket_one, ADMIN_PASSWORD)

    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()

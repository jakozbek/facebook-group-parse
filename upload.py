import os
import mailerlite as MailerLite
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

client = MailerLite.Client({"api_key": api_key})


# This function is used to get the group IDs when needed, they are set in the GROUP_IDS env var
def get_group_ids():
    response = client.groups.list(filter={"name": "afc"})
    print(response)


group_ids = os.getenv("GROUP_IDS")

if group_ids is not None:
    group_ids = group_ids.split(",")
    group_ids = [int(group_id) for group_id in group_ids]

if group_ids is None:
    exit("Group IDs not found")


# Upload a subscriber
def upload_subscriber(email: str, fname: str, lname: str):
    print(f"Adding {email} to MailerLite!")
    client.subscribers.create(
        email,
        fields={"name": fname, "last_name": lname},
        groups=group_ids,
    )

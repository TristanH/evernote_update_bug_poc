import os
import time
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient
import datetime
import random

BASE_NOTE_XML_TPL = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>
    <a href="https://www.example.com">Some nice title here</a>
    <br />
    <div>
        <p>
            <br />
        </p>
        <p>
            <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et magna ut sem iaculis imperdiet quis sed diam. Curabitur quis urna vitae arcu iaculis fermentum. Etiam ut mattis justo, vel consectetur erat. Vestibulum tellus ligula, rhoncus at elit in, elementum lobortis enim. Fusce viverra erat vitae eros porttitor mollis. Nunc vel gravida erat. Aenean viverra diam a imperdiet porttitor. Nam pharetra elit in lectus dapibus, sit amet tristique dui pretium. (</span>
            <a
                href="https://www.example.com/h0">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
</div>
    {}
</en-note>
"""

UPDATE_NOTE_XML_TPL = """<div>
        <hr />
        <p>
            <strong>
                <span>Updated: ABC ??, ????.</span>
            </strong>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>This will not show if you open the note in between creation and update. (</span>
            <a
                href="https://www.example.com/h1">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
    </div>
"""


def create_note(note_store, title="Test note"):
    note = Types.Note()
    note.title = title
    note.content = BASE_NOTE_XML_TPL.format("")
    note = note_store.createNote(note)
    return note


def update_note(note, note_store):
    note.content = BASE_NOTE_XML_TPL.format(UPDATE_NOTE_XML_TPL)
    note.updated = round(datetime.datetime.now().timestamp() * 1000)
    note = note_store.updateNote(note)
    return note


def get_client(auth_token):
    client = EvernoteClient(token=auth_token, sandbox=False)
    return client


def main():
    # Get Evernote auth token from environment variable
    auth_token = os.environ.get('EVERNOTE_AUTH_TOKEN')
    if not auth_token:
        print("Please set the EVERNOTE_AUTH_TOKEN environment variable.")
        return

    client = get_client(auth_token)
    note_store = client.get_note_store()

    created_notes = []

    for i in range(5):
        title = "Test note {}".format(random.randint(0, 10000000))
        note = create_note(note_store, title)
        print("Created note with title and GUID:", note.title, note.guid)
        created_notes.append(note)

    print("Waiting for 120 seconds. Please open one or more of the above notes in Evernote web now, then let them be updated...")
    time.sleep(120)

    print("Now, let's update the notes...")
    for note in created_notes:
        client = get_client(auth_token)
        note_store = client.get_note_store()
        note = note_store.getNote(note.guid, True, False, False, False)
        note = update_note(note, note_store)
        print("Updated note", note.title, note.guid)


if __name__ == "__main__":
    main()

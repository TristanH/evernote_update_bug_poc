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
        <p>
            <br />
        </p>
        <p>
            <span>Cras luctus condimentum ipsum, eu tempor nibh volutpat non. Phasellus dapibus et ante sit amet rutrum. Integer ullamcorper risus ut fringilla hendrerit. Maecenas velit metus, tempus ut venenatis a, bibendum nec nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam non nisi interdum, elementum mi et, venenatis est. Donec auctor risus sit amet tempor molestie. Morbi lectus neque, pellentesque non varius iaculis, dapibus vel diam. Sed id bibendum turpis, nec sodales libero. (</span>
            <a
                href="https://www.example.com/h0">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>Maecenas a feugiat orci, a vulputate nisi. Sed tincidunt imperdiet mattis. Maecenas pulvinar pretium eleifend. In nec consequat nibh. Vestibulum ac dapibus purus. Sed eu ligula non ex consequat bibendum. Morbi consectetur turpis sit amet massa semper fermentum. Nam sed volutpat turpis. Nullam iaculis, ex nec interdum dictum, elit velit euismod ipsum, eget lacinia orci nibh sed sem. Quisque nec fringilla orci. Pellentesque mollis feugiat purus sit amet tempor. Sed id egestas magna. Sed lacinia nunc vitae elementum euismod. Ut non velit elit. Nunc facilisis lectus sit amet ultricies semper. Praesent ornare auctor tellus mattis fringilla. (</span>
            <a
                href="https://www.example.com/h0">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>Sed lacus enim, ultrices et aliquet id, semper eu mi. Etiam sem neque, bibendum et leo quis, tempor efficitur felis. Etiam eu felis nisl. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas facilisis leo sed aliquet lobortis. Nunc nunc urna, euismod sed feugiat vel, aliquam sed leo. Ut id eleifend lectus, vitae auctor quam. Etiam interdum nec purus eu sagittis. Fusce tristique tempus justo, vitae commodo felis condimentum at. Donec ut lectus ut lectus sodales pretium eget in dui. Morbi cursus vulputate risus, et volutpat tellus. (</span>
            <a
                href="https://www.example.com/h0">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>Etiam semper convallis felis imperdiet aliquam. Suspendisse a enim ante. Phasellus ac ipsum vel justo commodo bibendum ac sed nulla. Maecenas lectus eros, gravida vitae facilisis sed, mattis finibus massa. Maecenas pellentesque, leo sed elementum tempus, magna turpis feugiat ante, non mollis dui velit at erat. Nulla a rutrum ligula, et ullamcorper justo. Mauris eget nulla urna. Donec lacinia dolor elit, non malesuada arcu pretium et. Curabitur et ex est. Aliquam ut posuere felis, a facilisis sem. Phasellus est odio, dignissim quis sem ut, laoreet malesuada mauris. Nullam sit amet velit eleifend, tempus arcu in, vulputate metus. Mauris tristique pretium sapien, et interdum arcu pretium sed. Integer at leo sit amet augue dignissim condimentum eu vel nisl. Integer facilisis, purus nec blandit faucibus, odio ante sodales tellus, in luctus quam neque vel magna. Fusce a posuere eros, eu molestie massa. (</span>
            <a
                href="https://www.example.com/h0">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
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
            <span>Interdum et malesuada fames ac ante ipsum primis in faucibus. In viverra eget felis vitae tristique. Quisque id finibus tellus. Nunc volutpat lacus vitae pulvinar elementum. Etiam consectetur felis vitae neque hendrerit, id convallis enim blandit. Suspendisse in ante et augue suscipit tincidunt. Integer convallis lectus in tellus finibus accumsan. Sed fermentum mattis quam, ut mattis lectus pulvinar ut. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed elementum dapibus quam. Pellentesque libero ante, luctus quis auctor non, euismod euismod augue. Nullam nec condimentum enim. (</span>
            <a
                href="https://www.example.com/h1">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>Morbi finibus rhoncus metus a egestas. Morbi a sapien sed ipsum tincidunt tincidunt. Etiam ac nunc ut lacus interdum malesuada. Cras rutrum luctus tellus, ac blandit mauris congue eu. Maecenas tincidunt ultricies orci, nec pharetra orci tempor a. Integer accumsan ante ac mattis pellentesque. Maecenas tincidunt massa non laoreet pharetra. Quisque venenatis non odio non egestas. Maecenas vel magna risus. (</span>
            <a
                href="https://www.example.com/h1">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
        </p>
        <p>
            <span>Donec suscipit leo eros, quis euismod tellus mattis at. In hac habitasse platea dictumst. Sed volutpat justo ut eros ornare ultricies. Praesent ut est tincidunt, tristique nunc non, pretium quam. Sed blandit ex eget neque fringilla, nec posuere metus eleifend. Aenean convallis volutpat aliquam. Aliquam erat volutpat. (</span>
            <a
                href="https://www.example.com/h1">
                <span>View Highlight</span>
            </a>
            <span>
    )</span>
        </p>
        <p>
            <br />
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

    for i in range(40):
        title = "Test note {}".format(random.randint(0, 10000000))
        note = create_note(note_store, title)
        print("Created note with title and GUID:", note.title, note.guid)
        created_notes.append(note)

    print("Waiting for 180 seconds...")
    time.sleep(180)

    print("Now, let's update the notes...")
    for note in created_notes:
        client = get_client(auth_token)
        note_store = client.get_note_store()
        note = note_store.getNote(note.guid, True, False, False, False)
        note = update_note(note, note_store)
        print("Updated note", note.id, note.guid)


if __name__ == "__main__":
    main()

# evernote_update_bug_poc

To run:

```
EVERNOTE_AUTH_TOKEN="<YOUR_TOKEN_HERE>" python poc.py
```

It will create 5 notes, some cases it will create eveything correctly but some times we can see only the first content of the note on Evernote missing the last update. We can verify that looking on the note history:

![Evernote screenshot](image.png)
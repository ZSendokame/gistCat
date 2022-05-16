# Gist Cat
Gist Cat is a powerful command-line tool to work with Gists.<br>
Total controll of them; Create, list, update and delete them.

# How-to Install
```
git clone https://github.com/ZSendokame/gistCat; cd gistCat; pip install -r requirements.txt
```

# How-to Use
Login
```sh
python gc.py login --username <Your Username> --token <Your Token>
```

List
```sh
python gc.py list # List current user Gists.
python gc.py list <Username> # List another user Gists. 
```

Download
```sh
python gc.py download <Gist ID>
```

Uploading
```sh
python gc.py upload <File name> --description "Description"
python gc.py upload <File name> --description "Description" --private # If you wan't a private repository.
```

Delete
```sh
python gc.py delete <Gist ID>
```

Updating
```sh
python gc.py update <Gist ID> --file <Modified file> --description "New description if you want."
# You can also add new files using --file flag, instead of adding an existing file. Add a new one that does not exists.
```
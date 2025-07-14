# Document360 API CRUD Console Application

A minimal Python 3.8+ console app that performs Create, Read, Update, and Delete operations on Document360 folders using the **MVP pattern**.

## Features

* Full CRUD with `GET`, `POST`, `PUT`, `DELETE`
* Logs requests/responses
* Handles and validates API errors
* Cleanly structured as Model, View, Presenter

## Quick Setup

```bash
git clone https://github.com/Mithun017/Document360-API-CRUD
cd Document360-API-CRUD
pip install requests
```

Edit the script:

```python
api_token = "your_api_token_here"
```

Run the app:

```bash
python document360_api.py
```

## What It Does

* Task 1: Fetches folders
* Task 2: Creates a new folder
* Task 3: Renames it
* Task 4: Deletes it

## API Endpoints Used

* `GET /v2/Drive/Folders`
* `POST /v2/Drive/Folders`
* `PUT /v2/Drive/Folders/{id}`
* `DELETE /v2/Drive/Folders/{id}`

## Sample Output

```
Success: Folder 'TestFolder_abc123' created with ID: folder_xyz
Success: Folder ID folder_xyz renamed to 'UpdatedFolder_xyz'
Success: Folder ID folder_xyz deleted
```

**Thank You**

# mapping.py
# Generates dataset/drive_map.json with all Google Drive file IDs from your folder

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json, os, time

# --- Your shared Google Drive folder ID ---
FOLDER_ID = "1LdXoaJhB4dry_nIMAlto2_gVrlvdwsU2"

# --- Scopes and auth ---
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)
service = build("drive", "v3", credentials=creds)


def list_all_files(folder_id):
    """Recursively list all files in the folder and subfolders."""
    file_map = {}
    query = f"'{folder_id}' in parents and trashed = false"
    page_token = None
    while True:
        response = (
            service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, mimeType)",
                pageToken=page_token,
                pageSize=1000,  # fetch 1000 per call
            )
            .execute()
        )
        for f in response.get("files", []):
            if f["mimeType"] == "application/vnd.google-apps.folder":
                # recurse into subfolder
                print(f"↳ Scanning subfolder: {f['name']}")
                file_map.update(list_all_files(f["id"]))
            else:
                file_map[f["name"]] = f["id"]

        page_token = response.get("nextPageToken", None)
        if not page_token:
            break
        time.sleep(0.1)  # avoid API rate limits
    return file_map


def main():
    print(" Scanning Google Drive folder for images...")
    all_files = list_all_files(FOLDER_ID)
    print(f" Found {len(all_files)} files.")

    os.makedirs("dataset", exist_ok=True)
    out_path = os.path.join("dataset", "drive_map.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_files, f, indent=2, ensure_ascii=False)

    print(f" Saved mapping to {out_path}")


if __name__ == "__main__":
    main()

# %% IMPORTS

import os
import json
from pathlib import Path

# %% CONFIGS

PROJECT = Path(__file__).parent.parent
FOLDERS = [
    PROJECT / 'A2A',
    PROJECT / 'modelcontextprotocol',
]
BUCKET = "gs://agentoc-data-sources"
BUCKET_DATA = f"{BUCKET}/data"
OUTPUTS = PROJECT / 'outputs'
METADATA = PROJECT / 'metadata.jsonlines'

# %% PROCESSING

with open(METADATA, 'w') as f:
    for folder in FOLDERS:
        for path in folder.rglob('*'):
            try:
                if not path.is_file(): # skip non files
                    continue
                if path.stat().st_size == 0: # skip empty files
                    continue
                # output
                output = OUTPUTS / str(path.relative_to(PROJECT)).replace('/', '__')
                output = output.with_suffix(output.suffix + '.txt')
                output.write_text(path.read_text())
                print("File:", output)
                # metadata
                metadata = {
                    'id': output.name.replace('.txt', '').replace('.', '--'),
                    "structData": {
                        "source": folder.name,
                        "path": str(path.relative_to(folder)),
                    },
                    "content": {
                        "mimeType": "text/plain",
                        "uri": f"{BUCKET_DATA}/{output.name}"
                    }
                }
                jsondata = json.dumps(metadata)
                f.write(jsondata + '\n')
            except Exception as error:
                print(f"Error: {path} - {error}")

# %% UPLOADS

os.system(f"gcloud storage cp {METADATA} {BUCKET}")
os.system(f"gcloud storage cp -r {OUTPUTS}/* {BUCKET_DATA}")

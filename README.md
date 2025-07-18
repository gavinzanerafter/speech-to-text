# speech-to-text

## Example of How to Use Front-end

https://github.com/user-attachments/assets/005920bd-0705-48a6-8b29-2e4cbbc1e65c

## Setup
Clone the repo:
```bash
git clone https://github.com/gavinzanerafter/speech-to-text.git
cd speech-to-text
```

Create & activate virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Pre-download models:

```bash
./init.sh
```

## Run the Server

Run the server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Then, open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API.

# API_Gateway
an api-gate-way for nlp tasks

## Usage

### Docker Compose

for docker compose u have to just type `docker-compose up -d` and `-d` is for ruuning
server in background

### Manual

#### [Backend](./backend/)

* first u need to install `redis-server` on your machine

* then make a python virtualenv using
```html
python -m venv env
```

* make virtualenv activate

* then go to /backend and install dependencies using: 
```html
pip install -r requirements.txt
```

#### [Frontend](./frontend/)

Install dependencies using:

```html
cd frontend
npm i
```

Compile and hot-reload for development using:

```html
npm run dev
```

Compile and minifile for production by running:

```html
npm run build
```
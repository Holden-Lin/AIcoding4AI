The directory of C4_DB is key to deploy a fastapi app to generate text. the project directory could be as follows:
├── C2_LLM_API
│   ├── GenBookIntro.py
│   ├── GetBookInfo.py
│   ├── learning_demos
│   │   ├── get_books.py
│   │   ├── learn_argparse.py
│   │   ├── learn_fire.py
│   │   ├── learn_psutil.py
│   │   ├── openAI_demo.py
│   │   ├── __pycache__
│   │   │   └── openAI_demo.cpython-310.pyc
│   │   ├── testPrompt.py
│   │   └── zpAI_demo.py
│   └── __pycache__
│       ├── GenBookIntro.cpython-310.pyc
│       └── GetBookInfo.cpython-310.pyc
├── C4_DB
│   ├── database
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── __pycache__
│   │   │   ├── crud.cpython-310.pyc
│   │   │   ├── database.cpython-310.pyc
│   │   │   ├── models.cpython-310.pyc
│   │   │   └── schemas.cpython-310.pyc
│   │   └── schemas.py
│   ├── database1125.db
│   ├── gunicorn_conf.py
│   ├── logs
│   │   ├── access.log
│   │   ├── error.log
│   │   └── fastapi.log
│   ├── main.py
│   ├── __pycache__
│   │   ├── gunicorn_conf.cpython-310.pyc
│   │   └── main.cpython-310.pyc
│   ├── sqlalchemy_learn
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── static
│   │   ├── script.js
│   │   └── styles.css
│   └── templates
│       └── index.html
├── common (in this folder, only count_tokens.py is useful)
│   ├── count_tokens.py 
│   ├── functions.py
│   ├── gradient.py
│   ├── __init__.py
│   ├── layers.py
│   ├── multi_layer_net_extend.py
│   ├── multi_layer_net.py
│   ├── optimizer.py
│   ├── __pycache__
│   │   ├── count_tokens.cpython-310.pyc
│   │   └── __init__.cpython-310.pyc
│   ├── trainer.py
│   └── util.py
└── requirements.txt


the server pip list is 
aiosqlite          0.19.0
annotated-types    0.6.0
anyio              3.7.1
cachetools         5.3.2
certifi            2023.11.17
charset-normalizer 3.3.2
click              8.1.7
dataclasses        0.6
distro             1.8.0
exceptiongroup     1.2.0
fastapi            0.104.0
fire               0.5.0
greenlet           3.0.1
gunicorn           21.2.0
h11                0.14.0
httpcore           1.0.2
httpx              0.25.2
idna               3.6
Jinja2             3.1.2
MarkupSafe         2.1.3
openai             1.3.7
packaging          23.2
pip                21.2.4
pydantic           2.5.2
pydantic_core      2.14.5
PyJWT              2.8.0
python-dotenv      1.0.0
requests           2.31.0
setuptools         58.1.0
six                1.16.0
sniffio            1.3.0
SQLAlchemy         2.0.18
sse-starlette      1.6.5
starlette          0.27.0
termcolor          2.3.0
tqdm               4.66.1
typing_extensions  4.8.0
urllib3            2.1.0
uvicorn            0.23.2
zhipuai            1.0.7
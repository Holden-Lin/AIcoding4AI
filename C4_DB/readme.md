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
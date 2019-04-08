# Slack Status Updater

Update your slack status based on configurable triggered events.


# Requirements

* Python3.7


# Installation and usage

1. Create virtual env

```
$ python3.7 -m venv .venv
```

2. Activate virtual env and install dependencies

```
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

3. Create a configuration file

```
(venv)$ cp config.toml.sample config.toml
```

4. Run to generate a slack token

```
(venv)$ python -m ssup
```

5. Run to watch for events and update your status

```
(venv)$ python -m ssup
```

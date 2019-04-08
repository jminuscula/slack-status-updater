
import asyncio
import toml
import ssup.triggers

from ssup.slack import SlackStatusClient


class SlackStatusUpdater:
    """
    Runs an event loop waiting for trigger events and updates
    the slack status when indicated.
    """
    DEFAULT_INTERVAL_SECONDS = 120

    def __init__(self, config):
        self.config = config
        slack_token = config.slack['token']

        self.client = SlackStatusClient(slack_token)
        self.triggers = config.load_triggers()

    async def run(self):
        async for status in self.watch_status_changes():
            if status is not None:
                self.client.set_status(**status)
            else:
                self.client.clear_status()

    async def watch_status_changes(self):
        while True:
            get_status_updates = (
                trigger.get_status_update()
                for trigger in self.triggers
            )

            status = await asyncio.gather(*get_status_updates)
            status = [p for p in status if p is not None]
            yield status[0] if status else None

            check_interval = self.config.general.get('interval', self.DEFAULT_INTERVAL_SECONDS)
            await asyncio.sleep(check_interval)


class SlackStatusConfig:
    """
    Reads and writes required configuration info for the updater,
    and loads trigger classes dynamically.
    """

    def __init__(self, path):
        self.path = path
        with open(path, 'r', encoding='UTF-8') as fconf:
            self.config = toml.load(fconf)

        self.__dict__.update(self.config)

    def save_config(self):
        with open(self.path, 'w', encoding='UTF-8') as fconf:
            toml.dump(self.config, fconf)
        self.__dict__.update(self.config)

    def save_slack_token(self, token):
        self.config['slack']['token'] = token
        self.save_config()

    def load_triggers(self):
        triggers = []
        for trigger_type, trigger_conf in self.config['trigger'].items():
            trigger_class = getattr(ssup.triggers, trigger_type)
            trigger = trigger_class(trigger_conf)
            triggers.append(trigger)
        return triggers

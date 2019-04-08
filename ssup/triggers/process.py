
import psutil


class ProcessEventTrigger():

    def __init__(self, config):
        self.config = config

    def is_process_running(self):
        for p in psutil.process_iter():
            if p.name() == self.config['process_name']:
                return True
        return False

    async def get_status_update(self):
        if self.is_process_running():
            return {
                'text': self.config.get('status_text'),
                'emoji': self.config.get('status_emoji'),
            }

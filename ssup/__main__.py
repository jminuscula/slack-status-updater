
import argparse
import asyncio
import sys

from ssup.slack import get_oauth_token
from ssup.updater import SlackStatusUpdater, SlackStatusConfig


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config',
        dest='config_path', metavar='PATH',
        default='config.toml',
        help='path to configuration file',
    )

    return parser.parse_args(args)


if __name__ == '__main__':
    arguments = parse_arguments(sys.argv[1:])
    config = SlackStatusConfig(arguments.config_path)

    if not config.slack.get('token'):
        token = get_oauth_token(config.slack)
        config.save_slack_token(token)
        sys.exit(0)

    try:
        updater = SlackStatusUpdater(config)
        asyncio.run(updater.run())
    except KeyboardInterrupt:
        pass

#!/usr/bin/env python3

import argparse
import datetime
import json
import sys
import pybird


def convert_datetime(data):
    key = "last_change"
    if type(data) == list:
        for i in range(len(data)):
            if key in data[i].keys():
                data[i][key] = data[i][key].isoformat()
    else:
        if key in data.keys():
            data[key] = data[key].isoformat()

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query BIRD socket for peer status")
    parser.add_argument("peer", nargs="?", help="peer name (default: all peers)")
    parser.add_argument("-s", "--socket", default="/var/run/bird/bird.ctl",
                        help="path to socket file (default: /var/run/bird/bird.ctl)")
    args = parser.parse_args()

    try:
        bird = pybird.PyBird(socket_file=args.socket)
        peer_state = bird.get_peer_status(args.peer)
        print(json.dumps(convert_datetime(peer_state), sort_keys=True, indent=4))
    except FileNotFoundError:
        print("Socket file not found.", file=sys.stderr)
        sys.exit(1)

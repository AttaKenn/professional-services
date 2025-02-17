#!/usr/bin/env python3

# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import slack
from get_firestore_tracked_cases import get_firestore_tracked_cases


def list_tracked_cases(channel_id, channel_name, user_id):
    """
    Display all of the tracked Google Cloud support cases for the current channel
    to the user that submitted the command.

    Parameters
    ----------
    channel_id : str
        unique string used to idenify a Slack channel. Used to send messages to the channel
    channel_name : str
        user designated channel name. For users to understand where their cases are being
        tracked in Slack
    user_id : str
        the Slack user_id of the user who submitted the request. Used to send ephemeral
        messages to the user
    """
    client = slack.WebClient(token=os.environ.get('SLACK_TOKEN'))
    tracked_cases = get_firestore_tracked_cases()

    local_tracked_cases = []
    for tc in tracked_cases:
        if tc['channel_id'] == channel_id:
            local_tracked_cases.append(tc['case'])
    if len(local_tracked_cases) > 0:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=f"Currently tracking cases {local_tracked_cases}")
    else:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=f"There are no cases currently being tracked in this channel")


if __name__ == "__main__":
    channel_id = os.environ.get('TEST_CHANNEL_ID')
    channel_name = os.environ.get('TEST_CHANNEL_NAME')
    user_id = os.environ.get('TEST_USER_ID')
    list_tracked_cases(channel_id, channel_name, user_id)

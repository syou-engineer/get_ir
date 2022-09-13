import os
from slack_sdk.webhook import WebhookClient
from slack_sdk import WebClient


SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


class Slack:
    is_updated = False
    send_message = ""

    def __init__(self) -> None:
        # token = os.environ.get("SLACK_BOT_TOKEN")
        # client = WebClient(token=token)
        self.send_message += f"IR情報が更新されました。\n\n"

    def send(self):
        webhook = WebhookClient(SLACK_WEBHOOK_URL)

        # 更新が無かったらSlackへ送信をしない
        if self.is_updated:
            webhook = WebhookClient(SLACK_WEBHOOK_URL)
            response = webhook.send(text=self.send_message)

    def show(self):
        """デバッグ用"""
        print(self.send_message)

    def message_heading(self, company_name):
        """送信メッセージに会社名を付与"""
        self.is_updated = True
        self.send_message += f"-------------------------------------------\n【{company_name}】\n"

    def message_shaping(self, body, link):
        """メッセージを整形する"""
        self.send_message += f"・{body}\n{link}\n"

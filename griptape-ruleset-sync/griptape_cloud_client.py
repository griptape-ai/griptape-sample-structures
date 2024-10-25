from attrs import define, field, Factory
from urllib.parse import urljoin
import requests
import os


@define
class GriptapeCloudClient:
    api_key: str = field(
        default=Factory(
            lambda: f'{os.environ["GT_CLOUD_API_KEY"]}',
            takes_self=False,
        )
    )
    base_url: str = field(
        default=Factory(
            lambda: f"https://cloud.griptape.ai",
            takes_self=False,
        )
    )
    headers: dict = field(
        default=Factory(
            lambda self: {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            takes_self=True,
        ),
        kw_only=True,
    )

    def create_ruleset(self, alias: str) -> dict:
        url = urljoin(self.base_url, f"/api/rulesets/")
        response = requests.post(
            url, headers=self.headers, json={"name": alias, "alias": alias}
        )
        response.raise_for_status()

        return response.json()

    def update_ruleset(self, ruleset_id: str, ruleset: dict) -> dict:
        url = urljoin(self.base_url, f"/api/rulesets/{ruleset_id}")
        response = requests.patch(url, headers=self.headers, json=ruleset)
        response.raise_for_status()

        return response.json()

    def get_ruleset_by_alias(self, alias: str) -> dict:
        url = urljoin(self.base_url, f"/api/rulesets/")
        response = requests.get(url, headers=self.headers, params={"alias": alias})
        response.raise_for_status()

        rulesets = response.json()["rulesets"]
        if len(rulesets) == 0:
            raise Exception("Ruleset does not exist")
        else:
            return rulesets[0]

    def get_rule(self, rule_id: str) -> dict:
        url = urljoin(self.base_url, f"/api/rules/{rule_id}")
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def create_rule(self, rule: dict) -> dict:
        url = urljoin(self.base_url, f"/api/rules/")
        response = requests.post(url, headers=self.headers, json=rule)
        response.raise_for_status()

        return response.json()

    def update_rule(self, rule_id: str, rule: dict) -> dict:
        url = urljoin(self.base_url, f"/api/rules/{rule_id}")
        response = requests.patch(url, headers=self.headers, json=rule)
        response.raise_for_status()

        return response.json()

from typing import List

from attrs import define, field, Factory
from griptape_cloud_client import GriptapeCloudClient


@define
class RulesetSynchronizer:
    input_artifacts: str = field(kw_only=True)
    ruleset_alias: str = field(kw_only=True)
    griptape_cloud_driver: GriptapeCloudClient = field(
        kw_only=True, default=Factory(lambda: GriptapeCloudClient())
    )

    def sync_ruleset(self) -> None:

        print(f"Syncing ruleset with alias {self.ruleset_alias}...")
        ingested_rules_list = self._extract_rules_from_input_artifacts()

        ruleset = self._get_or_create_ruleset()
        rules = self._get_rules_for_ruleset(ruleset)

        ruleset_rule_ids: List = ruleset["rule_ids"]
        rule_names = map(lambda x: x["name"], rules)

        # Merge the existing rules with the ingested rules
        for ingested_rule in ingested_rules_list:
            if ingested_rule["name"] in rule_names:
                print(f"Rule {ingested_rule['name']} already exists. Updating...")
                rule = next(
                    (item for item in rules if item["name"] == ingested_rule["name"])
                )
                self.griptape_cloud_driver.update_rule(rule["rule_id"], ingested_rule)
            else:
                print(f"Rule {ingested_rule['name']} does not exist. Creating...")
                created_rule = self.griptape_cloud_driver.create_rule(ingested_rule)
                ruleset_rule_ids.append(created_rule["rule_id"])

        ingested_rule_names = map(lambda x: x["name"], ingested_rules_list)
        for rule in rules:
            if rule["name"] not in ingested_rule_names:
                print(
                    f"Rule {rule['name']} does not exist in the ingested rules. Removing from ruleset..."
                )
                ruleset_rule_ids.remove(rule["rule_id"])

        self._update_ruleset_with_rules(ruleset, ruleset_rule_ids)

    def _get_or_create_ruleset(self) -> dict:
        try:
            ruleset = self.griptape_cloud_driver.get_ruleset_by_alias(
                self.ruleset_alias
            )
            return ruleset
        except Exception as e:
            print("Ruleset does not exist. Creating...")
            return self.griptape_cloud_driver.create_ruleset(self.ruleset_alias)

    def _get_rules_for_ruleset(self, ruleset: dict) -> List:
        rule_ids = ruleset["rule_ids"]
        rules = []
        for rule_id in rule_ids:
            rules.append(self.griptape_cloud_driver.get_rule(rule_id))
        return rules

    def _extract_rules_from_input_artifacts(self) -> List:
        ingested_rules = self.input_artifacts.split("\n")

        ingested_rules_list = []
        for ingested_rule in ingested_rules:
            rule_details = ingested_rule.split(": ")
            ingested_rules_list.append(
                {"name": rule_details[0], "rule": rule_details[1]}
            )

        return ingested_rules_list

    def _update_ruleset_with_rules(self, ruleset: dict, ruleset_rule_ids: List) -> None:
        ruleset["rule_ids"] = ruleset_rule_ids
        ruleset_dict = {
            "name": ruleset["name"],
            "description": ruleset["description"],
            "rule_ids": ruleset["rule_ids"],
        }
        self.griptape_cloud_driver.update_ruleset(ruleset["ruleset_id"], ruleset_dict)

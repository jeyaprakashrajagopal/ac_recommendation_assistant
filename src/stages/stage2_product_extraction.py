from dataclasses import dataclass

import pandas as pd

from config.settings import DATASET_PATH
from src.model.interfaces.chat_model_interface import ChatModel
from src.stages.compare_products import compare_products


@dataclass
class StageTwoResult:
    recommendations: str


class ProductExtractionAndMapping:
    def __init__(self, chat_model: ChatModel, system_message: str):
        self.__chat_model = chat_model
        self.__system_message = system_message
        self.df = pd.read_csv(DATASET_PATH)

    def run(self, user_requirement: dict) -> StageTwoResult:
        filtered_df = self.df[
            self.df["price"]
            <= int(round(float(user_requirement["price"].strip().replace(",", ""))))
        ]
        filtered_df["ac_features"] = filtered_df["description"].apply(
            lambda description: self.__product_map_layer(description=description)
        )
        filtered_df["scores"] = filtered_df["ac_features"].apply(
            lambda dataset: compare_products(
                user_requirements=user_requirement, from_dataset=dataset
            )
        )

        top_products = filtered_df.sort_values("scores", ascending=False).head(3)
        top_products = top_products[top_products["scores"] > 3]
        top_products.sort_values("price", ascending=False, inplace=True)
        top_products.drop(columns=["scores", "ac_features"], axis=1, inplace=True)

        return StageTwoResult(recommendations=top_products.to_json(orient="records"))

    def __product_map_layer(self, description):
        messages = [
            {"role": "system", "content": self.__system_message.format(description)},
            {
                "role": "user",
                "content": f"Follow the instructions and output the dictionary in json format for the following AC {description}",
            },
        ]
        response = self.__chat_model.preview_response(
            messages=messages, json_format=True
        )

        return response

    def add_message(self, role, content):
        self.__chat_model.add_message(role=role, content=content)

    def clear_messages(self):
        self.__chat_model.clear_messages()

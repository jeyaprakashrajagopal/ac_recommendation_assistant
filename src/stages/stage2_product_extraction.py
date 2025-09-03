from dataclasses import dataclass
from typing import Dict

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
        self.__df = pd.read_csv(DATASET_PATH)
        self.__VALIDATION_SCORE = 3

    def run(self, user_requirement: Dict) -> StageTwoResult:
        """
        This method runs the product extraction and mapping layer with the following steps
        1. Extracting price that matches user's budget
        2. Extracting features dictionary from product description via mapping layer and stores it in a new column
        3. Computing scores by comparing user requirement and dataset row dictionaries and stores it in scores column
        4. Sorts and Filters the products based on top scores
        5. Sorts top products based on price, then drops unwanted columns for the next conversation

        :param Dict user_requirement: User's requirement dictionary from the previous stage
        :param StageTwoResult: Returns product recommendations in a json string format
        """
        # 1). Extract products within user's expected price range
        filtered_df = self.__df[
            self.__df["price"]
            <= int(round(float(user_requirement["price"].strip().replace(",", ""))))
        ]

        # 2). Features extracted via mapping layer and stored in a separate column as a new feature
        filtered_df["ac_features"] = filtered_df["description"].apply(
            lambda description: self.__product_map_layer(description=description)
        )

        # 3). Calling compare products method for the scores
        filtered_df["scores"] = filtered_df["ac_features"].apply(
            lambda dataset: compare_products(
                user_requirements=user_requirement, from_dataset=dataset
            )
        )

        # 4). Sorts and filters the top products after validation
        top_products = filtered_df.sort_values("scores", ascending=False).head(3)
        top_products = top_products[top_products["scores"] > self.__VALIDATION_SCORE]

        # 5). Sorts top products based on price, then drops unwanted columns for the next conversation
        top_products.sort_values("price", ascending=False, inplace=True)
        top_products.drop(columns=["scores", "ac_features"], axis=1, inplace=True)

        return StageTwoResult(recommendations=top_products.to_json(orient="records"))

    def __product_map_layer(self, description) -> Dict:
        """
        Private method receives the product description, where an LLM extracts all the primary features from it,
        then classifies the values into one of the following categories such as essential, standard, or premium.

        :param str description: Product description that contains all the specifications
        :return Dict: Returns the extracted featues as a dictionary
        """
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
        """
        To add a message in messages history.

        :param str role: The roles of the message such as system, user, or assistant
        :param str content: The system message or user message to be sent
        """
        self.__chat_model.add_message(role=role, content=content)

    def clear_messages(self):
        """
        To clear the messages history of this particular stage since the chat can go on forever with the user.
        """
        self.__chat_model.clear_messages()

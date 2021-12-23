# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset
import datetime
import json

class ActionGetDate(Action):
    def name(self) -> Text:
        return "action_get_date"

    def run(self, dispatcher, tracker, domain):
        f = open('opening_hours.json')
        data = json.load(f)
        f.close()    

        response = """Restaurant open hour is: \n"""
        
        for date in data['items']:
            open_time = data['items'][date]['open']
            close_time = data['items'][date]['close']
            if open_time != close_time:
                response += """{} {} - {}.\n""".format(date, open_time, close_time)
            else:
                response += """{} restaurant is closed.\n""".format(date, open_time, close_time)

        dispatcher.utter_message(response)
        return []

class ActionGetNowDate(Action):
    def name(self) -> Text:
        return "action_get_now_date"

    def run(self, dispatcher, tracker, domain):
        f = open('opening_hours.json')
        data = json.load(f)
        f.close()

        date = datetime.datetime.now()
        date_name = date.date().strftime("%A")
        open_time = data['items'][date_name]['open']
        close_time = data['items'][date_name]['close']

        response = """Restaurant in {} is open from {} to {}.""".format(date_name, open_time, close_time)

        dispatcher.utter_message(response)
        return []

class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher, tracker, domain):
        f = open('menu.json')
        data = json.load(f)
        f.close()
        response = """Menu: \n"""

        for item in data['items']:
            name = item['name']
            price = item['price']
            preparation_time = item['preparation_time']
            preparation_time_str = ""
            if preparation_time >= 1:
                preparation_time_str = str(preparation_time) + " h"
            else:
                preparation_time_str = str(preparation_time * 60) + " min"
            response += """{} - price: {}$, estimated preparation time: {}.\n""".format(name, price, preparation_time_str)

        dispatcher.utter_message(response)
        return []

class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"
        
    async def required_slots(self, slots_mapped_in_domain, dispatcher, tracker, domain):
        order_slot = tracker.slots.get("orderSlotek")
        order_correctly = tracker.slots.get("order_correctly")
        # print("1")
        # print(order_slot)
        # print(order_correctly)
        # print(tracker.slots.get("order_stop"))
        if order_slot is not None:
            if order_correctly is False:
                return ["order_stop", "order_correctly"] + slots_mapped_in_domain
            else:
                return ["order_correctly"] + slots_mapped_in_domain
        return slots_mapped_in_domain

    async def extract_orderSlotek(self, dispatcher, tracker, domain):
        # print("1.2")
        intent = tracker.get_intent_of_latest_message()
        order_slot = tracker.slots.get("orderSlotek")
        if intent == "request_order":
            return {"orderSlotek": None}
        elif order_slot is not None:
            return {"orderSlotek": order_slot}
        else:
            return {"orderSlotek": tracker.latest_message['text']}

    def validate_orderSlotek(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # print("1.3")
        return {"orderSlotek": tracker.get_slot("orderSlotek")}

    async def extract_order_correctly(self, dispatcher, tracker, domain):
        # print("2")
        intent = tracker.get_intent_of_latest_message()
        order_correctly = tracker.get_slot("order_correctly")
        if order_correctly is not None:
            return {"order_correctly": order_correctly}
        return {"order_correctly": intent == "affirm"}

    def validate_order_correctly(self, slot_value, dispatcher, tracker, domain):
        # print("3")
        return {"orderSlotek": tracker.get_slot("orderSlotek"), "order_correctly": tracker.get_slot("order_correctly")}

    async def extract_order_stop(self, dispatcher, tracker, domain):
        # print("4")
        intent = tracker.get_intent_of_latest_message()
        return {"order_stop": intent == "affirm"}

    def validate_order_stop(self, slot_value, dispatcher, tracker, domain):
        # print("5")
        order_stop = tracker.get_slot("order_stop")
        if not order_stop:
            return {"orderSlotek": None, "order_correctly": None, "order_stop": None}
        return {"orderSlotek": tracker.get_slot("orderSlotek"), "order_correctly": tracker.get_slot("order_correctly"), "order_stop": tracker.get_slot("order_stop")}

class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_submit_order"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot("order_stop") is not True:
            # print("Ordered " + str(tracker.get_slot("orderSlotek")))
            dispatcher.utter_message("Food orderd.")
        else:
            dispatcher.utter_message("Ordering canceled.")
        return [AllSlotsReset()]

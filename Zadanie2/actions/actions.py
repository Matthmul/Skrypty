# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
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

        response = """Restaurant in {} open from {} to {}.""".format(date_name, open_time, close_time)

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

class ActionMakeOrder(Action):
    def name(self) -> Text:
        return "action_get_order"

    def run(self, dispatcher, tracker, domain):
        print(tracker.get_slot("order"))
        response = "Your order is:\n"
        response += str(tracker.latest_message['text'])
        dispatcher.utter_message(response)

        dispatcher.utter_message("Are you sure that you want it?")
        return []

class ActionMakeOrder(Action):
    def name(self) -> Text:
        return "action_make_order"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("Food orderd.")
        return []


class ValidateOrderForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_order_form"
    
    async def run(self, slots_mapped_in_domain, dispatcher, tracker, domain):
        order_slot = tracker.slots.get("order_slot")
        if order_slot is not None:
            return ["order_correctly"] + slots_mapped_in_domain
        return slots_mapped_in_domain
    
    async def extract_order_correctly(self, dispatcher, tracker, domain):
        intent = tracker.get_intent_of_latest_message()
        return {"order_correctly": intent == "affirm"}

    def validate_order_correctly(self, slot_value, dispatcher, tracker, domain):
        if tracker.get_slot("order_correctly"):
            return {"order_slot": tracker.get_slot("order_slot"), "order_correctly": True}
        return {"order_slot": None, "order_correctly": None}
        
    def validate_order(self, slot_value, dispatcher, tracker, domain):
        print(f"Order given: {slot_value}")
        return {"first_name": slot_value}
# -*- coding: utf-8 -*-

from tdm.lib.device import DddDevice, EntityRecognizer, DeviceAction, Validity, DeviceWHQuery
import unicodedata

class AndroidDevice(DddDevice):
    CONTACTS = [
        ("contact_1", u"john", "0701234567"),
        ("contact_1", u"约翰", "0701234567"),
        ("contact_2", u"lisa", "0709876543"),
        ("contact_3", u"mary", "0706574839"),
        ("contact_4", u"andy", None),
        ("contact_4", u"安迪", None),
    ]

    def reset(self):
        self.call_result = True

    def set_call_result(self, result):
        self.call_result = result

    class Call(DeviceAction):
        PARAMETERS = ["selected_contact_to_call"]
        def perform(self, selected_contact_to_call):
            return True

    class ContactRecognizer(EntityRecognizer):
        def recognize_entity(self, string):
            result = []
            tokens = string.split(" ")
            for contact_id, contact_name, number in self.device.CONTACTS:
                if self._contact_name_matches_tokens(contact_name, tokens):
                    contact_name = contact_name.capitalize()
                    recognized_entity = {
                        "sort": "contact",
                        "grammar_entry": contact_name,
                        "name": contact_id
                    }
                    result.append(recognized_entity)
            return result

        def _contact_name_matches_tokens(self, contact_name, tokens):
            if self._is_chinese_string(contact_name):
                return self._chinese_contact_name_matches_tokens(contact_name, tokens)
            else:
                return self._non_chinese_contact_name_matches_tokens(contact_name, tokens)

        def _is_chinese_string(self, string):
            return unicodedata.category(string[0]) == 'Lo'

        def _chinese_contact_name_matches_tokens(self, contact_name, tokens):
            for token in tokens:
                if contact_name in token:
                    return True

        def _non_chinese_contact_name_matches_tokens(self, contact_name, tokens):
            contact_name_lower = contact_name.lower()
            for token in tokens:
                if token.lower() == contact_name_lower:
                    return True

    class PhoneNumberAvailable(Validity):
        PARAMETERS = ["selected_contact_to_call"]
        def is_valid(self, selected_contact_to_call):
            for contact_id, contact_tokens, number in self.device.CONTACTS:
                if contact_id == selected_contact_to_call:
                    return number is not None
            return False

    class phone_number_of_contact(DeviceWHQuery):
        PARAMETERS = ["selected_contact_of_phone_number"]
        def perform(self, selected_contact_of_phone_number):
            for contact_id, contact_tokens, number in self.device.CONTACTS:
                if contact_id == selected_contact_of_phone_number:
                    number_entity = {
                        "grammar_entry": number
                        }
                    return [number_entity]

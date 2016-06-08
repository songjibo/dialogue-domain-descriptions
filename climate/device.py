import re

from tdm.lib import device


class ClimateDevice(device.DddDevice):
    class ClimateRecognizer(device.EntityRecognizer):
        """Entity recognizer for Climate"""

        def recognize_entity(self, utterance):
            m = re.search("(\d+) degrees", utterance)
            if m:
                temp = m.group(1)
                recognized_temp = _build_temp_struct(temp)
                return recognized_temp
            return []


    class TemperatureValidity(device.Validity):
        PARAMETERS = ["desired_temperature"]
        
        def is_valid(self, temperature_individual):
           temp = self._temperature_individual_to_int(temperature_individual)
           temp_int = int(temp)
           return (temp_int < 27) and (temp_int > 14)

        def _temperature_individual_to_int(self, individual):
            m = re.match("temperature_(\d+)_", individual)
            return m.group(1)
            
            

    class SetTemperature(device.DeviceAction):
        PARAMETERS = ["current_temperature", "desired_temperature"]
        
        def perform(self, current, desired):
            return True


    class cabin_temperature(device.DeviceWHQuery):
        def perform(self):
            return _build_temp_struct(18)

    class current_temperature(cabin_temperature):
        pass
        
def _build_temp_struct(temperature):
    return [{
            "sort": "temperature",
            "grammar_entry": "%s degrees" % temperature, 
            "name": "temperature_%s_" % temperature,  
            }]


# import sounddevice as sd

# print(sd.query_devices())

# import speech_recognition as sr

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(index, name)
# import speech_recognition as sr

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(index, name)

import speech_recognition as sr

r = sr.Recognizer()

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    try:
        with sr.Microphone(device_index=i) as source:
            print(f"\nTesting device {i}: {name}")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Speak now...")
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            print("Captured audio from device", i)
    except Exception as e:
        pass
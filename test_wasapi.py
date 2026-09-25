import sounddevice as sd

hostapis = sd.query_hostapis()

print("Available Host APIs:")
for i, api in enumerate(hostapis):
    print(i, api['name'])

print("\nDevices with Input Channels:\n")

devices = sd.query_devices()

for i, dev in enumerate(devices):
    if dev['max_input_channels'] > 0:
        hostapi_name = hostapis[dev['hostapi']]['name']
        print(f"{i} | {dev['name']} | HostAPI: {hostapi_name}")
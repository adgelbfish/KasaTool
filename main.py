import PySimpleGUI as sg

import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from kasa import Discover

sg.theme('DarkAmber')

wifi_choices = ['choice 1', 'choice 2']

wifi_chooser = sg.Combo(wifi_choices)

device_name_field = sg.InputText()

device_ip_field = sg.InputText()

device_ip = "192.168.0.1"



layout = [[sg.Text('Device Name'), device_name_field, sg.Button('Set')],
          [sg.Text('Wifi'), wifi_chooser],
          [sg.Text('Password'), sg.InputText(password_char="*")],
          [sg.Button('Turn On'), sg.Button("Turn Off")],
          [sg.Button('Refresh'), sg.Button('Cancel'), sg.Button('Ok and Connect')],
          [sg.Text('Device Ip'), device_ip_field, sg.Button('Switch Device')]]

window = sg.Window('Window Title', layout)



async def update_wifi_list():
    global wifi_choices

    device = await Discover.discover_single(device_ip)
    wifi_networks = await device.wifi_scan()
    wifi_choices = [net.ssid for net in wifi_networks]


async def set_alias(name):

    device = await Discover.discover_single(device_ip)
    await device.set_alias(name)


async def get_alias():

    device = await Discover.discover_single(device_ip)
    return device.alias



async def turn_on():

    device = await Discover.discover_single(device_ip)
    await device.turn_on()


async def turn_off():

    device = await Discover.discover_single(device_ip)
    await device.turn_off()


async def connect_to_wifi(ssid, password):

    device = await Discover.discover_single(device_ip)
    await device.wifi_join(ssid, password)


def set_ip(ip):
    global device_ip
    device_ip = ip
    device_ip_field.update(device_ip)

async def run_event(event, values):
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        exit(0)
    if event == 'Refresh':
        await update_wifi_list()
        wifi_chooser.update(values=wifi_choices)
        alias = await get_alias()
        device_name_field.update(alias)
        window.refresh()
    if event == "Set":
        await set_alias(values[0])
        alias = await get_alias()
        device_name_field.update(alias)
        window.refresh()
    if event == "Turn On":
        await turn_on()
    if event == "Turn Off":
        await turn_off()
    if event == "Switch Device":
        set_ip(values[3])
    if event == 'Ok and Connect':
        await set_alias(values[0])
        await connect_to_wifi(values[1], values[2])



while True:
    event, values = window.read()
    device_ip_field.update(device_ip)
    loop.run_until_complete(run_event(event, values))

window.close()


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

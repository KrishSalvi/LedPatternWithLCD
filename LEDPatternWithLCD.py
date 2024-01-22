#!/usr/bin/python3
# Inspired by : M Heidenreinch (c)
# Programmed By : Arth Raval, Krish Salvi - 12th December 2022

from gpiozero import PWMLED, Button
from threading import Thread
from time import sleep
from smbus import SMBus
import signal
from rpi_lcd import LCD


led_pins = [26, 25, 16, 12, 23, 6, 19, 13]
leds = [PWMLED(pin) for pin in led_pins]

button = Button(22)
bus = SMBus(1)
lcd = LCD()

ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

ptn_1 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1]
]

ptn_2 = [
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1]

]

ptn_3 = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],

]

ptn_4 = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0]
]

ptn_5 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

ptn_6 = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

ptn_7 = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

ptn_8 = [
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1],
]

NUM_PATTERNS = 8

patterns = [ptn_1, ptn_2, ptn_3, ptn_4, ptn_5, ptn_6, ptn_7, ptn_8]

running = True
delay = 0.1
pattern_number = 0
brightness = 1.0

levels = (
            0, 0.000471285480509, 0.000964781961432, 0.001481536214969,
            0.002022644346174, 0.002589254117942, 0.003182567385564,
            0.003803842646029, 0.004454397707459, 0.005135612484362,
            0.005848931924611, 0.006595869074376, 0.007378008287494,
            0.0081970085861, 0.009054607179632, 0.009952623149689,
            0.01089296130854, 0.011877616239496, 0.012908676527678,
            0.013988329190195, 0.015118864315096, 0.016302679918954,
            0.017542287033382, 0.018840315031266, 0.02019951720402,
            0.021622776601684, 0.023113112148259, 0.024673685045253,
            0.02630780547701, 0.028018939632056, 0.02981071705535,
            0.031686938347034, 0.033651583224017, 0.035708818961488,
            0.037863009232264, 0.040118723362727, 0.042480746024977,
            0.044954087385763, 0.047543993733716, 0.050255958607436,
            0.053095734448019, 0.05606934480076, 0.059183097091894,
            0.062443596007499, 0.065857757502918, 0.069432823472428,
            0.073176377110267, 0.077096358995608, 0.081201083935591,
            0.085499258602144, 0.09, 0.09471285480509, 0.099647819614319,
            0.104815362149688, 0.110226443461741, 0.115892541179417,
            0.121825673855641, 0.128038426460288, 0.134543977074593,
            0.141356124843621, 0.148489319246111, 0.155958690743756,
            0.163780082874938, 0.171970085860998, 0.180546071796325,
            0.189526231496888, 0.198929613085404, 0.208776162394955,
            0.219086765276777, 0.229883291901949, 0.241188643150958,
            0.253026799189538, 0.265422870333817, 0.278403150312661,
            0.291995172040202, 0.306227766016838, 0.321131121482591,
            0.336736850452532, 0.353078054770101, 0.370189396320561,
            0.388107170553497, 0.406869383470335, 0.426515832240166,
            0.447088189614875, 0.468630092322638, 0.491187233627272,
            0.514807460249773, 0.539540873857625, 0.565439937337157,
            0.592559586074358, 0.620957344480193, 0.650693448007596,
            0.681830970918936, 0.71443596007499, 0.748577575029184,
            0.784328234724282, 0.821763771102671, 0.860963589956081,
            0.90201083935591, 0.944992586021436, 0.99
        )


def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)


def map_to_brightness(value):
    index = int((value / 255) * (len(levels) - 1))
    return levels[index]


def adjust_brightness():
    global brightness
    while True:
        pot_value = read_ads7830(0)
        brightness = map_to_brightness(pot_value)
        sleep(0.01)


def adjust_speed():
    global delay
    while True:
        pot_value = read_ads7830(1)
        delay = 0.02 + 0.4 * pot_value / 255
        sleep(0.01)


def display_info():
    global pattern_number, brightness, delay
    direction_symbols = [">>", "<<", "||", "<>", ">>", ">>", "<|>", ">>"]

    while running:
        direction = direction_symbols[pattern_number]
        lcd.text(f"Pattern: {pattern_number + 1}/8 {direction}", line=1)
        lcd.text(f"B ={int(brightness * 100)}% | D ={delay:.1f}s", line=2)
        sleep(0.5)


def change_pattern():
    global pattern_number
    pattern_number = (pattern_number + 1) % NUM_PATTERNS


def safe_exit(signum, frame):
    global running
    running = False
    for led in leds:
        led.close()

    lcd.text("Thank you.", line=1)
    lcd.text("Bye Bye", line=2)

    sleep(3)
    lcd.clear()


if __name__ == "__main__":

    signal.signal(signal.SIGTERM, safe_exit)
    signal.signal(signal.SIGHUP, safe_exit)

    button.when_pressed = change_pattern

    brightness_thread = Thread(target=adjust_brightness, daemon=True)
    brightness_thread.start()

    speed_thread = Thread(target=adjust_speed, daemon=True)
    speed_thread.start()

    display_thread = Thread(target=display_info, daemon=True)
    display_thread.start()

    try:
        while True:
            pattern = patterns[pattern_number]
            for row in pattern:
                for led_id, value in enumerate(row):
                    leds[led_id].value = value * brightness
                sleep(delay)

    except KeyboardInterrupt:
        pass

    finally:
        safe_exit(None, None)

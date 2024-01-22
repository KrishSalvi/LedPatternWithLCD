# LED Patterns Display System

## Overview

Welcome to the LED Patterns Display System! This Python script is tailor-made for Raspberry Pi enthusiasts, providing a dynamic LED display with customizable patterns. Whether you're a hobbyist or tinkerer, this system allows you to interact with LEDs, a button, and potentiometers to explore various patterns in a hands-on way.

## Features

- **Pattern Variety:** Eight predefined LED patterns bring visual diversity to your display.
- **User Interaction:** Change patterns effortlessly with a dedicated button.
- **Dynamic Brightness:** Adapt to ambient lighting using a potentiometer for real-time brightness adjustments.
- **Pattern Speed Control:** Tailor the pace of your LED patterns with another potentiometer.
- **LCD Insights:** A connected LCD display keeps you informed about the active pattern, brightness level, and delay time.

## Hardware Requirements

Unlock the full potential of this script with the following hardware components:

- Raspberry Pi
- LEDs connected to GPIO pins
- Button linked to a GPIO pin
- Potentiometers connected to the ADC (ADS7830) for brightness and speed control
- LCD display compatible with the `rpi_lcd` library

## Dependencies

Ensure a seamless experience by having the following dependencies in place:

- `gpiozero`: Simplifying GPIO interactions for Raspberry Pi
- `threading`: Bringing multi-threading capabilities to your Python script
- `time`: Managing time-related operations in Python
- `smbus`: Enabling I2C communication with the ADS7830
- `signal`: Handling signals gracefully in your Python script
- `rpi_lcd`: The essential library for controlling LCD displays on Raspberry Pi

## Installation

Follow these steps to set up the LED Patterns Display System:

1. Confirm the installation of required dependencies.
2. Connect LEDs, a button, potentiometers, and an LCD display to your Raspberry Pi.
3. Run the script using Python 3: `python3 your_script_name.py`

## Usage

Embark on an exploration of LED patterns with ease:

- Press the button to cycle through captivating LED patterns.
- Fine-tune the brightness and speed using the responsive potentiometers.

## Termination

Safely conclude your LED adventure:

- Terminate the program by sending a SIGTERM or SIGHUP signal (e.g., Ctrl+C).
- Ensure all connected components are powered down securely.

## Author

Crafted with passion by Arth Raval and Krish Salvi on 12th December 2022.

## Credits

Inspired by the work of M Heidenreinch.

## License

This project operates under the MIT License - see the [LICENSE](LICENSE) file for details. Dive into the LED Patterns Display System, and let your creativity shine!
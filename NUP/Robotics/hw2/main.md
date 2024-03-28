# Arduino LED Control Project Report

## 1. Steady On

This effect is achieved by setting all the LEDs to a high state, ensuring they remain lit as long as this mode is active. The simplicity of this mode serves as a basic test of the LED setup and wiring.

## 2. Running Light

The Running Light effect is implemented by sequentially turning on each LED in the row, pausing briefly to create the appearance of movement, then turning it off before moving to the next LED. This cycle repeats, creating a continuous "running" effect. The speed of the running light can be adjusted by changing the delay between the activation of each LED.

## 3. Cycling Rainbow

For this effect, RGB LEDs are required. Each LED cycles through colors representing the rainbow by adjusting the intensity of the red, green, and blue components sequentially. This creates a gradient effect that cycles through the visual spectrum. Timing adjustments allow for control over the speed of the color transitions.

## 4. Binary Counter

The Binary Counter mode utilizes a series of LEDs to represent binary numbers, with each LED corresponding to a binary digit (bit). The state of the DIP switch determines whether the counter increments or decrements, as well as defining the range of the count. The LEDs are updated to reflect the current count in binary form, providing a visual representation of binary counting.

## 5. Pulse Wave

The Pulse Wave effect is realized using PWM (Pulse Width Modulation) to vary the brightness of the LEDs. The intensity of each LED is gradually increased from off to fully on and then decreased back to off, creating a "pulsing" effect. The rate of pulsing can be adjusted by modifying the delay within the pulse cycle, allowing for faster or slower waves. This effect is particularly effective in creating atmospheric or mood lighting.

To explore these scenarios interactively, visit the Tinkercad simulation [here](https://www.tinkercad.com/things/av9lpSEZqo8-brave-bombul-fulffy/editel?returnTo=%2Fthings%2Fav9lpSEZqo8-brave-bombul-fulffy) and [here](https://www.tinkercad.com/things/eRMvgfKtkNo-brave-bigery-albar/editel?returnTo=%2Fthings%2FeRMvgfKtkNo-brave-bigery-albar). Each setting on the DIP switch corresponds to a different lighting effect, offering a range of speeds from leisurely to rapid, enhancing the visual experience.

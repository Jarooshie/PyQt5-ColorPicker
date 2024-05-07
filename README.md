# PyQt5 Color Picker

A fully custom-made color picker class that you can seamlessly integrate into your own projects. The color picker is built entirely using PyQt5.

<p align="center">
  <img src="https://i.imgur.com/QTXWurs.png">
</p>

<p align="center">
  <i>Please note that the app above is the 'example2.pyw' code, The class itself ONLY contains the Color Picker shown at the top left, Consider checking out 'exmaple.pyw' for better understanding.</i>
</p>

## Requirements
The only requirement for this code is `PyQt5`. To install it, simply run the following command:
```bash
pip install PyQt5
```
## Integration into Your Project
To successfully integrate the color picker into your project, make sure to include both the `assets` folder and the `ColorUtils.py` file. Without these components, the color picker won’t function as expected.
## Usage
```python
from ColorPicker import ColorPicker

color_picker = ColorPicker(parent)
```


For a practical demonstration of how to use the color picker, refer to the `example.pyw`/`example2.pyw` file. Execute it to explore the color picker’s features firsthand.


## Functions

```python
picker.getColorRGB() -> tuple[int]

picker.getColorHSL() -> tuple[float]

picker.getColorHSV() -> tuple[float]

picker.getColorHEX() -> str; ex: "#fa0c2c"
```

#

```python
picker.setColorHEX(hex : str) -> None
# Updates the color based on the color hex code given to the function. ('#rrggbb' format)
```

## Signals
```python
picker.color_changed.connect(FUNCTION_TO_CALL)
# Runs FUNCTION_TO_CALL when the color changes.
```


## Example code
```python
# Initialization
picker = ColorPicker(self)
picker.move(20,20)
picker.setFixedSize(200,200) # It's highly recommeded to give the same width and height for the picker.

# Signal
picker.color_changed.connect(lambda: print(picker.getColorRGB()))
```

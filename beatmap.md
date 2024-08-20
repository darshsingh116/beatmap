
# Beatmap Data Conversion for Neural Network

This document outlines the process of converting osu! beatmap data into a format that can be fed into a neural network. The conversion process is broken down into two main phases: **Hit Object Parsing** and **Data Structuring**.

## Phase 1: Hit Object Parsing

In this phase, we parse the raw hit object data from the beatmap file. osu! beatmaps consist of various hit objects, including circles, sliders, and spinners. Each type of hit object requires special handling to extract relevant features.

### Hit Object Types (4th data in hitobject syntax)

1. **Hit Circle (Type 1 or 5)**: A simple circle that must be hit.
2. **Slider (Type 2 or 6)**: A slider that requires the player to hold and follow a path.
3. **Spinner (Type 8 or 12)**: A spinner that requires the player to spin their cursor.

### Example of Hit Objects Parsing

#### 1. Hit Circle (Type 1 or 5)

```python
# Input Data:
hitobject = "256,192,2500,1,0,0:0:0:0:"

# Parsing Result:
parsed_object = process_hitobject(hitobject)

Output: [['256', '192', '2500', '1', '0',  '-1', '-1', '-1', '-1','0:0:0:0:', '-1']]
```

#### 2. Slider (Type 2 or 6) (For detailed slider syntax check slider-info.md) 
- Splitting based on Slider points
- Note time is same for all parts as in the end we will combine

```python
# Input Data:
slider_data = "431,86,96039,2,0,B|406:144|433:238,1,157.500006008148,0|0,1:0|0:0,0:0:0:0:"

# Parsing Result:
parsed_slider_segments = process_hitobject(slider_data)
# Output: [
#   ['431', '86', '96039', '2', '0', 'B|419:115', '157', '0|0', '1:0', '0:0:0:0:', '0'],
#   ['433', '238', '96039', '2', '0', 'B|431:192', '157', '0|0', '0:0', '0:0:0:0:', '2']
# ]
```

#### 3. Spinner (Type 8 or 12)

```python
# Input Data:
spinner_data = "256,192,3500,8,0,5000,0:0:0:0:"

# Parsing Result:
parsed_object = process_hitobject(spinner_data)
# Output: [['256', '192', '3500', '8', '0', '5000', '-1', '-1', '-1', '0:0:0:0:', '-1']]
```

### Explanation

Each type of hit object is processed differently:

- **Hit Circles** are straightforward and involve minimal processing.
- **Sliders** are more complex, as they require interpolation based on their type (Linear, Bezier, Perfect Circle) to break them down into segments.
- **Spinners** are processed similarly to hit circles but may have different features to consider.

## Phase 2: Data Structuring

Once hit objects have been parsed, the next step is to structure the data into a format that can be used by a neural network. This involves converting the parsed data into a consistent numeric format, padding or truncating where necessary.

### Example of Structuring Parsed Data

Let's consider the parsed data from a hit circle and a slider and structure it.

#### 1. Hit Circle Structuring

```python
# Parsed Data from Phase 1:
parsed_hit_circle = ['256', '192', '2500', '1', '0', '0:0:0:0:', '-1', '-1', '-1', '-1', '-1']

# Structured Data:
# The data is normalized and padded to fit the neural network's input format.
structured_hit_circle = [256, 192, 2500, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1]
```

#### 2. Slider Structuring
- Assign B,L,P,O etc numbers 1,2,3,4,etc

```python
# Parsed Data from Phase 1:
parsed_slider_segment = ['431', '86', '96039', '2', '0', 'B|419:115', '157', '0|0', '1:0|0:0', '0:0:0:0:', '0']

# Structured Data:
# Similar to the hit circle, but includes additional fields for slider data.
structured_slider_segment = [431, 86, 96039, 2, 0, 1, 419, 115, 157, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
```
#### 3. Spinner Structuring

```python
# Parsed Data from Phase 1:
parsed_slider_segment = ['256', '192', '214067', '12', '0', '218781',  '-1', '-1', '-1', '0:0:0:0:', '-1']

# Structured Data:
# Similar to the hit circle, but includes additional fields for slider data.
structured_slider_segment = [256, 192, 214067, 12, 0, 218781, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -1]
```

### Explanation

- **Normalization**: Coordinates are normalized relative to the play area (512x384).
- **Padding**: If there are missing values, they are padded with `-1` to maintain a consistent input size.
- **Data Transformation**: Some fields are transformed or encoded to better fit the neural network's expected input format.

## Summary

The conversion process involves parsing raw beatmap data into structured, numeric representations suitable for machine learning models. This approach allows us to capture the intricacies of various hit objects, ensuring that the neural network receives all relevant features for effective learning. The structured data can then be used as input to train models for tasks such as difficulty estimation, beatmap ranking, or gameplay prediction.

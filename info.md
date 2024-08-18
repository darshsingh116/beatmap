# OSU! Slider Hit Object Format

In OSU!, sliders are a more complex type of hit object compared to circles. They require following a path and often include additional properties such as repeat count and pixel length. Here’s a detailed breakdown of the slider hit object format with examples for each part.

## Slider Hit Object Format

**Format:**


### Components:

- **x_start**: X-coordinate of the starting point of the slider.
- **y_start**: Y-coordinate of the starting point of the slider.
- **t**: Time in milliseconds when the slider starts.
- **2**: Hit object type for sliders.
- **hitSound**: Type of hit sound (0 = normal, 1 = soft, 2 = drum).
- **sliderData**: Detailed data about the slider path and properties.

## Slider Data Format

**Format:**


### Components:

- **path**: A series of points that define the path of the slider.
- **repeatCount**: Number of times the slider repeats.
- **pixelLength**: Length of the slider in pixels.
- **edgeSettings**: Settings for the slider edge, such as linear or curved.
- **edgeData**: Additional control points for the slider edge.
- **nodeData**: Control points for the slider path.

## Detailed Breakdown with Example

**Example Slider Hit Object:**


### 1. Coordinates and Time:

- `320,240`: The starting X and Y coordinates of the slider.
- `500`: The time in milliseconds when the slider starts.
- `2`: The hit object type for sliders.

### 2. Hit Sound:

- `0`: The type of hit sound (0 = normal). This specifies the sound that will be played when the slider is hit.

### 3. Slider Data:

#### a. Path:

- `322:354|322:354|416:325|416:325|475:345`:
  - `322:354`: The first control point.
  - `322:354`: The second control point (same as the first, meaning the slider might start at this point).
  - `416:325`: The third control point.
  - `416:325`: The fourth control point (repeated, creating a smooth curve).
  - `475:345`: The fifth control point (end of the path).

#### b. Repeat Count:

- `1`: The slider will repeat once. If set to `0`, the slider does not repeat.

#### c. Pixel Length:

- `188.999994232178`: The length of the slider in pixels. This defines how long the slider is.

#### d. Edge Settings and Data:

- `2|0`: Specifies the edge settings.
  - `2`: The type of slider edge (e.g., curved or linear).
  - `0`: Additional edge settings, often indicating a specific type of curve.

#### e. Node Data:

- `0:0|0:0`: Control points and settings for the nodes in the slider.
  - `0:0`: Represents default or no additional control points.
  - Additional nodes can be specified if the slider path is complex.

#### f. Additional Data:

- `0:0:0:0:`: This can include additional hit sound settings or other properties. In many cases, this is set to `0` for simple sliders.

## Summary

For a slider hit object, the key elements include:

- **Start Coordinates**: Where the slider starts.
- **Time**: When the slider appears.
- **Path**: The series of control points defining the slider's path.
- **Repeat Count**: How many times the slider repeats.
- **Pixel Length**: The length of the slider.
- **Edge Settings**: Type of edge for the slider path (linear, curved, etc.).
- **Additional Data**: Optional properties such as additional hit sounds or control points.

By understanding these components and their formats, you can effectively parse and work with slider hit objects in OSU! maps.

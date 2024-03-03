# graphicsengine

An extremely basic homemade pygame graphics engine built from scratch to learn about graphics and apply fundamentals of linear algebra.

## Controls
- **W, A, S, D** Move the camera's physical location through space
- **Arrow Keys** Change the camera's angle (look around)

## Adding Objects
Use the `create_object` function:

```python
create_object(points, connections, surfaces, color, drawPoints)
  """
  :param points: List of tuples (x, y, z) representing points in the array
  :param connections: List of tuples (i, j) representing lines between the ith and jth element in `points`
  :param surfaces: List of tuples (p1, p2, p3...) representing surfaces with vertices as the p1th, p2th... element of points
  :param color: Tuple (r, g, b) representing the color of the object
  :param drawPoints: Whether to draw the points as circles
  """
```

## Citations
Built alongside @ElliottF05 in summer 2023


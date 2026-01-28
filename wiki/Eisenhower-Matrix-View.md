# `[eisenhower_view]` Configuration

## `field_size`

> Default: `20` (Example)

Controls the width of the quadrants (columns) in character units. If your terminal is wide, you can bump this up to see more of your task descriptions without wrapping.

## `fields` Configuration

This is where the magic happens. You need to map your todo.txt priorities to the four specific quadrants of the matrix.

The available keys for `[eisenhower_view.fields]` are hardcoded to the logic of the matrix:

- `important_urgent` (Do First)
- `important_not_urgent` (Schedule)
- `not_important_urgent` (Delegate)
- `not_important_not_urgent` (Don't Do / Delete)

### `priorities`

Inside each field, you must assign a list of priorities.

```toml
priorities = ["A"]
```

You can also map multiple priorities to a single quadrant:

```toml
priorities = ["A", "B"]
```

### `style`

Each field supports a `style` object to customize the header color and font weight. This helps you visually distinguish the urgent tasks from the not so urgent ones.

**Accepts:**

- `color`: Hex code or color name (e.g., `"green"`, `"red"`).
- `bold`: Boolean (`true`/`false`).
- `italic`: Boolean (`true`/`false`).

## Configuration Example

Here is a full setup that maps standard `(A)` through `(D)` priorities to the classic Eisenhower quadrants:

```toml
[eisenhower_view]
field_size = 20

# Quadrant 1: Do First
[eisenhower_view.fields.important_urgent]
priorities = ["A"]
[eisenhower_view.fields.important_urgent.style]
color = "green"
bold = false
italic = false

# Quadrant 2: Schedule
[eisenhower_view.fields.important_not_urgent]
priorities = ["B"]
[eisenhower_view.fields.important_not_urgent.style]
color = "blue"
bold = false
italic = false

# Quadrant 3: Delegate
[eisenhower_view.fields.not_important_urgent]
priorities = ["C"]
[eisenhower_view.fields.not_important_urgent.style]
color = "red"
bold = false
italic = false

# Quadrant 4: Delete/Later
[eisenhower_view.fields.not_important_not_urgent]
priorities = ["D"]
[eisenhower_view.fields.not_important_not_urgent.style]
color = "magenta"
bold = false
italic = false
```

And the output looks like this:

![](./assets/03_eisenhower.png)

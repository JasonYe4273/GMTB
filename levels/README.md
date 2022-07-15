# JSON-based level editor
---

A level is represented as JSON object with three fields: a `name`, a `bounds` array and `objects`.

## Name
---
Self-explanatory. Should be a string.

## Bounds
---
The `bounds` field is an array containing two arrays of three integers, indicating the upper left and lower left corner of the the shear array. Coordinates are specified as in this link:
https://nornagon.medium.com/til-triangle-grids-133ed47cc807

## Objects
---
The `objects` field is an array containing game elements which make up the level. Each element is a JSON object with a `type`, `loc`(ation), and other fields as specified in the below table. The 	`loc` field uses the coordinate system as specified in the above medium link.

| Type 	| Fields (other than `loc`) |
|---|---|
| `start` |  |
| `d4` | `faces`: array[4], list of what is on each of the 4 faces. The topmost face is first, and the rest are top to bottom, left to right. (required) |
| `d8` | `faces`: todo |
| `d20` | `faces`: todo |
| `static` | `label`: string, what is printed on the top of this static square |
| `wall` |   |
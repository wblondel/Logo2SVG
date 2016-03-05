# List of commands

## Basic Commands
### fd x / forward x
x : int or float
Moves the turtle x pixels

### bk x / backward x
x : int or float
Moves the turtle back x pixels

### left x / lt x
x : int or float
Rotate the turtle left x degrees

### right x / rt x
x : int or float
Rotate the turtle right x degrees

## Controlling the pen
### penup / pu
Turtle stops leaving a trail

### pendown / pd
Turtle will leave a trail

## Colors
### setcolor x / setcolor color
x : int

color : string

Will set the line color according to the following table:

<table id='colortable'>
    <tr>
        <td style='background-color: black; color: white;'>0: black </td>
        <td style='background-color: blue;'>1: blue </td>
        <td style='background-color: lime;'>2: green </td>
    <tr>    
        <td style='background-color: cyan;'>3: cyan </td> 
        <td style='background-color: red;'>4: red </td>
        <td style='background-color: magenta;'>5: magenta </td>
    <tr>
        <td style='background-color: yellow;'>6: yellow </td>
        <td style='background-color: white;'>7: white </td>
        <td style='background-color: brown;'>8: brown </td>
    <tr>
        <td style='background-color: tan;'>9: tan </td>
        <td style='background-color: green;'>10: green </td>
        <td style='background-color: aquamarine;'>11: aqua </td>
    <tr>
        <td style='background-color: salmon;'>12: salmon </td>
        <td style='background-color: purple;'>13: purple </td>
        <td style='background-color: orange;'>14: orange </td>
    <tr> 
        <td style='background-color: gray;'>15: gray </td>
</table>

### setcolor r, g, b
r : int
g : int
b : int

Will set the line color according to the amount of red, green and blue.
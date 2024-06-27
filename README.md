# G84-Split

When generating code in CAMWorks, when you use G84 Tapping, the line with this operation looks like this:
G84 G98 R1. Z-10. F100.
Sometimes we need to split the tapping operation by several Z increments.
Unfortunately, CAMWorks cannot perform this option, even the machine postprocessor cannot be edited.
This script can divide all the G84 lines in the NC program by an increment to the original Z.

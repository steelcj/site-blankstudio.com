# Local Resources Strategies

## Description

Many websites that we work with use external resources for things like fonts, forms and other services. This increases bandwidth usage as well as vulnerability to internet outages.

## Font strategy

For fonts we are looking for a logical local storage locations that allow for separation of concerns. For example the add on "infusion" stores its fonts in one location and we want website fonts to be stored in a location indicating that they are for the website as a whole.

Ideally we would have a single configuration file .yaml that hold the source of the font as well as the sizes and other permutations that the site requires. Then this file can be used to feed a small (python) script that downloads and places the fonts in a logical location. 


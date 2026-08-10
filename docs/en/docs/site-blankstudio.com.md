# site-blankstudio.com

## Description

site-blankstudio.com is a template site used to get a client site up and running with all of the Universal Cake foundations in place. Through a process of client consultation we then customize a working site with dummy content and sculpt it to meet the client's needs and expectations.

Right now we are preparing the project for quick and efficient customization, so we can create and "brand" the site on the client's behalf.

## Customization process

The steps below run roughly in order. Earlier steps (languages, branding) shape later ones (content, forms), so complete them first where possible.

### 1. Languages

* Confirm the languages the client requires.
* Configure the site to support those languages before adding content, so all content and forms are authored multilingually from the start.

### 2. Branding

#### Fonts

* Select fonts with the client.
* Record each font, its weights, and any other required permutations in the font config (`fonts.yaml`).
* Download and place the fonts by running `scripts/fetch-fonts.py`, which reads `fonts.yaml`.

#### Colors

* Develop a color scheme with the client.
* Apply it to the theme.

#### Logos & images

* Rough in the logo and adjust the theme as required:
  * Main logo
  * Other representations (e.g. compact, monochrome, social)
* Add the favicon.

### 3. Accessibility

* Enhance accessibility options when desired or required on behalf of the client.

### 4. Forms and form support

* Replace template forms with the client's required forms.
* Stand up a custom multilingual form server, similar to the one created for https://poirierpeintureplus.com/en/home/.

> **Note:** The multilingual form server still needs significant work. See [poirierpeintureplus.com](https://poirierpeintureplus.com/en/home/) for the reference implementation.

### 5. Review & launch

* Review the site with the client against their expectations.
* Confirm languages, branding, accessibility, and forms all work end to end before launch.


# Material Community Icons for Soar

An opt-in Material Community icon font and glyph map matching `@expo/vector-icons` 15.1.1. Apps that do not install the plugin do not need its font, map or platform modules. The font is SHA-256 identical to `@mdi/font` 7.4.47. The Pictogrammers Free License, referenced Apache 2.0 license, and Expo MIT license are in `assets/`; see `assets/README.md` for provenance and notices.

The plugin's source code is licensed under the MIT License in `LICENSE`. The bundled font, glyph map, and generated data retain their upstream licenses and notices in `assets/`; the source-code license does not replace those terms.

## Status and prerequisites

This plugin depends on **unreleased Soar core changes**: the v90 reserved pure `native:format.lookupStringTable` function and compiler support for `bundleAssets` at `soar-plugin-assets/<plugin-name>/<path>` and `soarSources` imports using `@plugin/`. A host and compiler without these changes cannot build or run the included component. The old `native:format.materialCommunityGlyph` v85 builtin is a separate legacy API and its compatibility migration is not implemented. Do not remove it or publish an OTA that assumes it has moved to this plugin.

The component supports `name`, `size`, and `color`; full Expo style forwarding, accessibility and font scaling are not yet implemented. It has not been verified on Android or iOS devices. Use it only where the Material Community family is the intended source, and retain any app-specific SVG assets where those are required.

## Installation

From a Soar app whose engine includes the prerequisites above, install the plugin from a local checkout using `soar plugin add PATH`, or from its repository using `soar plugin add github:OWNER/REPO@TAG`. The plugin manager must register it in that engine's `soar-plugins.json`. Import the declared component with `import { MaterialCommunityIcon } from "@plugin/material-community-icons/soar/MaterialCommunityIcon";`. At compile time, the compiler embeds the font declared by `bundleAssets`; missing/uninstalled plugins, undeclared files, conflicting assets and paths that escape the plugin fail the build.

For ordinary handlers and effects, `native:materialCommunityIcons.glyph(name)` is also provided on Android, iOS and desktop. Empty names return an empty string and unknown names return `?`. This host function is **not** trusted as pure by the verifier; the component instead uses the core's bounded generic pure lookup with plugin-owned table data.

## Development

Run `python3 tools/regenerate.py` to check the generated Kotlin, Swift and Soar tables against `assets/glyphmap.txt`; use `--write` to regenerate. The map contains 7,448 entries. Tests must cover plugin installation and removal, full-map parity, render updates, host purity and version guard, asset path containment and collision, signed OTA upgrade/rollback, and both mobile platforms before release.

---
name: "China AI Provider Finder"
description: "Dense telemetry cockpit for discovering and evaluating Chinese AI gateways"
colors:
  primary: "#7bbaff"
  primary-bg: "#003a6e"
  void: "#030406"
  surface: "#0a0c10"
  surface-elevated: "#14171d"
  surface-pop: "#1f232d"
  text-primary: "#e1e7ef"
  text-muted: "#8892a0"
  text-faint: "#4b5563"
  border-base: "#20252e"
  border-hi: "#394354"
  status-warn: "#ffb59d"
  status-warn-bg: "#7a2600"
  status-ok: "#4edea3"
  status-ok-bg: "#003d28"
  status-critical: "#ffb4ab"
typography:
  display:
    fontFamily: '"JetBrains Mono", monospace'
    fontSize: "26px"
    fontWeight: 700
    lineHeight: "32px"
  body:
    fontFamily: '"Space Grotesk", system-ui, sans-serif'
    fontSize: "14px"
    fontWeight: 400
    lineHeight: "20px"
  label:
    fontFamily: '"JetBrains Mono", monospace'
    fontSize: "12px"
    fontWeight: 600
    lineHeight: "20px"
    letterSpacing: ".04em"
  label-sm:
    fontFamily: '"JetBrains Mono", monospace'
    fontSize: "11px"
    fontWeight: 500
    lineHeight: "16px"
    letterSpacing: ".12em"
  label-xs:
    fontFamily: '"JetBrains Mono", monospace'
    fontSize: "10px"
    fontWeight: 600
    lineHeight: "14px"
    letterSpacing: ".1em"
rounded:
  sm: "5px"
  lg: "8px"
components:
  button-primary:
    backgroundColor: "{colors.primary-bg}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  button-secondary:
    backgroundColor: "{colors.surface-elevated}"
    textColor: "{colors.text-primary}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "8px 16px"
  badge:
    typography: "{typography.label-xs}"
    rounded: "{rounded.sm}"
    padding: "2px 6px"
---

# Design System: China AI Provider Finder

## Overview

**Creative North Star: "The Deep Radar Terminal"**

The visual identity presents a dense telemetry cockpit set on a deep-space blue-black canvas. It prioritizes data legibility and operational speed over decorative chrome. Contrast is laser-focused: the vast majority of the interface recedes into layered dark tones (`void`, `surface`, `surface-2`), allowing evidence badges, high-contrast indicator pings (blue, green, amber), and tabular intel to stand out unequivocally. 

This design refuses the padded "dashboard-card by numbers" aesthetic. It is built as a single dense instrument where evidence and status rule. There are no gradients, no rounded fluff, and no unnecessary padding—just crisp monospace typography, glowing focus vectors, and pure functional intent.

**Key Characteristics:**
- **Evidence-First Density:** Aggressive tabular layouts displaying maximum intel.
- **Instrumental Typography:** `JetBrains Mono` carries all critical metadata, numbers, and interactive verbs; `Space Grotesk` supports readable prose.
- **Phosphor Feedback:** Hover and focus states use intense cyan-blue glows instead of solid opaque fills.

## Colors

The palette grounds the interface in a deep abyss, reserving vivid colors strictly for status, telemetry, and critical interactions.

### Primary
- **Signal Blue** (`#7bbaff`): Actionable controls, focus rings, active busy states, and primary button text. 
- **Signal Blue Background** (`#003a6e`): Deep blue substrate for primary buttons.

### Neutral
- **Deep Void** (`#030406`): The outermost page background canvas.
- **Surface Level 1** (`#0a0c10`): Primary container background (e.g., stats, tables).
- **Surface Level 2** (`#14171d`): Secondary interactive surface (e.g., secondary buttons, table headers, hover rows).
- **Surface Level 3** (`#1f232d`): Elevated hover surface for controls (e.g., secondary button hover, tags).
- **Border Base** (`#20252e`): Subtle structural dividers between table rows or muted containers.
- **Border High** (`#394354`): Interactive or hovered borders ensuring clear boundaries.
- **Text Primary** (`#e1e7ef`): High-contrast readable foreground for standard reading material.
- **Text Muted** (`#8892a0`): Secondary descriptive text and inactive metadata.
- **Text Faint** (`#4b5563`): Placeholder text and empty state iconography.

### Status (Tertiary)
- **Pulse Green** (`#4edea3`): Signifies healthy, alive, or verified status.
- **Pulse Amber** (`#ffb59d`): Indicates warnings or degraded signals.
- **Critical Red** (`#ffb4ab`): Used solely for explicit errors and extreme risk flags.

**The Signal-to-Noise Rule.** Do not paint large surfaces in primary or status colors. Vivid hues exist exclusively as borders, text highlights, pulsing dot indicators, or low-opacity (12%) badge backgrounds to preserve raw visual hierarchy.

## Typography

**Display Font:** JetBrains Mono
**Body Font:** Space Grotesk (fallback: system-ui, sans-serif)
**Mono Font:** JetBrains Mono (fallback: monospace)

**Character:** Highly technical and precise. Space Grotesk brings geometric, legible warmth to standard text, while JetBrains Mono asserts extreme instrumental accuracy for tabular data and controls.

### Hierarchy
- **Display** (bold, 26px, 32px line-height): Large metric numbers on the stats strip. Always uses tabular figures.
- **Body** (regular, 14px, 20px line-height): Descriptive text, configuration blocks, and primary narrative fields.
- **Label** (semibold, 12px, 20px line-height): Core action verbs (Buttons, Tabs) and input text.
- **Label Small** (medium, 11px, 16px line-height, expansive tracking): Eyebrows, column headers, and dense metadata blocks.
- **Label Extra Small** (semibold, 10px, 14px line-height, tight tracking): Pill badges and tertiary metric labels.

## Layout

**The Ledger Imperative Rule.** Avoid arbitrary max-widths on tabular views. The interface should consume horizontal space fluidly up to 1800px to display unclipped URLs, timestamps, and model claims. 

- **Containers:** Bound at 1800px max-width, center-aligned, flanked by 24px gutters.
- **Rhythm:** Tightly packed vertical grids with small sub-gaps (8px, 10px, 16px). Tabular cells prioritize horizontal reading rhythm over vertical airiness.
- **Alignment:** Numbers (latency, scores) aggressively right-aligned. Badges flex-wrapped with 6px gaps.

## Elevation & Depth

Layered Deep Space: the application is visibly stacked through shifting background saturations rather than floating drop shadows.

- **Background:** The absolute bottom layer is the Void.
- **Substrates:** `surface` containers rest on the void; `surface-2` inputs/headers rest on `surface`.
- **Glow & Pulse:** True depth comes from luminescence. Active focal elements (focused inputs, primary buttons) use deep blue box-shadows (0 0 12px rgba(123, 186, 255, 0.15)) to achieve a "phosphor bloom" effect on the dark space, rather than casting a black shadow.

## Shapes

- **Radius:** Subtle and unyielding. Standard controls (buttons, inputs) use a small 5px radius (var(--r)). Large structural shells (the table wrapper) use 8px (var(--r-lg)). Absolutely no pill-shaped buttons; geometry represents precision.
- **Borders:** Hard 1px solid lines define every container. The absence of a background requires a border.

## Components

Controls are heavily tactile and instrumental. Focus states demand glowing attention.

- **Primary Buttons:** Deep blue background (#003a6e) with cyan text (#7bbaff) and borders. On hover, background fully shifts to cyan while text punches-out to Void (#030406), coupled with a strong phosphor bloom shadow.
- **Secondary Buttons:** Medium dark surface (#14171d) stepping out of the page slightly, lifting to #1f232d on hover.
- **Inputs & Textareas:** Recessed surfaces (#0a0c10) adopting a vivid blue border and bloom shadow when focused. 
- **Pill Badges:** Small, highly dense metric labels. Backgrounds use 12% opacity of their respective status hue with 25% opacity borders. Text remains solid status hue to ensure legibility.
- **Status Dots:** 7x7 round pings using solid status colors plus an 88 hex alpha localized glow. Busy state aggressively animates transparency scaling (breathing heartbeat).

## Do's and Don'ts

- **Do** wrap raw API claims, metrics, and timestamps in `JetBrains Mono`.
- **Do** align numeric and boolean data to the right wherever appropriate to aid scanability.
- **Do** use strict low-opacity background washes for colored badges, protecting text contrast.
- **Don't** use pure white (#ffffff) for structural text; stick to the slightly-blue #e1e7ef standard text tone unless it's a specific button hover or high-octane focus state requiring max-contrast.
- **Don't** stack opaque boxes randomly. Uphold the Void/Surface/Surface-2 tonal hierarchy.
- **Don't** try to make the UI look "friendly." It is a technical operations terminal built to process dirty gateway intelligence fast.

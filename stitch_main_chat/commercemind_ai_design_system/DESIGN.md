---
name: CommerceMind AI Design System
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#464555'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#684000'
  on-tertiary: '#ffffff'
  tertiary-container: '#885500'
  on-tertiary-container: '#ffd4a4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-metrics:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style
The design system is engineered for a professional, high-tech SaaS environment that prioritizes reliability and results. The aesthetic is a fusion of **Corporate Modern** and **High-Contrast Bold**, utilizing sharp typographic hierarchies and strategic pops of functional color to drive user focus toward key commerce metrics.

The emotional response is one of "intelligent authority"—the interface feels stable and enterprise-ready, yet possesses the kinetic energy of real-time AI processing. We use heavy whitespace to separate dense data sets and high-contrast text to ensure immediate scannability.

## Colors
The palette is rooted in a clean, high-contrast foundation. 

- **Primary (Indigo):** Used for primary actions, active states, and brand recognition.
- **Secondary (Emerald):** Reserved for growth metrics, success states, and positive AI insights.
- **Surface & Background:** A crisp white surface (#FFFFFF) sits atop a slightly tinted gray background (#F9FAFB) to provide subtle depth without traditional heavy shadows.
- **Accents:** Red and Amber are used strictly for urgency and warnings. Soft Indigo (#EEF2FF) serves as a functional utility color for icon containers and light-mode hover states.

## Typography
The system uses **Inter** exclusively to maintain a systematic and utilitarian feel. 

- **Metrics & KPIs:** Use `display-metrics` with tight letter spacing to emphasize numerical growth.
- **Headlines:** Must be bold and high-contrast against the background using the Neutral Dark (#0F172A) color.
- **Body Text:** Uses Neutral Gray (#4B5563) for improved long-form readability.
- **Labels:** Small labels use a semi-bold weight and uppercase styling for categorizing metadata and table headers.

## Layout & Spacing
This design system utilizes a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **Desktop:** 24px gutters with 48px side margins.
- **Mobile:** 16px gutters with 16px side margins.
- **Rhythm:** All margins and paddings must be multiples of 4px. Use `lg` (24px) for standard container padding to ensure a breathable, premium feel. 
- **Reflow:** Components like metric cards should stack vertically on mobile but may span 3 or 4 columns on desktop layouts.

## Elevation & Depth
Depth is achieved through **Tonal Layering** and ultra-soft ambient shadows. 

- **Level 0 (Background):** #F9FAFB.
- **Level 1 (Cards/Surfaces):** #FFFFFF with a 1px border of #E2E8F0. 
- **Shadows:** Use a single, highly diffused shadow for elevated cards: `0px 4px 20px rgba(15, 23, 42, 0.05)`. 
- **Urgency Accents:** Specific cards (Alerts, Critical Insights) feature a 4px top-border in Indigo, Red, Amber, or Emerald to indicate status without relying solely on shadows.

## Shapes
The shape language is modern and approachable. 

- **Standard Elements:** Buttons and Input fields use a 0.5rem (8px) radius.
- **Containers:** Dashboard cards and modals use a `rounded-xl` (1.5rem / 24px) or `rounded-lg` (1rem / 16px) radius to create a soft, high-end frame for data.
- **Icon Enclosures:** Always perfectly circular (pill-shaped) to contrast against the structured grid of the layout.

## Components

### Buttons
- **Primary:** Solid Indigo (#4F46E5) with White text. Hover state transitions to a slightly darker shade with a soft shadow increase.
- **Secondary:** Outlined with a 1px Indigo border and Indigo text. Transparent background.
- **Tertiary:** Text-only in Indigo for low-priority navigation.

### Inputs
- **Style:** Minimalist with a 1px light gray border (#D1D5DB).
- **Focus State:** 2px Indigo border with a subtle 4px Indigo outer glow (low opacity).
- **Labels:** Always positioned above the field in `label-sm` style.

### Cards
- **Construction:** White background, 16px or 24px padding, 16px corner radius.
- **Accents:** Optional 4px solid top-border for status-driven data (e.g., Red for "Low Stock").

### Icons
- **System:** Dual-tone or sleek outline icons.
- **Enclosure:** Icons must be centered within a circular background of Soft Indigo (#EEF2FF).

### Metrics & Chips
- **Metric Cards:** Large `display-metrics` value with a secondary `body-md` label below.
- **Chips:** Used for status (e.g., "Active", "Pending"). Backgrounds should be 10% opacity versions of the status color (Emerald/Amber/Red) with full-opacity bold text of the same color.
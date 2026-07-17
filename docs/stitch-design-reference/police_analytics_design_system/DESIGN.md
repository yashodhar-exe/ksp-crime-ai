---
name: Police Analytics Design System
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#454650'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757681'
  outline-variant: '#c6c5d2'
  surface-tint: '#4b5b9b'
  primary: '#000b38'
  on-primary: '#ffffff'
  primary-container: '#0b1f5e'
  on-primary-container: '#7989cd'
  inverse-primary: '#b7c4ff'
  secondary: '#1d4ed8'
  on-secondary: '#ffffff'
  secondary-container: '#4069f2'
  on-secondary-container: '#fffbff'
  tertiary: '#250700'
  on-tertiary: '#ffffff'
  tertiary-container: '#481400'
  on-tertiary-container: '#c97758'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#324381'
  secondary-fixed: '#dce1ff'
  secondary-fixed-dim: '#b7c4ff'
  on-secondary-fixed: '#001551'
  on-secondary-fixed-variant: '#0039b5'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#370d00'
  on-tertiary-fixed-variant: '#74341a'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '450'
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
  tight: 8px
  compact: 12px
  standard: 16px
  loose: 24px
  container-margin: 32px
  sidebar-width: 260px
---

## Brand & Style
The design system is engineered for high-stakes investigative work, prioritizing authority, clarity, and rapid data synthesis. It adopts a **Modern Corporate** style with leanings toward **Minimalism**, specifically optimized for high-density information environments. 

The aesthetic is inspired by leading analytical platforms, utilizing a "Chrome-less" interface philosophy where the data remains the focal point. The emotional response is one of stability and precision—essential for law enforcement personnel managing complex crime data. Every element is designed to minimize cognitive load while maximizing the visibility of critical insights and AI-driven correlations.

## Colors
The palette is anchored by **Primary Dark Blue (#0B1F5E)**, a color that evokes institutional trust and authority. 

- **Primary:** Used for the sidebar, primary actions, and branding elements.
- **Surface & Canvas:** A pure white surface is used for primary content cards to ensure maximum contrast for data tables, set against a very light gray canvas (#F8FAFC) to define workspace boundaries.
- **Status Semantic Colors:** Strictly defined for priority levels (High/Medium/Low) to ensure immediate visual triage of case files.
- **AI Accent:** A distinct Violet (#8B5CF6) is reserved exclusively for AI-generated insights, differentiating synthesized intelligence from raw database records.

## Typography
This design system utilizes **Inter** as its primary typeface. Selected for its exceptional legibility in data-heavy tables and functional neutrality, it allows for a high-density layout without sacrificing readability.

- **Scale:** The system uses a tight typographic scale. Body text is set at 14px for standard reading, while 13px (body-sm) is the workhorse for enterprise data tables.
- **Monospace:** For Case IDs, Lat/Long coordinates, and IP addresses, use **JetBrains Mono** to ensure character differentiation (e.g., distinguishing '0' from 'O').
- **Hierarchy:** Use `label-caps` for table headers and section metadata to create clear visual anchors in dense interfaces.

## Layout & Spacing
The layout follows a **Fixed-Fluid Hybrid** model. The primary navigation sidebar is fixed at 260px, while the content area expands to fill the viewport, utilizing a 12-column grid for dashboard widgets.

- **Density:** To accommodate the vast amount of crime data, the design system utilizes a "Compact" spacing rhythm. Standard cell padding in tables should be 8px vertically to maximize vertical information density.
- **Breakpoints:** 
  - **Desktop (1440px+):** Full 12-column visibility with persistent sidebar.
  - **Tablet (1024px):** Sidebar collapses to icons; 8-column content grid.
  - **Mobile (768px):** Content stacks vertically; margins reduce to 16px.

## Elevation & Depth
Depth is communicated through **Tonal Layering** and **Low-Contrast Outlines** rather than heavy shadows. This maintains the professional, "flat" aesthetic required for government software.

- **Level 0 (Canvas):** #F8FAFC - The base background.
- **Level 1 (Cards):** Pure White (#FFFFFF) with a 1px border in #E2E8F0. This is the primary container for all data.
- **Level 2 (Modals/Popovers):** Pure White with a subtle ambient shadow (0px 4px 12px rgba(0, 0, 0, 0.05)).
- **AI Panels:** Utilize a subtle 1px inner-glow or border-tint using the AI Accent color (#8B5CF6) to signify a different layer of information origin.

## Shapes
The design system employs a **Rounded** shape language to soften the density of the data-heavy interface.

- **Cards & Panels:** Use a 0.5rem (8px) radius to strike a balance between modern software aesthetics and professional rigidity.
- **Input Fields & Buttons:** Use a 6px radius for a precise, "tooled" look.
- **Status Badges:** Use a fully rounded "pill" shape (100px) to distinguish them from interactive buttons or static data containers.

## Components
Consistent component behavior ensures that investigators can navigate the platform intuitively.

### Data Tables
The core of the system. Tables must support:
- **Sticky Headers:** Always visible during scroll.
- **Zebra Striping:** Sublte (#F1F5F9) on even rows for horizontal tracking.
- **High-Density Rows:** 32px height for standard rows.

### Buttons
- **Primary:** Solid #0B1F5E with white text.
- **Secondary:** Transparent with #E2E8F0 border and #0B1F5E text.
- **Actionable Icons:** 16px size within a 32px hit area.

### AI Insight Panels
Specialized containers for synthesized data. These should feature:
- A subtle gradient border using the AI Accent color.
- A "Source Attribution" footer in `body-sm` font size to explain the logic behind the AI suggestion.

### Status Badges
- **High Priority:** Red background (10% opacity) with #DC2626 text.
- **Medium Priority:** Amber background (10% opacity) with #D97706 text.
- **Low Priority:** Green background (10% opacity) with #059669 text.

### High-Density Sidebar
The sidebar should use the Primary Dark Blue (#0B1F5E) background. Icons should be line-art style (20px) with 60% opacity, moving to 100% opacity on hover/active states.
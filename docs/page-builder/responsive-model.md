# Responsive model and interaction

One page schema serves all devices. Base presentation is merged with only the selected device's overrides. Desktop, tablet and mobile overrides are independent; changing tablet spacing does not change desktop spacing. Runtime breakpoints are mobile at 600px or below, tablet at 601–1100px, desktop above 1100px.

Order, width, visibility, spacing, alignment, density, surface, border and containment can differ by device. Width uses a 12-column grid; width 12 stacks a column. Source defaults make phone columns full width. Reordering siblings writes order overrides for the current device. Adding/removing elements and moving widgets between columns changes the shared structure on all devices. Use visibility and order for device-specific arrangements; do not create unrelated copies of a business widget.

Media has a shared desktop/default asset and focal point, with optional tablet/mobile asset and x/y overrides. Fit, ratio, alt/decorative, radius, overlay and video flags are shared. Reset a device crop to inherit the default asset/crop.

Editor preview selects the responsive context explicitly. Its canvas fits the available editing workspace; it is not a claim that a 1440px desktop fits inside an iPad screen. Below 850px the controls sit above the canvas. Phone runtime remains the primary execution view; detailed authoring is intended for tablet or desktop.

Drag only from a labelled 44px handle. Content and margins remain scrollable. Structure → Settings provides Move earlier/later and Move to column. Arrow keys/Home/End navigate panel tabs; all settings are keyboard controls. A focal-point image click has equivalent labelled x/y range inputs. Escape cancels an active drag. Live business controls are inert during editing and preview. Reduced-motion preferences suppress editor scrolling animation.

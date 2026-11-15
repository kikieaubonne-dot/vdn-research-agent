---
title: Light sources
description: Fixture de test au format des Roblox Docs (texte construit pour les tests, pas une copie de la page).
---

# Light sources

Light sources such as `Class.PointLight|PointLight` and `Class.SpotLight|SpotLight` emit light from a part.

## Shared properties

| Property | Description |
| --- | --- |
| `Class.Light.Brightness|Brightness` | Intensity of the light. |
| `Class.Light.Shadows|Shadows` | Whether the light casts shadows. |

## Spotlights

To create a spotlight:

1. In the **Explorer** window, hover over a `Class.BasePart` and click the ⊕ button.
2. Insert a `Class.SpotLight`.
3. Then adjust the `Class.SpotLight.Angle|Angle` and `Class.SpotLight.Range|Range`.

```lua
local light = Instance.new("SpotLight")
light.Angle = 45 -- `Class.SpotLight.Angle|Angle` reste intact dans le code
light.Parent = workspace.Lamp
```

4. Test the light in **Play** mode.

> **Info:** The `Class.Lighting.LightingStyle|LightingStyle` property sets your game's lighting style.

![A street lamp spotlight with a 30 degree angle.](../assets/SpotLight-Angle-30.jpg)

### Flashlight setup

- Parent the light to the `Class.Tool.Handle|Handle`.
  - Keep `Class.Light.Shadows|Shadows` enabled.
- Use a narrow angle.

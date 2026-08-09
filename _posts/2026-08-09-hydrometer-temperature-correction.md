---
title: "Temperature correction for hydrometer readings"
tags: ['fermentation', 'measurement', 'physics']
---

I brew wine and fermented drinks at home with a friend every summer. To track fermentation, you measure the sugar content of the liquid via its specific gravity (SG). But the reading depends on temperature, and I wanted to understand how much that matters and whether I can correct for it. This post collects what I found — it's meant as a concise reference, so the tone is a bit dry. I hope that makes it useful to come back to.

While I made the first draft, and did the last proofing, I let Claude Code do some of the work in writing the post. I hope it didn't hallucinate and fool me in the process.

## What is specific gravity?

Specific gravity (SG), or more precisely *relative density*, is the ratio of the density of a sample to the density of pure water. Both densities depend on temperature, so a proper SG specification includes two temperatures: sample/reference. For example, SG 1.050 (20°C/15°C) means the sample at 20°C is 1.050 times as dense as water at 15°C. 

In some data tables of density, they list density in air, or density in a vacuum (the 'true' density). When weighing in air, both the sample and the reference weights experience buoyancy from the surrounding air. Water has a density around 0.997–1.000 g/mL in the 0–25°C range, while air is about 1.2 kg/m³. The relative error from ignoring air buoyancy in this range is at most about 130 ppm — well below typical instrument precision (an error of 0.001 SG when the value to measure is 1.0000 means an error of 1000 ppm ). We can treat apparent density (measured in air) as equal to true density (in vacuum).

In homebrewing the most common and simple instrument to measure SG is a hydrometer. A hydrometer is a sealed glass tube with ballast at the bottom and a graduated scale on the stem. It floats at a depth determined by Archimedes' principle: the weight of displaced liquid equals the weight of the hydrometer. A denser liquid displaces less volume, so the hydrometer floats higher; a less dense liquid lets it sink deeper. It has a scale calibrated to read SG directly. The scale is calibrated at a specific temperature. At that temperature, the markings are correct. But if the liquid temperature differs, the density changes and the reading shifts. Different liquids change their volume with temperature at different rates. The instrument itself also changes volume with temperature.

The hydrometer scale explains its calibration temperature, so you know at what sample temperature the reading is valid. A common temp is 20°C (68°F). Some hydrometers are calibrated at 60°F (15.56°C). They then report SG (60/60) or SG (20C/20C).

If the sample temperature is off, can we correct for that?


## Correction tables from manufacturers

Some hydrometers come with printed correction tables. For example, one of my American hydrometers has:

| Temp | Correction  (SG) |
|---|---|
| 10°C | −0.0025 | 
| 15°C | −0.0014 | 
| 20°C | 0 | 
| 25°C | +0.0028 
| 30°C | +0.0046 

The instruction booklet says this is a beer hydrometer, and I suppose it is computed empirically for this specific instrument and the thermal density dependence of typical beer wort. The corrections are at most 0.005 SG. Since a homebrewing hydrometer can typically be read to about ±0.001 SG, a 5°C temperature offset gives a correction comparable to the instrument's resolution.

If doing readings in sucrose solutions, or wine, will that still hold? For a different hydrometer with different gemoetry and glass, will it still hold? Maybe not. Lets discuss that further below. 

## Pure water correction, from first principles

Assume that the glass expansion of the hydrometer is negligible compared to the liquid's thermal expansion. This is a good approximation: glass has a volumetric expansion coefficient of about 25 ppm/K, while water is about 207 ppm/K at 20°C — almost an order of magnitude smaller.

A hydrometer calibrated at $$T_{\text{cal}}$$, used at temperature $$T$$, reads:

$$\text{reading} \approx \frac{\rho_{\text{sample}}(T)}{\rho_{\text{water}}(T_{\text{cal}})}$$

What we want is the SG at 20°C/20°C:

$$\text{SG}_{20/20} = \frac{\rho_{\text{sample}}(20°C)}{\rho_{\text{water}}(20°C)}$$

If we assume that the sample's thermal expansion is similar to water's (reasonable for dilute sugar solutions), then $$\rho_{\text{sample}}(T) / \rho_{\text{sample}}(20°C) \approx \rho_{\text{water}}(T) / \rho_{\text{water}}(20°C)$$, and we can show that:

$$\text{SG}_{20/20} \approx \text{reading} \times \frac{\rho_{\text{water}}(T_{\text{cal}})}{\rho_{\text{water}}(T)}$$

The correction factor is just the ratio of water densities at the calibration temperature and the measurement temperature.

For the water density, I use the polynomial from Jones & Harris[^jones], which gives the density of air-free water on the ITS-90 temperature scale, valid from 5 to 40°C:

$$\rho(T) = 999.85308 + 6.33 \times 10^{-2}\,T - 8.52 \times 10^{-3}\,T^2 + 6.94 \times 10^{-5}\,T^3 - 3.82 \times 10^{-7}\,T^4 \quad [\text{kg/m}^3]$$

Some representative values are in the table below. The correction is the value to add if reading a hydrometer calibrated at 20°C, used at the given temperature, and the sample is at true SG 1.050 (a medium value in home brewing). This column can be compared with the values in the previous table.

| Temperature | $$\rho_{\text{water}}$$ (g/mL) | $$\Delta $$ (SG) | 
|---|---|---|
| 10°C | 0.99970 | −0.0016 |
| 15°C | 0.99910 | −0.0009 |
| 15.56°C (60°F) | 0.99901 | −0.0009 |
| 20°C | 0.99820 | 0 |
| 25°C | 0.99704 | +0.0012 |
| 30°C | 0.99564 | +0.0027 |

We find that the pure-water correction is on the order of 0.001–0.003 SG in the 10–30°C range, and that the manufacturer corrections are roughly 1.6–2.4× larger. This is consistent with the manufacturer table being calibrated for beer wort, which has a different thermal expansion than pure water.

## Empirical correction tables

Sugar solutions have different thermal expansion coefficients than pure water. The correction therefore depends on what is dissolved and in what concentration.

The OIV Compendium of International Methods of Analysis[^oiv] acknowledges this explicitly: it provides *separate* temperature correction tables for dry wine (Table II), natural or concentrated must (Table III), and sweet wine (Table IV). The worked examples in the OIV method illustrate the difference. For a dry wine with 11% alcohol measured at 18°C, the OIV correction to 20°C is $$c/1000 = 0.49/1000 = 0.00049$$ g/mL. For pure water over the same 2°C interval, the density change is about 0.00042 g/mL — roughly 15% smaller. The discrepancy grows at larger temperature offsets and for liquids with more dissolved solids.

This explains why the manufacturer correction table above gives values 1.6–2.4× larger than the pure water model: the table is calibrated for beer wort, which contains sugars, proteins, and other compounds that increase the thermal expansion beyond that of pure water.

A single pure-water-based correction is therefore only a first approximation. For homebrewing accuracy (±0.001–0.003 SG), it's usually good enough. For analytical precision, you'd need composition-specific tables.

## How much does temperature correction matter?

For a hydrometer calibrated at 20°C, measuring at typical room temperatures (20–25°C), the pure-water correction is about +0.001 SG. Even the larger manufacturer correction is at most +0.003 SG in this range. Since homebrewing hydrometers can be read to about ±0.001 SG, the temperature correction is comparable to but not dramatically larger than the reading precision. At 30°C the correction grows to +0.003–0.005 SG and becomes clearly significant.

In practice: if your sample is within a few degrees of the calibration temperature, the correction is small — on the order of one scale division. If you are 10°C off, it matters. For a companion post evaluating how large these errors are compared to other sources of instrument error, see [How accurate are homebrew hydrometers and refractometers?](/sugar-measurement-calibration/).

[^jones]: F.E. Jones and G.L. Harris, "ITS-90 Density of Water Formulation for Volumetric Standards Calibration," *J. Res. Natl. Inst. Stand. Technol.*, 97(3), 335–340 (1992). [PDF](https://nvlpubs.nist.gov/nistpubs/jres/097/jresv97n3p335_a1b.pdf).

[^oiv]: OIV, "Density and Specific Gravity at 20°C," Method OIV-MA-AS2-01A, in *Compendium of International Methods of Wine and Must Analysis* (R2012). [PDF](https://www.oiv.int/public/medias/2467/oiv-ma-as2-01a.pdf).

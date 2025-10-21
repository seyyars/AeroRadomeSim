---
title: "AeroRadomeSim: Numerical simulation of Mach-0–3 aerothermodynamics and temperature-dependent radome RF transmission"
tags: [python, aerodynamics, electromagnetics, radome, open-source]
authors:
  - name: Seyed Arsham Asgari
    orcid: 0009-0001-6783-2245
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 2025-10-21
bibliography: paper.bib
---

# Summary
*AeroRadomeSim* is an open-source Python library for quick, reproducible studies of near-sea-level compressible aerothermodynamics over Mach 0–3 and radome RF transmission with temperature-dependent dielectric properties. The package targets researchers and practitioners who need validated, lightweight building blocks that run in seconds and integrate easily with notebooks and CI.

# Statement of need
Aerothermal loads (dynamic pressure \(q\), recovery/stagnation temperatures, wall adiabatic temperature) and first-order skin-friction estimates are basic inputs to early-stage missile/vehicle design. In parallel, RF transmission through hot radome laminates depends on \(\varepsilon_r(T)\) and \(\tan\delta(T)\). Existing tools are either heavy/closed or split across domains. This library provides a minimal, well-tested, and documented bridge: aerothermo sweep + multilayer T-matrix (TMM) for TE/TM incidence with temperature-dependent material laws.

# Functionality
- **Aerothermo:** ISA-based property lookup and compressible relations to compute \(M\to \{q, T_0, T_\mathrm{aw}\}\), plus Reynolds-number-based \(C_f\) estimates for length scales.  
- **Radome RF:** Multilayer transmission using transfer-matrix (TMM) in amplitude and power, TE/TM, oblique incidence; temperature-dependent \(\varepsilon_r(T)\) and \(\tan\delta(T)\).  
- **Reproducibility:** Tests (pytest), CI (GitHub Actions), example figures (shown in README), and a versioned archive at Zenodo.

# Example
A 1-km altitude sweep reproduces the expected monotonic growth of \(q(M)\). For a 10-mm single-layer radome at 2.4 GHz, |S21| decreases as loss increases with temperature (300→420 K). The exact commands are in the README quickstart.

# Availability & reuse
MIT-licensed. Archived release for this submission: **Zenodo DOI [10.5281/zenodo.17408778](https://doi.org/10.5281/zenodo.17408778)**. Development occurs openly on GitHub (tests/CI included).

# Acknowledgements
The author thanks open-source maintainers of Python and scientific packages used in this work.

# References
See `paper.bib`.

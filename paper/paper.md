---
title: "AeroRadomeSim: Numerical simulation of Mach-0–3 aerothermodynamics and temperature-dependent radome RF transmission in Python"
tags: [Python, aerothermodynamics, radome, numerical simulation, reproducibility]
authors:
  - name: Seyed Arsham Asgari
    orcid: 0009-0001-6783-2245
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
---

# Statement of need
Early-stage sub/supersonic (Mach 0–3) studies on slender, axisymmetric flight bodies often need a fast, reproducible way to couple reduced-order aerothermodynamics with temperature-dependent multilayer radome transmission. Full CFD/EM stacks are costly to run and maintain. **AeroRadomeSim** is an open Python library that provides quick parametric sweeps and ready-to-cite figures/CSVs, targeting researchers and educators who want rapid exploration and reproducibility.

# Summary & methods
The aerothermodynamic module implements an ISA-like atmosphere (0–20 km), Sutherland’s law for viscosity, and a laminar–turbulent skin-friction blend with a mild compressibility correction. From a Mach sweep at a given altitude it returns velocity, dynamic pressure \(q\), stagnation temperature \(T_0\), adiabatic-wall temperature \(T_{\mathrm{aw}}\), and a characteristic Reynolds number \(Re_L\). Geometry helpers for slender, axisymmetric noses (e.g., ogive/cone) are provided.

The RF module uses the thin-film **transfer-matrix method** (TMM) for TE/TM polarizations and arbitrary incidence angles. Each dielectric layer is defined by thickness, relative permittivity \(\varepsilon_r\), and loss tangent \(\tan\delta\); temperature dependence is supported via user mappings \(\varepsilon_r(T)\), \(\tan\delta(T)\). The solver returns the complex forward transmission \(t=S_{21}\); power transmission is \(T=\mathrm{Re}(q_L)/\mathrm{Re}(q_0)\,|t|^2\), where \(q\) is the optical admittance (TE/TM). Example scripts generate frequency sweeps of \(|S_{21}|\) at multiple temperatures.

The repository ships plotting scripts that save **PNG** figures and **CSV** tables suitable for manuscripts. For instance, the provided script builds (i) \(q\)–Mach curves at 1 km and (ii) \(|S_{21}(f)|\) for a single heated radome layer, reproducing the screenshots in `docs/img/`_

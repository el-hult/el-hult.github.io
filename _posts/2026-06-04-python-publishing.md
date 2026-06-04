---
title: "A Python Package for ICD-10-SE codes, with a twist"
tags: ['python', 'packaging', 'publishing']
---
Today, I published my first Python package to PyPI. The interesting part is how it provides ICD-10 diagnosis code data without including any ICD-10 data files.

The package is called codeDx (available at [pypi.org/project/codedx/](https://pypi.org/project/codedx/)). The name is a play on codex (a collection) and Dx (the medical shorthand for diagnoses).

## Why a package?

This package fulfills my own needs. I've been working with a Swedish research database from Region Uppsala, analyzing healthcare contacts across hospital, primary, and outpatient specialist care. Coding practices vary across sectors. Our official data request specified ICD-10 codes, but we actually received a mixture of mostly ICD-10 and also something more. codeDx was built to make sense of this data. Because research reporting often requires English nomenclature, the package also handles translations from Swedish to English diagnosis names.

## The challenge

Three constraints combined into a puzzle:

**Licensing.** The ICD-10 standard is maintained internationally, and Sweden uses a national adaptation called ICD-10-SE. These data files carry licensing restrictions, and it is not clear to me when and how you can redistribute. I wanted to be on the safe side, so I needed the package to fetch data at install time rather than shipping it.

**Air-gapped deployment.** I run analyses on a high-performance computing cluster with no internet access. Packages must be bundled into Docker images and pushed into the environment. Runtime downloads — the usual workaround for large auxiliary data like pretrained models or benchmark datasets — were completely off the table.

**Slow file system.** The HPC environment runs on a Network File System (NFS), which is slow for repeated reads. Loading large CSV or XML files from scratch every time the module starts was not acceptable.

## Resolution

The solution combines two mechanisms: install-time downloads and runtime caching.

**Install-time downloads** happen when someone runs `pip install codedx` as part of a Docker build. To understand why this works, it helps to know how Python distributes packages. There are two main formats: a *wheel* (.whl) is pre-built and installs instantly with no build step. A *source distribution* (sdist, .tar.gz) ships raw source and triggers a build on the user's machine at install time. By distributing codeDx only as an sdist, I can hook into that build step to download the official data files directly from Socialstyrelsen, the WHO, and the CDC.

I chose [hatch](https://hatch.pypa.io/) as the build backend because it has a mature, well-documented hook interface. The uv build backend — my usual default — does not expose equivalent hooks yet. The hook itself is straightforward:

```python
class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name != "wheel":
            return
        for filename, url, label in _SINGLE_DOWNLOADS:
            dest = _DATA / filename
            if not dest.exists():
                print(f"[codedx build] Downloading {label}...", flush=True)
                _download(url, dest)
            build_data["artifacts"].append(str(dest))
```

That `if self.target_name != "wheel": return` guard was the hardest part to figure out. Hatch runs `initialize` for both sdist and wheel builds. I had excluded the data files from the sdist in `pyproject.toml` — but `build_data["artifacts"]` overrides the exclude list, force-including whatever you append. Without the guard, every sdist build silently bundled the licensed data I was trying to keep out. Once I understood that artifacts bypass the manifest, the fix was a single line.

**Runtime caching** happens on first import. The package builds a versioned local cache in the user's home directory, so NFS reads happen once rather than on every analysis run. Multiple versions can also coexist cleanly across different projects.

---

Right now, the package is far from polished, and I suspect I might be its primary user for the time being. Since it's published as an sdist, you can download and inspect the source if you're curious.

If you're working with similar Swedish health data, tackling air-gapped deployments, or want to chat about Python packaging quirks, feel free to reach out.

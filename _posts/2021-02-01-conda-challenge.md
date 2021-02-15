---
layout: post
title:  "Some exploration of conda"
tags: [conda, rlang, github]
---


I've spent almost a full day battling `conda`. My goal was to have a simple `environment.yml` file that I could `conda env create --file environment.yml` both on my windows machine as well as on a linux system. There was only one catch: I needed to install both official anaconda packages (e,g, `numpy`), from third party channels (`pytorch`) from PyPI (the package `cdt`) not on any conda channel, as well as some `r` packages not available in conda at all - bot those in CRAN (e.g. package `kpcalg`) and those not even there `PCIT` only on github).

I can simply say I failed. But I want to share some reflections on what I did and what I gave up.

# Building conda packages seems like a mess
If you have macOS you can follow the guide [here](https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-r-pkgs.html). The idea is simple:

1. Install the conda build tools `conda install conda-build`
1. Create a skeleton recepie for packages available on CRAN `conda skeleton cran kpcalg`
1. Build that recepie into a conda package and place that package in your local package directory `conda build ./r-kpcalg`
1. Install the package `conda install --use-local r-kpcalg`

Unfortunately this process failed and gave me super strange python compilation errors, and googling that told me someone on StackOverflow had this issue using wrong python version with Homebrew. I assume there is some error here because I use windows, and not macOS.

Also, I assume there is issues because the package in question relies on other R libraries that I have not installed. Those libraries are available though the channel `bioconda`, but involving extra channels to resolve the dependency tree seemed a bit too complicated for me at this stage.

If I would pursue this avenue late on, it seems to me the proper way is to construct R packages in the bioconda channel. Most prerequisites are available there.

# What I did
In the end I did this very direct. I had a `environment.yml` file for my environment. It installed the relevant python packages and all R packages that I could find in the regular conda channels. It furthermore installed some packages needed to install R packages from source. I needed `rtools`, `m2w64-gcc` and `m2w64-gcc-fortran`. The complete file was:

~~~yaml
name: Forskningsutmaningar
channels:
 - defaults
 - r
 - pytorch
dependencies:
  - numpy
  - pandas
  - seaborn
  - pytorch
  - cpuonly
  - pip
  - r
  - r-base
  - r-irkernel
  - r-essentials
  - rtools # for compiling R libraries from source
  - m2w64-gcc # for compiling R libraries from source
  - m2w64-gcc-fortran # for compiling R libraries from source
  - pip:
    - cdt
    - -e .
~~~

After completing `conda env new --file environment.yml` I ran `Rscript.exe ./r_deps.r` with the content below.
The code is commented inline. It installs some libraries, and most of them from source.
The reason for that is twofold: 
(1) Github install needs to be from source and I do that in R 3.6.0, and therefore its dependency MASS needs to be compiled in 3.6.0, but the CRAN version is 3.6.3, so it fails unless I compile that from source too.
(2) Conda gives me R 3.6.0, but most compiled packages are for 3.6.3, so if I don't install from source I get warnings all the time.... 

All packages installed are also loaded with `library(..)` to ensure that the load works as expected.

~~~r
## Set a default repo
local({r <- getOption("repos")
       r["CRAN"] <- "http://cran.r-project.org" 
       options(repos=r)
})


# conda installing rtools don't add to path correctly, so here is a fix for that.
prefix <- Sys.getenv("CONDA_PREFIX")
rtools_path <- paste(prefix, '\\rtools\\bin', sep="") #n.b. escaped backslashes in windows...
Sys.setenv(PATH = paste(rtools_path, Sys.getenv("PATH"), sep=";"))
Sys.setenv(BINPREF = "C:/Rtools/mingw_$(WIN)/bin/")

# BioConductor installs for two libraries not available on CRAN
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install(c("graph","RBGL"))
# CRAN installs
pkgs = c('pcalg','kpcalg','momentchi2','devtools', 'MASS')
for( pkg in pkgs){ 
    install.packages(pkg, type='source')
    library(pkg,character.only=TRUE)
}
# Github installs
library('devtools')
install_github("Diviyan-Kalainathan/RCIT")

library('RCIT')
~~~

This procedure worked. So that is good. But I finished off with discovering what seemed a [bug in CDT](https://github.com/FenTechSolutions/CausalDiscoveryToolbox/issues/93).
Probably it is something related to matplotlib versions and how they do their imports. But I'm not sure... The conclusion of that little bug hunt is that one cannot do any `cdt` imports after `matplotlib` or `seaborn`. That is....

~~~python
# OK!
import cdt
import matplotlib.pyplot as plt
~~~

~~~python
# Not OK!
import cdt
import matplotlib.pyplot as plt
from cdt.causal.graph import PC
~~~

Probably this will get fixed in later versions when they make new library builds...
---
title:  "On Haskell Builds"
tags: [haskell, cabal, stack, functional programming, advent of code]
---

Currently, Im about to finish my [AoC 2016](https://adventofcode.com/2016) code in Haskell.
The main motivation is that I will be Teaching Assistant in a Functional Programming course this fall, and wanted to brush up on my skills.
Below are my notes regarding project setups, and they should reflect my own state of learning.

You find the code [here](https://github.com/el-hult/adventofcode2016) if you want to give it a glimpse.

## The Jigsaw
My understanding here builds a lot on [this video by Haskell At Work](https://www.youtube.com/watch?v=a7R-2vtPLDM). You should watch that too.

In advent of code, one solves 25 problems with low or little interdependency. You typically code a library of solvers for solving each day of Advent of Code, some general utility functions to reuse between days, test suites, and finally executable(s) that run the solver code. One uses the build tool [Cabal](https://www.haskell.org/cabal/) inthe Haskell ecosystem to manage the build process, but there are several other technologies in play, making the whole setup a bit messy. Some core concepts are:


Modules
: A Haskell module is a set of code collected in a source file. The module name should generally match the file name. You import a module like `import Control.Monad.State` and define your own modules with syntax like `module My.Library where` at the top of the file. If the module has a `main` function in it, you can build the module into an executable. Examples of modules are `Data.List` or `Text.Pandoc`.

Libraries
: In Cabal, a library is a set of modules where some are exposed to users and some are hidden. So you could have a library with all the solvers and utilities, or several different libraries for each day.

Executable
: In Cabal, a module with a `main :: IO ()` function can be denoted an executable, and in that case Cabal will compile the module, link to compiled modules, and produce an executable having `main` as the entry point.

Test suites
: In Cabal, a with a `main :: IO ()` function can be denoted a Test suite. Tests of the type `exitcode-stdio-1.0 ` (the default) are built, run, the exit code is inspected. If the exit code is 0, the tests went well. Often, this is a "gate", and if the tests fail, it wont bother building executables.

Packages
: In Cabal, libraries, executables and test suites can be bundeled together into a package. Packages can be distributed through e.g. [hackage](https://hackage.haskell.org/). You can install packages via `stack install XX`, and when you install them, they expose both their executables and their libraries. So for example, the package [pandoc](https://hackage.haskell.org/package/pandoc) exposes the module `Text.Pandoc.XML` for working with XML, but it also exposes the executable `pandoc` that you can use for converting XML to and from other formats.

Projects
: In Cabal, you can collect many packages into a project. To build a package, Cabal keeps track of what source files have changed, so it only rebuilds that parts that it needs. If you break your code into smaller packages, this build step goes much faster, as the dependencies are in general smaller. Within your project, you can still make imports between packages, since all built packages are exposed to each other.

Build targets
: Tests, executables, libraries, packages or projects can all be build targets. So when you compile, run, and test your code, you can specify that you only want a certain package to be compiled. This is very useful to run only some test suites.

`.cabal`-files
: Each package is defined by a cabal-file. It is a special file format defining package name, dependencies and its build targets (library, executable, tests). There is also a special cabal-file in the project root, telling Cabal what packages there are to build.

`package.yaml`
: Since the Cabal file format is a bit tedious, there is a tool called [hpack](https://github.com/sol/hpack). It is a yaml-to-cabal converter. It is simply a nicer interface. When building with hpack, you get a generated cabal-file, so if there are build errors, you can always check the cabal-file. If it looks bad, you might have to edit the `package.yaml` file so it generates a proper `.cabal`-file. You get one `package.yaml` for each `.cabal`, and put one inside each pacakge.

`stack.yaml`
: Since Cabal has been historically bad at caching built projects, combining global and local dependencies, and since Hackage is so full of incompatible package versions, the tool [stack](https://docs.haskellstack.org/en/stable/README/) helps you build faster, and with better reproducibility. You configure stack via `stack.yaml` in the *project* root (not the *package* root, but in single-package-projects they happen to coincide). Stack always uses hpack, so you never need to invoke hpack yourself.

## How I assembeled it

As can be seen in the state of [my code per 2021-07-16](https://github.com/el-hult/adventofcode2016/tree/c3860a83c9844b4c94ffb771a2161dcd6f65ed4f) - I first decided to have a single package with one executable, the solver for each day as a Module, and common code in another module. That package is in the folder `old`, is named `adventofcode2016` (look into the `package.yaml`!), and has an executable called `aoc2016`.  The tests are implemented in a single large test file written with [HUnit](https://github.com/hspec/HUnit). This structure is far from ideal, since that meant that each build would link together ~ 20 different modules, and each test always re-tests old tests. The builds became slower and slower as I completed more days. I gradually started developing the code for each day in ghcid, and when it was complete, I moved to the 'proper' setup. This was of course very unsatisfying. 

One solution is to disassembeled the project structure, so that stack can track what is updated and needs to be run, and what is not touched. I started to do one package per day (implemented in `day20` and `day21`), plus a package for common utilities (package `util` in folder `util` with module `Util`, a single test and no executable). Each packages contains its own tests. Each package may have different dependencies (e.g. only some days use parsec, so it is nice to only pull it in when needed). All in all, this created a shorter feedback loop, which is very nice.

In a tiny "day-package", one could have a single module acting as both library and executable, and no tests. In that case, the source file may lie in the package root. But if there are several files, and they have different dependencies (e.g. test files depending on HUnit), one must divide the source files into separate folders. That way, cabal can easily understand what dependencies are relevant for what modules, by specifying separate build targets, and the hpack label `source-dirs`. Otherwise, Cabal could think that the `Spec.hs` file is a part of the library, and try to compile it as such (with no link to HUnit).

As I moved to this better tructure, I looked at [taschan aoc2018](https://github.com/tomasaschan/advent-of-code-2018), since he has some better ideas about project setups. I tried not to do it exactly like him, but it was hard not to in the end. One change is that he uses [hspec](https://hspec.github.io/) for test specification. One nice thing with hspec is that it has test discovery, and you can avoid the boiler plate for that. I have mixed and matched between explicit test runners, the automatic test runner of hspec, and plain HUnit.

The `stack.yaml` file is very small. It is for me just a reference to how stack should resolve package versions, and then a list of my own project packages.

 
# Honorable mentions
I use [vscode](https://code.visualstudio.com/) with the [Haskell extension](https://marketplace.visualstudio.com/items?itemName=haskell.haskell). It is great, and I think it beats the other extensions due to the Language Server.
Do note that the extension plugin works best with either a *global* GHC-installation, *or* stack projects in local mode. I got the [advise on Stack Overflow](https://stackoverflow.com/questions/68191196/global-ghc-from-stack?noredirect=1#comment120534459_68191196) to only use local stack projects, and it seemed to be a good idea.

I sometimes use [ghcid](https://github.com/ndmitchell/ghcid) for small code adventures.
It is fabulous.
It is a fast reloading ghci wrapper that supports reporting typed holes, syntax- and type errors and so on.
I can REALLY recommend ghcid for small toys that only require a single file or so. Super quick and helpful!
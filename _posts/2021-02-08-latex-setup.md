---
layout: post
title:  "My current LaTeX setup"
---

LaTeX is a constant source of frustration of mine. And I guess it is the same for many others. In this writeup I'll explain my current setup and why I like it. 

# What do you want?

## Why not just Overleaf?
But before that, I wan't to admit that I often use [Overleaf](https://overleaf.com/), and in all those cases I just use defaults. Overleaf is also GREAT in many situations, but it lacks things that many editors can do - such as find and replace in many different files. And file renames simpler. And moving files between folders. So that is a bummer. It can sometimes be a bit funny with some libraries as well. But overall it is quite nice, and it is my go-to for writing tex together with others.

So I do have a tex-setup that I run locally. I use it often for various types of notes that need typesetting. I want it to be simple and straightforward, while still being somewhat consistent with the other coding environments that I use. And this is where there comes many choices.

## What more did fail?

- Editing tex in PyCharm is acceptable, but managing the build pipeline was terrible. I use pdflatex+bibtex+pdflatex+pdflatex and that was just not nice. Previews was so-so.
- Editing tex in vscode is quite nice. The plugin Latex Workshop has many nice features, and the build system with tools and recipies allows one to make the customization one wants in a quite straightforward and tex-y fashin. Handling output errors and warnings was a pain though. It tries to link errors to source files and show in the editor, and that was really slow and error prone. Did not like!
- TexWorks. This is the "standard" editor with TexLive. I like it quite a bit because it is simple and fast. But whenever I change the bibliography I need to do the whole pdflatex+bibtex+pdflatex+pdflatex manually. And if i *don't* change the bibfilde (most common) I don't want to run that same toolchain. Also the hotkeys in the editor feels very wrong, and the pdf viewer is so-so. The find-and-replace function in the editor is not nice at all.
- Custom powershell script for a watcher that observes the main tex-file and reruns the toolchain at every save. This was quite nice and surprisingly fast. It seems there is so little overhead that rerunning pdflatex many times was quite acceptable. But on the downside, it becomes unreasonably complex to build a watcher that checks all other includes and bib-files and all. So NO!

# What I did

## Setup / installation

First I got [Sumatra PDF](https://www.sumatrapdfreader.org/) and set it as a default pdf viewer. I'm at version 3.1.2. It is a nice pdf-viewer that:

1. is FAST
2. supports editing pdf-files in the background while having the file open
3. supports SyncTex

It reads djvu-files, so I use as a complement to Acrobat Reader. Since I use Acrobat Reader to annotate pdf's (e.g. correcting homeworks from students), I enjoy the "Open this file in Acrobat Reader" button. Sumatra is a *reader* so it cannot be used for annotations itself.


Then I got [Notepad++](https://notepad-plus-plus.org/). I'm at version 7.5.4. It is a very simple and nice editor that:

1. has reasonable key bindings
2. has good find/replace
3. Is very simple and general purpose - i use it on huge csvs, xml-files, markdown, and other stand alone files that is not part of a project/folder (as most IDEs assume)
4. has some scripting support

I then got [TexLive](https://tug.org/texlive/) in the basic install. I'm at the release TexLive2020. This includes most common toolchains and things. It also bundles the tool `latexmk`. It is a build tool that coordinates what toolchain to run, and can monitor the file system for updates so it runs the relevant scripts when the tex-files are updated.

## The workflow

I first create a folder for my project, open a terminal in that folder and run `latexmk main.tex -pdf -pvc -pdflatex="pdflatex -synctex=1"`. This code compiles the file `main.tex` into `main.pdf`, and opens the results in Sumatra PDF. It also makes sure that the synctex file is created so that one can go quickly between source code and pdf. The command also watches the files for edits and recompiles as necessary. Sumatra will always have the latest successful compilation open. You might want to pass some other arguments depending on your personal workflow, see [the documentation on CTAN](https://www.ctan.org/pkg/latexmk/)

I use notepad++ as an editor. And if I want to preview a specific part of the pdf related to the line I am editing I use a synctex forwards search. The first time, I do this by pressing F5, and pasting into the run-box. Make sure that the paths to Sumatra and to Notepad is correct. I save this run command and bind it to `Ctrl+Shit+A` which is a free hotkey that sits nice on the keyboard.

~~~
"C:\Program files\SumatraPDF\SumatraPDF.exe" -forward-search "$(FULL_CURRENT_PATH)" $(CURRENT_LINE) -inverse-search "\"C:/Program Files (x86)/Notepad++/notepad++.exe\" \"%f\" -n%l" "$(CURRENT_DIRECTORY)"/"$(NAME_PART)".pdf
~~~

This command both makes Sumatra open the relevant PDF and highlight the relevant part of the PDF, but also configures Sumatra for a reverse search. Just double-click some text in the pdf, and Notepad++ will show the source for that text. Also, I don't think that command worked just a year ago, so check out the latest [Sumatra documentation for work with TeX](https://www.sumatrapdfreader.org/docs/Use-Sumatra-as-a-pre-viewer-for-LaTeX-editors.html)

## Summary
Use Notepad++, Sumatra and latexmk. It is not very fancy, and it requires a little bit of config to get SyncTex to work, but it is very very fast and it uses all the building blocks in the way they were designed to work.

# Acknowledgements
A lot of my first inspiration was from  https://william.famille-blum.org/blog/static.php?page=static081010-000413, but since that article is very old, most of the actual code did not work. But it got me inspired to do this in a way that suited me.

[This post](https://mg.readthedocs.io/latexmk.html) is how I realized you cannot ask latexmk to create synctex files, but you pass it as a pdflatex command. I find that annoying, but it is okay. I also think it is fun that this post often comes higher than the official documentation.
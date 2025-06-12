<br/>
<p align="center"> <img src="icon.png" alt="Logo" width="150"> </p>
<h3 align="center"> Stag </h3>
<h3 align="center"> Upgrade your hierarchical filesystem with a tag-based structure </h3>
<br/>

# Overview
**Stag** (**S**imple **Tag**ger) is a FUSE-based filesystem that upgrades a hierarchical filesystem to support a tag-based folder structure. It turns tags into folders, while remaining compatible with a standard Unix utilities and file managers.

Key features are:

- **Tags are Folder**: Each tag corresponds to a folder in your filesystem, which stack recursively for files with multiple tags.
- **Files are Files**: Each file that you tag will show up in one or more folders, integrating seamlessly with any file manager.
- **Same Tools as Usual**: Browse and manage your files the same way you would before, using your favorite file manager or the CLI.

<!--- TODO: meter imagem/gif que eu desenhei no remarkable aqui -->

# Installation

The requirements to run Stag are:

- Python (version 3)
- [Click](https://click.palletsprojects.com/en/stable/)
- [fusepy](https://github.com/fusepy/fusepy)

To install Stag, download the Python script to your machine

```console
$ wget https://github.com/jpmvferreira/stag/blob/master/stag
```

set it as executable

```console
$ chmod +x stag
```

and place it somewhere in your `$PATH`, e.g.

```console
$ mv stag ~/.local/bin
```

Finally, check if the program is installed successfully by running

```console
$ stag --help
```

<!--- TODO: AUR -->

# Usage

<!---
TODO: guide que mostra todas as funcionalidades presentes no Stag com uma breve explicacao
- init repo
- adicionar ficheiros a repo
- criar tags
- associar tags a ficheiros
- remover tags de ficheiros
- remover tags
- remover ficheiros
 -->

# Similar Projects

As far as I know, there is only one project similar to this: [TMSU](https://tmsu.org/). It has more features than Stag and is actively maintained. However, it does more than what I need it to do, I don't like the folder structure and the CLI was quite complicated. It is also written in Go, which I am not familiar with.

Therefore, I decided to make my own version of TMSU, with ~~blackjack~~ smaller codebase and ~~hookers~~ less features. This makes the program more constrained, while still doing what I want it to do, more user friendly and easier to maintain.

# Contributing

This is a small program developed by somebody who is not an experienced programmer. If you have any comments, feedback, suggestions or even feature requests, don't hesitate in opening a ticket or a discussion in the Github repository.

# References

<!--- TODO -->

# License
[MIT](./LICENSE.md).

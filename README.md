<br/>
<p align="center"> <img src="icon.png" alt="Logo" width="150"> </p>
<h3 align="center"> Stag </h3>
<h3 align="center"> Upgrade your hierarchical filesystem with a tag-based structure </h3>
<br/>

# Overview
**Stag** (**S**imple **Tag**ger) is a FUSE-based filesystem that upgrades your filesystem to support a tag-based structure. It turns tags into folders and remains compatible with a standard Unix utilities and file managers.

Key features are:

- **Tags are Folder**: Each tag corresponds to a folder in your filesystem, which stack recursively for files with multiple tags.
- **Files are Files**: Each file that you tag will show up in one or more folders, integrating seamlessly with any file manager.
- **Same Tools as Usual**: Browse and manage your files the same way you would before, using your favorite file manager or the CLI.

<!--- TODO: meter imagem/gif que eu desenhei no remarkable aqui -->

# Installation

The dependencies to run Stag are:

- [Python](https://www.python.org/) (version 3)
- [Click](https://click.palletsprojects.com/en/stable/)
- [fusepy](https://github.com/fusepy/fusepy)

## Manual Installation

After ensuring the dependencies are satisfied, download the Python script to your machine, e.g. using `wget`

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

<!--- TODO: AUR, criar stag-git porque nao tenho versoes -->

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

# Motivation

Ever you ever started doing some spring cleaning and realized that

```console
$ find wallpapers -type f | wc -l
1603
```

and, as if this is not bad enough already, you stumbled across

```console
$ find memes -type f | wc -l
1377
```

Yeah... But, you know what could help you sort all of this mess? That's right: ~~stop hoarding~~ Tags! So I just need to find a program that:

1) Tags file(s);
2) Integrates with the filesystem to browse the files and tags;
3) Uses terminal utilities to interact with files and tags.

As far as I know, there is only one project that comes close to this: [TMSU](https://tmsu.org/). However, I don't like the folder structure and the CLI was quite complicated. Besides, the interaction via filesystem is lacking to me. It is also written in Go, which I am not familiar with.

Therefore, I decided to make my own version of TMSU, with ~~blackjack~~ smaller codebase and ~~hookers~~ better filesystem integration.

# Contributing

This is a small program developed by somebody who is not an experienced programmer. If you have any comments, feedback, suggestions or even feature requests, don't hesitate in opening a ticket or a discussion in the Github repository.

If you would like to submit code, you will need basic knowledge of Python, SQL and FUSE. Both the CLI and the filesystem are implemented in the file [stag](./stag). After making any change there, make sure it passes the tests. The test units use [pytest](https://docs.pytest.org/en/stable/).

# References

The **fusepy** Github repository:

- https://github.com/fusepy/fusepy
- Mainly the file `fuse.py` where the FUSE object is implemented

The **libfuse** documentation:

- https://libfuse.github.io/doxygen/index.html
- Emphasis to the file where the operations available in a FUSE filesystem are defined (Data Structures > fuse_operations)

# License
[MIT](./LICENSE.md)

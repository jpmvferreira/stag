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
- correr no background (nao sei se deveria ser uma subseccao a parte ou nao)
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

As far as I know, there is only one project that comes close to this: [TMSU](https://tmsu.org/). However, I don't like the folder structure, the CLI is quite complicated and the interaction via filesystem is lacking. It also does more than what I want it to.

Therefore, I decided to make my own version of TMSU, with ~~blackjack~~ smaller codebase and ~~hookers~~ better filesystem integration.

# Contributing

This is a small program developed by somebody who is not an experienced programmer. If you have any comments, feedback, suggestions or even feature requests, don't hesitate in opening a ticket or a discussion in this repository.

# Disclaimer

Stag is a personal project, not enterprise grade software. I use it myself and it works well for me, but bugs can happen, so don’t trust it with important files unless you’ve got backups (which you should always have anyways!). Stag repositories are kept in a single folder, so backing up is very straight forward.

# References

The [fusepy](https://github.com/fusepy/fusepy) Github repository, in particular the Python object FUSE implemented in `fuse.py`.

Also the official [libfuse](https://libfuse.github.io/doxygen/index.html) documentation, mainly the file that defines the operations available in a FUSE filesystem (Data Structures > fuse_operations).

# License

[MIT](./LICENSE.md)

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

- [FUSE](https://github.com/libfuse/libfuse)
- [Python](https://www.python.org/) (version 3)
- [Click](https://click.palletsprojects.com/en/stable/)
- [fusepy](https://github.com/fusepy/fusepy)

Installing these packages depends on your system, but both Click and fusepy are available via pip.

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

<!--- TODO: AUR, criar stag-git porque nao tenho versoes por enquanto, meter aqui systemd unit -->

# Usage

Stag stores its files in the environmental flag `$STAG_SHARE`. This flag is required for the program to work. My advice is that you add the following line in your `.bashrc` or equivalent

```bash
export STAG_SHARE="$HOME/.local/share/stag"
```

With that out of the way, you can now create a new repository, let's call it `myrepo`, with

```console
$ stag --init myrepo
```

You can list all repositories you have created so far using

```console
$ stag --ls
```

The way you interact with Stag is via filesystem calls, via your favorite text editor or CLI tools. But first, you have to mount it, which you can by running

```console
$ mkdir mnt
$ stag --mount myrepo mnt
$ cd mnt
```

This is where you would add your files to the mount directory, the same way you usually would: by copying them or moving them to the corresponding folder. For illustration purposes, let's create some dummy files

```console
$ touch lisbon.txt
$ touch berne.txt
$ touch venice.txt
```

We would like to add some tags. In Stag, tags are directories, so to create the tags `city`, `mountains` and `ocean` we execute

```console
$ mkdir city ocean mountains
```

To add a tag to a file we use `ln`. Here's how we add the tag `city` to the file `lisbon.txt` and `venice.txt`

```console
$ ln lisbon.txt city
$ ln venice.txt city
```

You can add multiple tags at the same time, for instance to add `city` and `mountains` to `berne.txt`

```console
$ ln berne.txt city/mountains
```

If you would like to remove tags from a file, you use `rm` and specify the path of the file. For instance

```console
$ rm city/berne.txt
```

will remove the tag `city` from `berne.txt`, and

```console
$ rm city/mountains/berne.txt
```

will remove both tags `city` and `mountains`. If you would like to remove the file from the repository, you call `rm` with the file path in the root of the mount directory

```console
$ rm berne.txt
```

You can also remove tags from the repository with

```console
$ rmdir mountains
```

> [!CAUTION]
> Never use `rm -r` to remove tags, which issues an `rm` on each individual file. Only use `rmdir`to remove tags from the repository.

There's another way of removing and adding tags to files, using the `mv` command. Running

```console
$ mv <tags>/file.txt <tags2>/file.txt
```

will remove every tag from `file.txt` and replace them with `<tags2>`, while `<tags>` is ignored.

You can also use `mv` to rename a file, however, you have to do it in the same folder, i.e.

```console
$ mv <tags>file.txt <tags>/newname.txt
```

To rename tags you don't have such restriction, you can run

```console
$ mv <tags>/<tag> <tags2>/<tag2>
```

to rename `<tag>` to `<tag2>`, and if `<tag2>` already exists, it will merge them together.

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

Stag is a personal project, not enterprise grade software. I use it myself and it works well for me, but bugs can happen, so don’t trust it with important files unless you’ve got backups (which you should have anyways!). Stag repositories are kept in a single folder in `$STAG_SHARE`, so backing up is very straight forward.

# References

The [fusepy](https://github.com/fusepy/fusepy) Github repository, in particular the Python object FUSE implemented in `fuse.py`.

The official [libfuse](https://libfuse.github.io/doxygen/index.html) documentation, mainly the file that defines the operations available in a FUSE filesystem (Data Structures > fuse_operations).

# License

[MIT](./LICENSE.md)

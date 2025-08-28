<br/>
<p align="center"> <img src="icon.png" alt="Logo" width="150"> </p>
<h3 align="center"> StagFS </h3>
<h3 align="center"> Upgrade your hierarchical filesystem with a tag-based structure </h3>
<br/>

# Overview

**StagFS** (**S**imple **Tag**ger) is a FUSE-based filesystem that upgrades your filesystem to support a tag-based structure. It turns tags into folders and remains compatible with a standard Unix utilities and file managers.

Key features are:

- **Tags are Folder**: Each tag corresponds to a folder in your filesystem, which stack recursively for files with multiple tags.
- **Files are Files**: Each file that you tag will show up in one or more folders, integrating seamlessly with any file manager.
- **Same Tools as Usual**: Browse and manage your files the same way you would before, using your favorite file manager or the CLI.

StagFS is fully functional, but it's **still in alpha**, so things might change a bit before the first full release. Once everything settles down, I'll start putting out official versions.

# Installation

## Requirements

Before running StagFS, ensure you have the following dependencies installed

- [FUSE](https://github.com/libfuse/libfuse)
- [Python 3](https://www.python.org/) (version 3.6 or newer recommended)
- [Click](https://pypi.org/project/click/) (Python package for command-line interfaces)
- [fusepy](https://pypi.org/project/fusepy/) (Python bindings for FUSE)

## Manual Installation

StagFS is distributed as a standalone Python script that you can easily download with

```console
$ wget https://github.com/jpmvferreira/stagfs/raw/refs/heads/master/stagfs
```

make it executable

```console
$ chmod +x stagfs
```

and move it to a directory in your `$PATH`, e.g.

```console
$ mv stagfs ~/usr/bin/stagfs
```

To run StagFS in the background with Systemd, download the provided unit file and place it in your user systemd directory

```console
$ wget https://github.com/jpmvferreira/stagfs/raw/refs/heads/master/stagfs@.service -O ~/.config/systemd/user/stagfs@.service
$ systemctl --user daemon-reload
```

# Usage

To get started with StagFS, begin by creating a new repository. For example, to create a repository called `myrepo`

```console
$ stagfs init myrepo
```

> [!NOTE]
> StagFS assumes the repository is located in `~/.local/share/stagfs` by default. This can be overwritten using the flag `-r`.

You can list all repositories at any time with

```console
$ stagfs ls
```

StagFS works by mounting your repository as a virtual filesystem. To do this, create a mount point and mount your repository

```console
$ mkdir mnt
$ stagfs mount myrepo mnt
$ cd mnt
```

> [!TIP]
> If you use the Systemd unit file, you can mount a repository in the background with:
> ```
> systemctl --user start stagfs@<repository name>:<mount point>
> ```
> Systemd will warn you about using `/`, to avoid issues, replace all `/` with `-`, e.g.:
> ```
> systemctl --user enable now stagfs@wallpapers:-home-user-wallpapers-
> ```

Add files to your repository as you would in any directory, by copying or moving them into the mount point. For demonstration purposes, let's create the following files

```console
$ touch lisbon.txt bern.txt venice.txt
```

In StagFS, tags are directories. To create tags such as `city`, `mountains`, and `ocean`

```console
$ mkdir city ocean mountains
```

To add a tag to a file, use the `ln` command. For example, to tag `lisbon.txt` and `venice.txt` with `city`

```console
$ ln lisbon.txt city
$ ln venice.txt city
```

You can add multiple tags at once, for instance, to tag `bern.txt` with both `city` and `mountains`

```console
$ ln bern.txt city/mountains
```

If you wish to remove a tag from a file, use `rm` with the path to the file inside the tag directory

```console
$ rm city/bern.txt
```

this will remove the tag `city` from ``bern.txt`, leaving other tags untouched.

It's possible to remove multiple tags at once, e.g., both `city` and `mountains` from `bern.txt` with

```console
$ rm city/mountains/bern.txt
```

To remove a file entirely from the repository, delete it from the root of the mount point

```console
$ rm bern.txt
```

To remove a tag from the repository:

```console
$ rmdir mountains
```

> [!CAUTION]
> Do **not** use `rm -r` to remove tags, as it will attempt to delete all files within the tag. Always use `rmdir` to safely remove tags.

It is possible to manage both tags and files using `mv`. For instance

```console
$ mv <old_tags>/file.txt <new_tags>/file.txt
```

will remove **all** tags from `file.txt`, disregarding `<old_tags>`, and add `<new_tags>`.

If you want to rename a file, you must call `mv` within the same path and change the file name, i.e.

```console
$ mv <tags>/file.txt <tags>/newname.txt
```

For renaming tags, you can run

```console
$ mv <tags>/<tag> <tags_alt>/<tag_new>
```

where `<tags>` and `<tags_alt>` are ignored and `<tag>` will be renamed to `<tag_new>`. If `<tag_new>` already exists, they will be merged.

> [!NOTE]
> To avoid ghost overwrites, StagFS does not allow you to change the name of a file to one that already exists. As for tags, it will refuse to change the name to a tag that is not visible in the current subdirectory to avoid ghost merges.

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

StagFS is a personal project, not enterprise grade software. I use it myself and it works well for me, but bugs can happen, so don’t trust it with important files unless you’ve got backups (which you should have anyways!). StagFS repositories are kept in a single folder, so backing up is very straight forward.

# References

The [fusepy](https://github.com/fusepy/fusepy) Github repository, in particular the Python object FUSE implemented in `fuse.py`.

The official [libfuse](https://libfuse.github.io/doxygen/index.html) documentation, mainly the file that defines the operations available in a FUSE filesystem (Data Structures > fuse_operations).

# License

[MIT](./LICENSE.md)

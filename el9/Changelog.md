# Changelog el9

## 01-12-2023
* Add `tmux` package as requested in https://github.com/cms-sw/cms-docker/issues/237.

## 28-11-2023
* Add `squid` package as requested in https://github.com/cms-sw/cms-docker/issues/235.

## 05-10-2023
* Add `python3-pip` package to install comp tools, e.g. Rucio (`Dockerfile` in https://github.com/cms-sw/cms-docker/commit/35ad9f96b2e9ed6403ed1d49b41b0e06cc92c29c
and `Docker.runtime` in
https://github.com/cms-sw/cms-docker/commit/afa5d94f461e261b9d2b90cddb00fd75f9565f36).

## 29-09-2023
* Split original `Dockerfile` in independent images (`Dockerfile.runtime`,
`Dockerfile.grid` and `Dockerfile.buildtime`). **Note:** Image for `ppc64le` disabled in `config.yaml`.

## 10-01-2023
* Add `glibc-langpack-en` package (https://github.com/cms-sw/cms-docker/commit/a2a6ca43d91bca7227a46b88e1b5096c97391069).

## 17-06-2022
* Add `boost-python3` package
(https://github.com/cms-sw/cms-docker/commit/f5df618dacf5974de6c35d739fd565465f6648e9).

## 13-01-2022
* Add `perf` package (https://github.com/cms-sw/cms-docker/commit/3be4202edd5d1388c5b4482d2a4c567c9b037618).

**Previous changes not tracked. See git history.**

### From el8 to el9
A few notes on the change from `el8` images to `el9`:
* Remove `perl` dependencies. We do not build perl-based SCRAM for `el9`.
* Drop Python 2.X and, therefore, remove `python2`, `python2-psutil` and `python2-requests` packages.
* Drop `libstdc++-static` and `libidn` dependencies from the first commit (as expected from `el8` image comments).
* Remove keberos config fix `ADD krb5.conf /etc/krb5.conf`.
* Add `texinfo` from `crb` repo.
* Package `coreutils-single` added Dockerfile (for `el8` it is defined as `DEFAULT_PACKAGE` in `config.yaml`).
* Packages `krb5-devel` and `libcom_err-devel` present in `el9` from first commit, but not present in `el8`.

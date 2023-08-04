# Changelog of Rohmann's Python Library
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.1.2] GBA 2023-04-20

### Added
- functions to slit strings into chunks:
  - split_str_into_chunks()
  - split_bin_str_into_chunks()
  - split_hex_str_into_chunks()

## [1.1.1] GBA 2023-04-18

### Changed
- update unit tests: run folder ".test" [Issue](https://rohmann.atlassian.net/browse/HIL-357)
- convert_to_int_list can now convert lists like '[0,1]'

## [1.1.0] GBA 2023-04-11
### Added
- bit handling
- byte handling

### Changed
- update unit tests

## [1.0.0] GBA 2023-03-27

### Added
- init stuff
- system types
- system types: added DeviceType and DeviceVariant

### Changed
- rename: Project ro ProjectName
- rename: DeviceType to LogicDeviceType

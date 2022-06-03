<img src=img/gcode_modifier_logo.JPG alt="G-Code Modifier Logo" width="241" height="256">

--------------------------------------------------------------------------------
[![MIT-License](https://img.shields.io/github/license/johanneshagspiel/gcode-modifier)](LICENSE)
[![Top Language](https://img.shields.io/github/languages/top/johanneshagspiel/gcode-modifier)](https://github.com/johanneshagspiel/gcode-modifier)
[![Latest Release](https://img.shields.io/github/v/release/johanneshagspiel/gcode-modifier)](https://github.com/johanneshagspiel/gcode-modifier/releases/)
# G-Code Modifier

This repository contains the created for the "JPacman" game. "JPacman" was originally developed by [Arie van Deursen](https://github.com/avandeursen) and is a recreation of the "Pacman" game in Java.

## Features

The [test suite](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman) contains a variety of different test such as:

- [unit](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/npc/ghost/ClydeTest.java) [tests](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/npc/ghost/InkyTest.java) made with [JUnit](https://junit.org/junit5/)
- [boundary tests](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/board/WithinBordersTest.java) using a 1x1 domain testing strategy
- [tests](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/level/CollisionMapTest.java) made with [Mockito](https://site.mockito.org/) to increase observability and controllability
- [fuzz testing](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/default-test/java/nl/tudelft/jpacman/fuzzer/JPacmanFuzzer.java) to determine a potential security vulnerability of a plugin
- [system tests](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/integration/suspension/SuspendSystemTest.java) based on system requirements
- [model based tests](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman/integration/GameStateTest.java) for which first a [UML state machine](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/doc/images/singlelevel_state_machine.jpeg) was created which then was turned into a [transition tree](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/doc/images/singlelevel_transition_tree.PNG) and then finally into a [transition table](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/doc/images/singlelevel_transition_table.PNG)

Most of these tests were created directly on the basis of user stories found in the [requirements document](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/doc/scenarios.md) in line with agile methodologies. Finally, "JPacman's" functionality was extended in a test-driven manner in order to support [multi-level games](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/main/java/nl/tudelft/jpacman/game/MultiLevelGame.java)

## Tools

| Purpose                | Name                                                                                                                     |
|------------------------|--------------------------------------------------------------------------------------------------------------------------|
| Programming language   | [Java](https://openjdk.org/)                                                                                             |
| Dependency manager     | [Gradle]()                                                                                                               |
| Version control system | [Git](https://git-scm.com/)                                                                                              |
| Unit testing framework | [JUnit](https://junit.org/junit5/)                                                                                       |


## Installation Process

It is assumed that both a [Java JDK](https://openjdk.org/) and an IDE such as [IntelliJ](https://www.jetbrains.com/idea/) or [Eclipse](https://www.eclipse.org/ide/) are installed.

- Import the repository as a gradle project and resolve all dependencies.
- Run the game by executing the main method in the [Launcher class](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/main/java/nl/tudelft/jpacman/Launcher.java).
- Execute the tests in the [test suite](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/src/test/java/nl/tudelft/jpacman)

## Contributors

The authors of the "JPacman" game can be found [AUTHORS](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/AUTHORS.md) file and the repository of the original source code can be found [here](https://github.com/SERG-Delft/jpacman-framework).

This test suite was created together with:

- [Reinout Meliesie](https://github.com/Zedfrigg)

## Licence

The original "JPacman-Framework" was published under the Apache 2.0 license, which can be found in the [Apache-2.0-LICENSE](https://github.com/johanneshagspiel/jpacman-test-suite/tree/master/Apache-2.0-LICENSE.txt) file. For this repository, the terms laid out there shall not apply to any individual that is currently enrolled at a higher education institution as a student. Those individuals shall not interact with any other part of this repository besides this README in any way by, for example cloning it or looking at its source code or have someone else interact with this repository in any way.

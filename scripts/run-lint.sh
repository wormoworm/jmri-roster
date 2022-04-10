#!/bin/bash

runLint () {
    poetry run black --line-length=130 $1
    poetry run pylint --rcfile .pylintrc $1
}

runLint "**.py"
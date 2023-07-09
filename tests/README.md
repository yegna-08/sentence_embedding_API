# Unit Testing
The following guide covers how to run all unit tests

## Running Tests
It is recommended to use [tox](https://github.com/tox-dev/tox) to easily run unit tests for each component in their own virtual
environment.

### Setup
Install tox in your terminal (not inside a VM)
```shell
$ pip install tox
```

### Running The Tests
To run all tests
```shell
$ tox
```
**Note**: The first time running this command might take a while as tox installs the requirements from every component

To pass in extra arguments to pytest
```shell
$ tox -- <args>
```
For example, to get a coverage report
```shell
$ tox -- --cov
```

To view the coverage report on missing lines
```shell
$ pip install coverage
$ coverage html
```
Then open the html files in your browser from htmlcov/ in your root directory

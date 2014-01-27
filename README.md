# failurescreenshots

failurescreenshots is a Nose plugin for users of Webdriver to attempt to capture a browser screenshot whenever a test fails or errors.

To setup: run python setup.py install

To run with nose:
* run nose with --with-failurescreenshots

Currently this requires the driver instance to be named driver

Future work: Specify driver name, specify path and/or folder strategy to save pictures to
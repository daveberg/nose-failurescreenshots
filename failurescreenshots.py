"""Attempt to capture Webdriver screenshots on test error or failure.
Requires an active driver instance named driver within the test
"""
import os

from selenium.common.exceptions import WebDriverException
from nose.plugins.base import Plugin


def get_screen_shot(driver, test_id):
    # don't care about leading 'tests' bit, they're all tests
    # needs revisiting if tests get moved to sub-folders
    name = test_id.split('.', 1)[1]
    # make a folder to keep them in
    path = 'screenshots'
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    # save to it
    try:
        driver.get_screenshot_as_file('{path}/{name}.png'.format(path=path, name=name))
    except WebDriverException as e:
        # possibly browser has died or communication lost but not worth crashing for
        print('Failed to take screenshot: {error}'.format(error=e))


class FailureScreenshots(Plugin):
    """Attempt to capture Webdriver screenshots on test error or failure.
    Requires an active driver instance named driver within the test
    """
    name = 'failurescreenshots'
    score = 2  # run when?
    enabled = True
    enabled_for_errors = True
    enabled_for_failures = True

    def __init__(self):
        super(FailureScreenshots, self).__init__()

    def options(self, parser, env):
        """Register commandline options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            "--ss-errors-only", action="store_true", dest="debugErrors", default=False,
            help="Screenshot errors but not failures")
        parser.add_option(
            "--ss-failures-only", action="store_true", dest="debugFailures", default=False,
            help="Screenshot failures but not errors")

    def configure(self, options, config):
        """Configure which kinds of failures trigger plugin."""
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            if options.debugFailures and options.debugErrors:
                raise ValueError("--errors-only and --failures-only are mutually exclusive")
            self.enabled_for_errors = not options.debugFailures
            self.enabled_for_failures = not options.debugErrors

    def addError(self, test, err):
        """Something."""
        if not self.enabled_for_errors:
            return
        get_screen_shot(test.test.driver, test.id())

    def addFailure(self, test, err):
        """Something."""
        if not self.enabled_for_failures:
            return
        get_screen_shot(test.test.driver, test.id())


"""Attempt to capture Webdriver screenshots on test error or failure.
Requires an active driver instance named driver within the test
"""
import logging
import os

from selenium.common.exceptions import WebDriverException
from nose.plugins.base import Plugin


class FailureScreenshots(Plugin):
    """Attempt to capture Webdriver screenshots on test error or failure.
    Requires an active driver instance named driver within the test
    """
    name = 'failurescreenshots'
    enabled = True
    enabled_for_errors = True
    enabled_for_failures = True
    log = logging.getLogger('nose.plugins.failure_screenshots')

    def __init__(self):
        super(FailureScreenshots, self).__init__()

    def options(self, parser, env):
        """Register commandline options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            "--ss-errors-only", action="store_true", dest="debugErrors",
            default=False, help="Screenshot errors but not failures")
        parser.add_option(
            "--ss-failures-only", action="store_true", dest="debugFailures",
            default=False, help="Screenshot failures but not errors")

    def configure(self, options, config):
        """Configure which kinds of failures trigger plugin."""
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            if options.debugFailures and options.debugErrors:
                raise ValueError("--errors-only and --failures-only are mutually exclusive")
            self.enabled_for_errors = not options.debugFailures
            self.enabled_for_failures = not options.debugErrors

    def get_screen_shot(self, test, test_id):
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
            test.driver.get_screenshot_as_file('{path}/{name}.png'.format(path=path, name=name))
        except AttributeError as e:
            # No WebDriver called driver? Oops.
            self.log.warning('No driver instance found: {error}'.format(error=e))
        except WebDriverException as e:
            # possibly browser died or communication lost, not worth crashing
            self.log.warning('Failed to take screenshot: {error}'.format(error=e))

    def addError(self, test, err):
        """Something."""
        if not self.enabled_for_errors:
            return
        self.get_screen_shot(test.test, test.id())

    def addFailure(self, test, err):
        """Something."""
        if not self.enabled_for_failures:
            return
        self.get_screen_shot(test.test, test.id())

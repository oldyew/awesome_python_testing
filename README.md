# Awesome Python Testing

## Project Setup

### System Prerequisites

To install pipenv, run `pip install pipenv` from the command line.

### Setup Instructions

1. Clone this repository.
2. Run `cd <cloned folder>` to enter the project.
3. Run `pipenv install` to install the dependencies.
4. Run `pipenv run python -m pytest` to verify that the framework can run tests.
5. Create a branch for your code changes. (See *Branching* below.)

### Branching

The `master` branch contains the code for the tutorial's starting point.
The project is basically empty in the `master` branch.

If you want to code along with the tutorial, then create a branch for your work off the `master` branch.
To create your own branch named `tutorial/develop`, run:

    > git checkout master
    > git branch tutorial/develop
    > git checkout tutorial/develop

## Tutorial Instructions

Let's implement this test using pytest.
Create a new file named `test_search.py` under the `tests` directory,
and add the following code:

```python
"""
These tests cover DuckDuckGo searches.
"""

def test_basic_duckduckgo_search():

    # Given the DuckDuckGo home page is displayed
    # TODO

    # When the user searches for "panda"
    # TODO

    # Then the search result title contains "panda"
    # TODO
    
    # And the search result query is "panda"
    # TODO
    
    # And the search result links pertain to "panda"
    # TODO

    raise Exception("Incomplete Test")
```

Adding comments to stub each step may seem trivial,
but it's a good first step when writing new test cases.
We can simply add code at each TODO line as we automate.
Once the test is completed, we will remove the exception at the end.
Also, note that pytest expects all test functions to begin with `test_`.

To avoid confusion when we run tests, let's remove the old placeholder test.
Delete `tests/test_fw.py`.

Rerun the tests using `pipenv run python -m pytest`.
The `test_basic_duckduckgo_search` should be the only test that runs,
and it should fail due to the "Incomplete Test" exception.

Finally, commit your code change. Part 1 is complete!

### Part 2: Defining Page Objects

*Time Estimate: 8 Minutes*

A **page object** is an object representing a Web page or component.
They have *locators* for finding elements,
as well as *interaction methods* that interact with the page under test.
Page objects make low-level Selenium WebDriver calls
so that tests can make short, readable calls instead of complex ones.

Since we have our test steps, we know what pages and elements our test needs.
There are two pages under test, each with a few interactions:

1. The DuckDuckGo search page
   * Load the page
   * Search a phrase
2. The DuckDuckGo results page
   * Get the results
   * Get the search query
   * Get the title

Understanding interactions with the Web app is more important than the code.
We can write stubs for page object classes as we figure out the interactions.

Create a new Python package named `pages`.
To do this create a directory under the root directory named `pages`.
Then, put a blank file in it named `__init__.py`.
The `pages` directory shoult *not* be under the `tests` directory.
Why? When using pytest, the `tests` folder should *not* be a package.

Create a new module named `pages/search.py` and add the following code
for the DuckDuckGo search page:

```python
"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""


class DuckDuckGoSearchPage:

  def load(self):
    # TODO
    pass

  def search(self, phrase):
    # TODO
    pass
```

Create another new module named `pages/result.py` and add the following code
for the DuckDuckGo result page:

```python
"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo search result page.
"""


class DuckDuckGoResultPage:
  
  def result_count_for_phrase(self, phrase):
    # TODO
    return 0
  
  def search_input_value(self):
    # TODO
    return ""

  def title(self):
    # TODO
    return ""
```

Finally, update `test_basic_duckduckgo_search` in `tests/test_search.py`
with the following code:

```python
"""
These tests cover DuckDuckGo searches.
"""

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


def test_basic_duckduckgo_search():
  search_page = DuckDuckGoSearchPage()
  result_page = DuckDuckGoResultPage()
  PHRASE = "panda"
  
  # Given the DuckDuckGo home page is displayed
  search_page.load()

  # When the user searches for "panda"
  search_page.search(PHRASE)

  # Then the search result title contains "panda"
  assert PHRASE in result_page.title()
  
  # And the search result query is "panda"
  assert PHRASE == result_page.search_input_value()
  
  # And the search result links pertain to "panda"
  assert result_page.result_count_for_phrase(PHRASE) > 0

  # TODO: Remove this exception once the test is complete
  raise Exception("Incomplete Test")
```

Notice how we are able to write all the test steps using page object calls and assertions.
We also kept the step comments so the code is well-documented.
Even though we haven't made any Selenium WebDriver calls, our test case function is nearly complete!
Our code is readable and understandable.
It delivers clear testing value.

Rerun the test using `pipenv run python -m pytest`.
The test should fail again, but this time, it should fail on one of the assertions.
Then, commit your latest code changes. Part 2 is now complete!

### Part 3: Setting Up Selenium WebDriver

*Time Estimate: 8 Minutes*

[Selenium WebDriver](https://www.seleniumhq.org/projects/webdriver/)
is a tool for automating Web UI interactions with live browsers.
It works with several popular programming languages and browser types.

The Selenium WebDriver package for Python is named `selenium`.
Run `pipenv install selenium` to install it for our project.

Every test should use its own WebDriver instance.
This keeps things simple and safe.
The best way to set up the WebDriver instance is using a
[pytest fixture](https://docs.pytest.org/en/latest/fixture.html).
Fixtures are basically setup and cleanup functions.
As a best practice, they should be placed in a `conftest.py` module so they can be used by any test.

Create a new file named `tests/conftest.py` and add the following code:

```python
"""
This module contains shared fixtures.
"""

import pytest
import selenium.webdriver


@pytest.fixture
def browser():

  # Initialize the ChromeDriver instance
  b = selenium.webdriver.Chrome()

  # Make its calls wait up to 10 seconds for elements to appear
  b.implicitly_wait(10)

  # Return the WebDriver instance for the setup
  yield b

  # Quit the WebDriver instance for the cleanup
  b.quit()
```

Our fixture uses Chrome as the browser.
Other browser types could be used.
Real-world projects often read browser choice from a config file here.

The implicit wait will make sure WebDriver calls wait for elements to appear before sending calls to them.
10 seconds should be reasonable for our test project's needs.
For larger projects, however, setting explicit waits is a better practice
because different calls need different wait times.
Read more about implicit versus explicit waits [here](https://selenium-python.readthedocs.io/waits.html).

The `yield` statement makes the `browser` fixture a generator.
The first iteration will do the "setup" steps,
while the second iteration will do the "cleanup" steps.
Always make sure to *quit* the WebDriver instance as part of cleanup,
or else zombie processes might lock system resources!

Now, update `test_basic_duckduckgo_search` in `tests/test_search.py` to call the new fixture:

```python
def test_basic_duckduckgo_search(browser):
  search_page = DuckDuckGoSearchPage(browser)
  result_page = DuckDuckGoResultPage(browser)
  # ...
```

Every page object needs a reference to the WebDriver instance.
Update the page object classes to have `__init__` methods.

In `pages/search.py`:

```python
class DuckDuckGoSearchPage:

  def __init__(self, browser):
    self.browser = browser

  # ...
```

And in `pages/result.py`:

```python
class DuckDuckGoResultPage:
  
  def __init__(self, browser):
    self.browser = browser

  # ...
```

Rerun the test using `pipenv run python -m pytest` to test the fixture.
Even though the test should still fail,
Chrome should briefly pop up for a few seconds while the test is running.
Make sure Chrome quits once the test is done.
Then, commit your latest code changes.
Part 3 is now complete!

### Part 4: Making WebDriver Calls

*Time Estimate: 16 Minutes*

Now we can implement all the page object methods using WebDriver calls.
The [WebDriver API for Python](https://selenium-python.readthedocs.io/api.html)
documents all WebDriver calls.
If you aren't sure how to do something, look it up.
WebDriver can do anything a user can do on a Web page!

Let's start with `DuckDuckGoSearchPage`.
The `load` method is a one-line WebDriver call,
but it's good practice to make the URL a class variable:

```python
URL = 'https://www.duckduckgo.com'

def load(self):
  self.browser.get(self.URL)
```

The `search` method is a bit more complex because it interacts with an element.
We need to use a *locator* to find the search input element,
and then we need to *send keys* to type the search phrase into the element.

First, import some key pieces from the `selenium` package:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
```

Then, write a locator for the search input element.
If we inspect the page's HTML, we can see that the search element has a "name" attribute set to "q".
Therefore, we can use the `By.NAME` locator to find the element like this:

```python
SEARCH_INPUT = (By.NAME, 'q')
```

It's good practice to write locators as page object class variables.
That way, the locator can be reused by multiple page object methods.
It is also good to write them as tuples - and we will see why next.

The `search` method needs two parts: finding the element and sending the keystrokes:

```python
def search(self, phrase):
  search_input = self.browser.find_element(*self.SEARCH_INPUT)
  search_input.send_keys(phrase + Keys.RETURN)
```

The `find_element` method will return the first element found by the locator.
Notice how the locator uses the `*` operator to expand the tuple into arguments.
The `selenium` package offers specific locator type methods (like `find_element_by_name`),
but using the generic `find_element` method with argument expansion is better practice.
If the locator type must be changed due to Web page updates,
then the `find_elements` call would not need to be changed.

The `send_keys` call sends the search phrase passed into the `search` method.
This means that the page object can search any phrase!
The addition of `Keys.RETURN` will send the ENTER/RETURN key as well,
which will submit the input value to perform the search and load the results page.

The full code for `pages/search.py` should look like this:

```python
"""
This module contains DuckDuckGoSearchPage,
the page object for the DuckDuckGo search page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class DuckDuckGoSearchPage:

  # URL

  URL = 'https://www.duckduckgo.com'

  # Locators

  SEARCH_INPUT = (By.NAME, 'q')

  # Initializer

  def __init__(self, browser):
    self.browser = browser

  # Interaction Methods

  def load(self):
    self.browser.get(self.URL)

  def search(self, phrase):
    search_input = self.browser.find_element(*self.SEARCH_INPUT)
    search_input.send_keys(phrase + Keys.RETURN)
```

Now, let's do `DuckDuckGoResultPage`.
The `title` method is the easiest one because it just returns a property value:

```python
def title(self):
  return self.browser.title
```

The `search_input_value` method is similar to the `search` method from `DuckDuckGoSearchPage`,
but instead of sending a command, it asks for state from the page.
Thankfully, it uses the same locator.
(The "value" attribute contains the text a user types into an "input" element.)

```python
from selenium.webdriver.common.by import By

SEARCH_INPUT = (By.NAME, 'q')

def search_input_value(self):
  search_input = self.browser.find_element(*self.SEARCH_INPUT)
  return search_input.get_attribute('value')
```

The `result_count_for_phrase` method is the most complex.
The test must verify that the result page displays links relating to the search phrase.
This method should find all result links that contain the search phrase in their display texts.
Then, it should return the count.
The test asserts that the count is greater than zero.
This assertion may seem weak because it could allow some results to be unrelated to the phrase,
but it is good enough for the nature of a basic search test.
(A more rigorous test could and should more carefully cover search result goodness.)

How can we write a locator that finds elements based on text?
We can use XPath:

```python
@classmethod
def PHRASE_RESULTS(cls, phrase):
  xpath = f"//div[@id='links']//*[contains(text(), '{phrase}')]"
  return (By.XPATH, xpath)
```

`PHRASE_RESULT` is a method because the phrase is a parameter for the XPath.
It still returns a tuple so that it can work like other locators.

The `result_count_for_phrase` method uses it like this:

```python
def result_count_for_phrase(self, phrase):
  results = self.browser.find_elements(*self.PHRASE_RESULTS(phrase))
  return len(results)
```

The full code for `pages/result.py` should look like this:

```python
"""
This module contains DuckDuckGoResultPage,
the page object for the DuckDuckGo search result page.
"""

from selenium.webdriver.common.by import By


class DuckDuckGoResultPage:
  
  # Locators

  SEARCH_INPUT = (By.NAME, 'q')

  @classmethod
  def PHRASE_RESULTS(cls, phrase):
    xpath = f"//div[@id='links']//*[contains(text(), '{phrase}')]"
    return (By.XPATH, xpath)

  # Initializer

  def __init__(self, browser):
    self.browser = browser

  # Interaction Methods

  def result_count_for_phrase(self, phrase):
    results = self.browser.find_elements(*self.PHRASE_RESULTS(phrase))
    return len(results)
  
  def search_input_value(self):
    search_input = self.browser.find_element(*self.SEARCH_INPUT)
    return search_input.get_attribute('value')

  def title(self):
    return self.browser.title
```

Finally, remove the "incomplete" exception from `tests/test_search.py`.
That module's code should look like this:

```python
"""
These tests cover DuckDuckGo searches.
"""

from pages.result import DuckDuckGoResultPage
from pages.search import DuckDuckGoSearchPage


def test_basic_duckduckgo_search(browser):
  search_page = DuckDuckGoSearchPage(browser)
  result_page = DuckDuckGoResultPage(browser)
  PHRASE = "panda"

  # Given the DuckDuckGo home page is displayed
  search_page.load()

  # When the user searches for "panda"
  search_page.search(PHRASE)

  # Then the search result title contains "panda"
  assert PHRASE in result_page.title()
  
  # And the search result query is "panda"
  assert PHRASE == result_page.search_input_value()
  
  # And the search result links pertain to "panda"
  assert result_page.result_count_for_phrase(PHRASE) > 0
```

Run the test using `pipenv run python -m pytest`.

## Running Tests

You will need a CrossBrowserTesting license to run the tests in this project.
You can obtain a trial license from https://crossbrowsertesting.com/.
Add your username and authentication key to `cbt_config.json`.

Tond from the project's root directory:

    > pipenv run python -m pytest

## Independent Exercises

The guided tutorial covered one very basic search test, but DuckDuckGo has many more features.
Write some new tests for DuckDuckGo.
Here are some suggestions:

* search for different phrases
* search by clicking the button instead of typing RETURN
* click a search result
* expand "More Results" at the bottom of the result page
* verify auto-complete suggestions pertain to the search text
* search by selecting an auto-complete suggestion
* search a new phrase from the results page
* do an image search
* do a video search
* do a news search
* change settings
* change region

These tests will require new page objects, locators, and interaction methods.
See how many tests you can automate on your own!
If you get stuck, ask for help.

## Additional Resources

* [Web Element Locators for Test Automation](https://automationpanda.com/2019/01/15/web-element-locators-for-test-automation/)
* [Selenium with Python](https://selenium-python.readthedocs.io/)
  * [WebDriver API](https://selenium-python.readthedocs.io/api.html)
  * [Waits](https://selenium-python.readthedocs.io/waits.html)
  * [Locating Elements](https://selenium-python.readthedocs.io/locating-elements.html)
* [pytest.org](https://docs.pytest.org/)
* [Selenium Grid wiki](https://github.com/SeleniumHQ/selenium/wiki/Grid2)
* [CrossBrowserTesting](https://crossbrowsertesting.com/) website

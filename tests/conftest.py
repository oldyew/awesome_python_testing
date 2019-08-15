import pytest
import selenium.webdriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def browser():

  # Initialize the ChromeDriver instance
  b = selenium.webdriver.Chrome(ChromeDriverManager().install())

  # Make its calls wait up to 10 seconds for elements to appear
  b.implicitly_wait(10)

  # Return the WebDriver instance for the setup
  yield b

  # Quit the WebDriver instance for the cleanup
  b.quit()

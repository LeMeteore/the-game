#! No shebang #!
""" Requirements:
* Linux
* nginx in $PATH and
* /etc/hosts contaning a line like:

127.0.0.1 domain-name.tld:port
"""

# no __future__
# no 'public class' either
# By the way, is Python a Object Oriented Programming language ?

import copy
import getpass
import subprocess
import socket
import sys
import textwrap
import time
import functools
import pprint

import pytest

import path
from selenium import webdriver
import requests
import bs4 as beautiful_soup


@pytest.fixture(autouse=True, scope="session")
def free_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

# Personas:
@pytest.fixture
def me():
    class _Inner():
        def __init__(self):
            self.name = getpass.getuser()
            self.hostname = socket.gethostname()
            self.mail = "%s@%s" % (self.name, self.hostname)

    return _Inner()

@pytest.fixture
def mr_nice_guy():
    class _Inner():
        def __init__(self):
            self.name = "Mr. Nice Guy"
            self.hostname = "Awful Corp"
            self.mail = "nice.guy@awful.corp"

    return _Inner()


@pytest.fixture
def tmp_path(tmpdir):
    # py.path sucks, let's use path.py instead
    return path.Path(tmpdir)


@pytest.fixture(autouse=True, scope="session")
def build_and_run(request, free_port):
    subprocess.check_call(["go", "build"])
    process = subprocess.Popen(["./server", str(free_port)])
    yield process
    process.kill()


@pytest.fixture(autouse=True)
def wrapping_fixture(request):
    """" Just so that the output of py.test is nice when used with `-s` """
    title = "{request.module.__name__}::{request.function.__name__}".format(request=request)
    print("\n", title, sep="", flush=True) # Python2 sucks
    print("-" * len(title), flush=True)

    # Before each:
    subprocess.check_call(["git", "clean", "-fd"])
    #  (don't try this at home)
    yield
    # After each
    pass

    print("\n", flush=True) # Yup, that's the TearDown


@pytest.fixture
def browser(free_port, scope="session"):
    class _Inner():
        """ This is a web browser API. In case you need it one day.

        It's also a nice example of the Facade Design Pattern
        """
        def __init__(self, port):
            self._driver = webdriver.Chrome()
            self.port = port

        def _to_full_url(self, path):
            return "http://localhost:%i%s" % (self.port, path)

        def get_css_link(self):
            stylesheet_link = self.html_soup.find("link", rel="stylesheet")
            return stylesheet_link.attrs['href']

        @property
        def html_soup(self):
            return beautiful_soup.BeautifulSoup(self._driver.page_source, "lxml")

        def read(self, path):
            full_url = self._to_full_url(path)
            self._driver.get(full_url)
            return self._driver.page_source

        def click_button(self, button_id):
            button = self._driver.find_element_by_id(button_id)
            button.click()

        def follow_link(self, link_id):
            link = self._driver.find_element_by_id(link_id)
            self._driver.get(link.get_attribute("href"))

        def fill_text(self, id_, text):
            input_ = self._driver.find_element_by_id(id_)
            input_.clear()
            input_.send_keys(text)

        def downlod(self, path):
            full_url = self._to_full_url(path)
            response = requests.get(full_url)
            return response

        def visit(self, url):
            self._driver.get(url)

        def click_link(self, link_text):
            link = self._driver.find_element_by_link_text(link_text)
            link.click()

        def close(self):
            self._driver.close()

    browser = _Inner(free_port)
    yield browser
    browser.close()


def test_zero(browser, me):
    """ Make sure setup and tearn down work properly """
    print("Here's what you should know about me: ")
    pprint.pprint(vars(me)) # Take that, ruby.inspect!


def assert_(a, o, b):
    """ assert on steroids """
    # This is a Framework that actually works.
    if o == "in":
        if not a in b:
            sys.exit(b)
    elif o == "not found in":
        for line in b.splitlines():
            if a in line:
                sys.exit("Got you!\n" + line)
    else:
        raise Exception("Unkwon operator", o)


# Credit goes to one of the Clean Coder videos about TDD for this naming scheme
# Thanks, Uncle Bob!
def test_when_onboarding(browser):
    ...
    "/index.html is not available"
    assert_("resource is not available", "in", browser.read("/index.html"))


# Is this more ore less readable than Cucumber?
def test_when_not_writing_anything(browser):
    ...
    "index still gets written with placeholders values"
    browser.get("/index/edit")
    browser.click_button("save-button")
    browser.follow_link("edit-link")

    index = browser.read("/index.html")

    assert_("Replace", "in", index)
    assert_("Your name", "in", index)


def test_when_filling_all_the_fields(browser, me):
    ... # < Python2 sucks
    "page gets rewritten completely"
    browser.read("/index/edit")
    browser.fill_text("markdown-textarea",
                      textwrap.dedent("""\
# My title

My text

[My first link](http://example.com)"""))

    browser.fill_text("nickname-input", me.name)
    browser.click_button("save-button")

    written_htmtl = browser.read("/index.html")

    html_bits = [
        '<h1>My title</h1>',
        '<p>My text</p>',
        '<a href="http://example.com">My first link</a>',
        '<span class="nickname">{me.name}</span>'.format(me=me)
    ]

    for bits in html_bits:
        assert_(bits, "in", written_htmtl)

    # Check that stylesheet works:
    css = browser.get_css_link()
    assert browser.downlod(css).status_code == 200

    # Nice to have:
    assert_credit_designers(browser)

    # Let's troll a little, it's Friday
    html_lint(written_htmtl)


# I never actually implemented this. Maybe one day.
def test_i_can_upload(browser, tmp_path):
    filename = "foo.png"
    binary_content = b".PNG\0\1\2"
    png_path = tmp_path.joinpath(filename)
    png_path.write_bytes(binary_content)
    browser.get("/upload")
    assert_("Upload", "in", browser.page_source)

    browser.upload_file(png_path)
    browser.click_button("Upload")

    status = browser.downlod("/" + filename)
    assert status == 200


# Below are features I personally care about:

def assert_credit_designers(browser):
    """
    The .css style sheet has a comment stating its origin

    """
    assert_("/* Taken from", "in",  browser.read("/style.css"))


def html_lint(written_html):
    # Just an example, `for name in GAFA` also works :)
    taboos = ["js", "<script>", "javascript"]
    for taboo in taboos:
        assert_(taboo, "not found in", written_html)


# The best for the last:
# Pornography, open-source, privacy, and all that jazz!

@pytest.fixture
def pornhub_server(tmp_path):
    class _Inner():
        def __init__(self, tmp_path):
            self.port = "8080"
            self.path = tmp_path
            self.cfg_path = self.path.joinpath("nginx.cfg")
            self.logs_path = self.path.joinpath("nginx.logs")

        def start(self):
            self.generate_config()
            self.generate_homepage()
            self.start_nginx_process()
            return "http://localhost:8080/"

        def generate_config(self):
            cfg_in = path.Path("nginx.in.cfg").text()
            cfg_out = copy.copy(cfg_in) # Python sucks
            cfg_out = cfg_out.replace("@root_path@", self.path)
            cfg_out = cfg_out.replace("@logs_path@", self.logs_path)
            self.cfg_path.write_text(cfg_out)

        def generate_homepage(self):
            pornhub_html = path.Path("pornhub.html")
            pornhub_html.copy(self.path.joinpath("index.html"))
            pornhub_ico = path.Path("pornhub.ico")
            pornhub_ico.copy(self.path.joinpath("favicon.ico"))

        def _nginx_args(self):
            return ["-p", self.path, "-c", self.cfg_path]

        def start_nginx_process(self):
            cmd = ["nginx"] + self._nginx_args()
            print(*cmd)
            subprocess.check_call(cmd)

        def stop(self):
            cmd = ["nginx"] + self._nginx_args() + ["-s", "stop"]
            subprocess.check_call(cmd)

        @property
        def logs(self):
            return self.logs_path.text()

    res = _Inner(tmp_path)
    yield res
    res.stop()


def test_pornhub_setup(pornhub_server):
    pornhub_server.start()
    print("Using Python requests to talk to porhub")
    response = requests.get("http://localhost:8080/index.html")
    assert response.status_code == 200
    print("Pornhub says:")
    print(response.text)
    print("But here's what it knows:")
    print(pornhub_server.logs)


def test_do_not_track(browser, pornhub_server, mr_nice_guy):
    """
    Make sure that when users follow the link _they_ generated, they can't be
    tracked.

    """
    pornhub_url = pornhub_server.start()
    print("Pornhub running on", pornhub_url, "minding its own buisness ...")


    # Mr. Nice Guy edits a page on the server ...
    browser.read("/mr_nice_guy_home_page/edit")
    shameful_markdown = textwrap.dedent("""\
I really don't want anyone to know ...

[Pr0n]({pornhub_url})""").format(pornhub_url=pornhub_url)

    browser.fill_text("markdown-textarea", shameful_markdown)
    browser.fill_text("nickname-input", mr_nice_guy.name)
    browser.click_button("save-button")


    # Now he visits the same page, but from a public domain name
    public_url = "http://server.tld:{browser.port}/mr_nice_guy_home_page.html"
    public_url = public_url.format(browser=browser)
    browser.visit(public_url)

    # And then he clicks to the pr0n link:
    browser.click_link("Pr0n")

    time.sleep(1)
    pornhub_server.stop()

    # Pornhub knows!
    print(pornhub_server.logs)
    assert_("mr_nice_guy_home_page", "not found in", pornhub_server.logs)

    
# no if __name__ == "__main___" :)

# [1]: Hint: it's almost vim, but not quite

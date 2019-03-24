# Python: Shodan Starcluster

Starcluster automates searching for vulnerable systems within the same postal code. It is written in Python 3 and relies on three, third-party libraries: the Shodan API, GuerrillaMail, and MechanicalSoup.

Shodan is the flare-gun of the script. With an API key & query statement, it searches its remote database of devices directly connected to the Internet. GuerrillaMail generates temporary e-mailboxes that expire after one hour (used to register for a Shodan account). MechanicalSoup is a combination of two other libraries: Mechanize and BeautifulSoup. The former interacts with web pages and submit forms while the latter parses HTML tags.

---

**Copyright**<br>
This project is licensed under the terms of the [MIT license](/LICENSE).

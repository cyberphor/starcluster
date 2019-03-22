# Python: Shodan Starcluster
Automates searching Shodan for vulnerable systems within the same postal code.

---

Check-out the related blog post I wrote to help explain how Starcluster works: <br>
https://www.yoursecurity.tech/python-shodan-starcluster.html

## Outline
* Imported Libraries
	* Built-in Libraries
	* Third-party Libraries
		* GuerrillaMail
		* MechanicalSoup
		* Shodan
* Main Logic
	* Scenario #1: API key & postal code provided
	* Scenario #2: Only API key provided
	* Scenario #3: Only postal code
	* Scenario #4: Nothing is provided
* Primary Functions
	* getShodanAPIkey()
	* findNeighborhood()
	* searchPostalCode()
* Script Header
	* Hashbang
	* Encoding
	* Docstring
	* Dunders

---

**Copyright**<br>
This project is licensed under the terms of the [MIT license](/LICENSE).

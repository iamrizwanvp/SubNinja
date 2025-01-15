# SubNinja  


## About  

SubNinja is a Python-based DNS active brute-force tool designed for efficient subdomain discovery. Built on **ShuffleDNS**, it ensures zero false positives by implementing advanced wildcard DNS filtering. SubNinja supports Discord notifications for real-time updates, making it user-friendly for penetration testers and bug hunters.  


---


## Features  

1. **Chunk-Based Processing**: Handles large wordlists efficiently by processing them in chunks.  

2. **Wildcard DNS Filtering**: Avoids false positives caused by wildcard entries.  

3. **Discord Notifications**: Get notified when chunk processing starts, completes, or encounters errors.  

4. **Customizable**:  

   - Add your own DNS resolvers (`resolvers.txt`).  

   - Use your own wordlists (`wordlist.txt`).  

5. **Manual Results Merging**: After processing, merge results using:  

   ```bash

   cat chunk*_final.txt | sort | uniq > subs.txt


Requirements

	•	ShuffleDNS: Install it from https://github.com/projectdiscovery/shuffledns.

	•	Python 3.x

	•	Install Python dependencies:


pip install -r requirements.txt


Usage

        1.       Clone or download this repository.

	2.	Add your resolvers to resolvers.txt.

	3.	Add your wordlist to wordlist.txt.

	4.	Run the script:


python3 SubNinja.py



	5.	Merge results manually after completion:


cat chunk*_final.txt | sort | uniq > subs.txt

Setup


Before running the script, update the following variables inside the script:

	•	main_domain: Replace with your target domain (e.g., example.com).

	•	wildcard_ip: Set this to the wildcard IP address to avoid false positives.

	•	discord_webhook_url: Add your Discord Webhook URL for notifications.

	•	target_domain: Replace with your target domain (e.g., example.com).


Run the Tool

	1.	Clone or download this repository.

	2.	Add your resolvers to resolvers.txt.

	3.	Add your wordlist to wordlist.txt.

	4.	Run the script:


python3 SubNinja.py



	5.	After completion, merge results manually using:


cat chunk*_final.txt | sort | uniq > subs.txt


File Descriptions

	•	SubNinja.py: The main script for DNS brute-forcing.

	•	filter_wildcard_ip.sh: Bash script for filtering wildcard IPs.

	•	resolvers.txt: A list of DNS resolvers.

	•	wordlist.txt: Wordlist for brute-forcing subdomains.

	•	requirements.txt: Python libraries required to run the tool.


Notes

	•	Ensure your resolvers in resolvers.txt are working to avoid delays.

	•	Results will be saved as chunk*_final.txt for each processed chunk.

	•	Don’t forget to replace the required fields (domain, wildcard IP, etc.) inside the script.

 Enjoy discovering subdomains effortlessly!

# SubNinja
SubNinja is a Python-based DNS Active Bruteforce solution designed for subdomain enumeration made with ShuffleDNS and included advanced wildcard subdomain filtering and optimized for accurate results. It works efficiently on local machines without the need for a VPS and processes large wordlists by splitting them into manageable chunks. SubNinja is designed to:

	•	Reduce false positives: By using wildcard IP filtering to ensure only valid subdomains are included in the results.

	•	Handle duplicates: Automatically avoids duplicates during processing.

	•	Customizable: Supports user-provided resolvers and wordlists for enhanced flexibility.

	•	Chunk-based processing: Works on wordlist chunks, making it scalable even for large domains.

	•	Post-processing simplicity: After completing all operations, you can manually run a simple command to merge and deduplicate results into a single file.


While the tool prioritizes accuracy, note that it may take time to process large datasets. After processing, use the following command to merge results into a single file:


cat results/chunk*_final.txt | sort | uniq > results/subs.txt



# Usage

	1.	Clone the repository:


git clone https://github.com/SubNinja.py.git





	2.	Install requirements:


pip install -r requirements.txt



	3.	Prepare your inputs:

	•	Add resolvers to resolvers.txt.

	•	Add your wordlist to wordlist.txt.

	4.	Run the tool:


python3 SubNinja.py 



	5.	After the script completes, manually merge the final results:


cat chunk*_final.txt | sort | uniq > subs.txt




File Descriptions

	•	SubNinja.py: Main script for DNS brute-forcing.

	•	resolvers.txt: List of resolvers used by ShuffleDNS.

	•	wordlist.txt: Wordlist for DNS enumeration.

	•	filter_wildcard_ip.sh: Bash script for wildcard IP filtering.

	•	requirements.txt: Python library dependencies.


Enjoy discovering subdomains effortlessly!

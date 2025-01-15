# SubNinja
SubNinja is a Python-based DNS Active Bruteforce solution designed for subdomain enumeration and optimized for accurate results. It works efficiently on local machines without the need for a VPS and processes large wordlists by splitting them into manageable chunks. SubNinja is designed to:

	•	Reduce false positives: By using wildcard IP filtering to ensure only valid subdomains are included in the results.

	•	Handle duplicates: Automatically avoids duplicates during processing.

	•	Customizable: Supports user-provided resolvers and wordlists for enhanced flexibility.

	•	Chunk-based processing: Works on wordlist chunks, making it scalable even for large domains.

	•	Post-processing simplicity: After completing all operations, you can manually run a simple command to merge and deduplicate results into a single file.


While the tool prioritizes accuracy, note that it may take time to process large datasets. After processing, use the following command to merge results into a single file:


cat results/chunk*_final.txt | sort | uniq > results/subs.txt

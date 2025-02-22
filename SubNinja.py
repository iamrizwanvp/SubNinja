import os
import re
import subprocess
import requests

# Directories and constants
CHUNKS_DIR = "chunks"
RESULTS_DIR = "results"
MAIN_DOMAIN = "alasco.de"
WILDCARD_IPS = ["141.101.90.107", "141.101.90.104", "141.101.90.105", "141.101.90.106"]
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1326843541078409318/Bl-ku08YLuUdYa9tomkfKtbf1zN_sxpFbCXaIz5hko3S86mbjnS3SfqYywKc56D0SRBY"
LINES_PER_CHUNK = 100000

# Ensure necessary directories exist
os.makedirs(CHUNKS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Function to send notifications to Discord
def send_notification(message):
    try:
        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"[ERROR] Failed to send notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Error sending notification: {e}")

# Function to split the wordlist into chunks
def create_chunks(wordlist):
    print("[INFO] Starting chunk creation...")
    with open(wordlist, "r") as infile:
        lines = infile.readlines()

    chunks = [lines[i:i + LINES_PER_CHUNK] for i in range(0, len(lines), LINES_PER_CHUNK)]
    for i, chunk in enumerate(chunks, 1):
        chunk_file = os.path.join(CHUNKS_DIR, f"chunk{i}.txt")
        with open(chunk_file, "w") as outfile:
            outfile.writelines(chunk)
        print(f"[INFO] Chunk created: {chunk_file}")
    print(f"[INFO] Total chunks created: {len(chunks)}")
    return len(chunks)

# Function to run ShuffleDNS on a chunk
def run_shuffledns(domain, resolvers, chunk_file, output_file):
    print(f"[INFO] Starting ShuffleDNS scan for {chunk_file}...")
    command = [
        "shuffledns",
        "-d", domain,
        "-r", resolvers,
        "-w", chunk_file,
        "-t", "200",
        "-retries", "5",
        "-sw",
        "-wt", "250",
        "-o", output_file,
        "-silent",
        "-mode", "bruteforce"
    ]
    try:
        subprocess.run(command, check=True)
        print(f"[INFO] ShuffleDNS completed for {chunk_file}. Results saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error running ShuffleDNS for {chunk_file}: {e}")

# Function to filter valid subdomains
def filter_subdomains(input_file, output_file, main_domain):
    print(f"[INFO] Starting subdomain filtering for {input_file}...")
    DOMAIN_REGEX = re.compile(r"^(?!\-)([a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,63}$")
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            domain = line.strip()
            if DOMAIN_REGEX.match(domain) and domain.endswith(f".{main_domain}") and domain != main_domain:
                outfile.write(domain + "\n")
    print(f"[INFO] Filtering complete for {input_file}. Results saved to {output_file}.")

# Function to call the bash script for wildcard IP filtering
def filter_wildcard_ip(input_file, output_file, wildcard_ips):
    print(f"[INFO] Starting wildcard IP filtering for {input_file} using bash script...")
    try:
        # Call the bash script with multiple wildcard IPs
        subprocess.run(
            ["bash", "filter_wildcard_ip.sh", input_file, output_file, *wildcard_ips],
            check=True
        )
        print(f"[INFO] Wildcard filtering complete for {input_file}. Results saved to {output_file}.")
        send_notification(f"Final processing complete for {input_file}. Results saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error during wildcard IP filtering: {e}")
        send_notification(f"Error during wildcard IP filtering for {input_file}: {e}")

# Function to merge all final chunk files into a single file and clean up
def finalize_results():
    subs_file = os.path.join(RESULTS_DIR, "subs.txt")
    print(f"[INFO] Merging all valid subdomains into {subs_file}...")

    with open(subs_file, "w") as outfile:
        for filename in sorted(os.listdir(RESULTS_DIR)):
            if filename.endswith("_final.txt"):  
                final_chunk_file = os.path.join(RESULTS_DIR, filename)
                with open(final_chunk_file, "r") as infile:
                    outfile.write(infile.read())

    print(f"[INFO] All final chunk files merged into {subs_file}.")
    send_notification(f"All final chunk files successfully merged into {subs_file}.")

    # Cleanup: Delete unnecessary chunk files
    for filename in os.listdir(RESULTS_DIR):
        if filename.startswith("chunk") or filename.startswith("filtered_chunk"):
            os.remove(os.path.join(RESULTS_DIR, filename))

    print("[INFO] Cleanup complete. Only subs.txt remains.")
# Main workflow
def main(wordlist, resolvers, domain):
    print("[INFO] Script started.")
    send_notification("Script started.")
    try:
        # Step 1: Create chunks
        num_chunks = create_chunks(wordlist)
        print(f"[INFO] {num_chunks} chunks created successfully.")
        send_notification(f"Chunks created: {num_chunks}")

        for i in range(1, num_chunks + 1):
            chunk_file = os.path.join(CHUNKS_DIR, f"chunk{i}.txt")
            result_file = os.path.join(RESULTS_DIR, f"chunk{i}_result.txt")
            filtered_file = os.path.join(RESULTS_DIR, f"filtered_chunk{i}.txt")
            final_file = os.path.join(RESULTS_DIR, f"chunk{i}_final.txt")

            # Step 2: Run ShuffleDNS
            run_shuffledns(domain, resolvers, chunk_file, result_file)

            # Step 3: Filter subdomains
            filter_subdomains(result_file, filtered_file, MAIN_DOMAIN)

            # Step 4: Filter wildcard IPs
            filter_wildcard_ip(filtered_file, final_file, WILDCARD_IPS)

        # Step 5: Merge results & clean up
        finalize_results()

        print("[INFO] All tasks completed successfully.")
        send_notification("All tasks completed successfully.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        send_notification(f"An error occurred: {e}")

# Run the script
if __name__ == "__main__":
    wordlist_path = "/root/mass_recon/subdomains-top1million-110000.txt"
    resolvers_path = "/root/alasco/resolvers.txt"
    target_domain = "alasco.de"

    main(wordlist_path, resolvers_path, target_domain)

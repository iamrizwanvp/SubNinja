
#!/bin/bash

# Parameters
input_file=$1
output_file=$2
wildcard_ip=$3

# Clear or create the output file
> "$output_file"

while read -r subdomain; do
    # Get the IP of the subdomain
    resolved_ip=$(dig +short "$subdomain" | tail -n1)

    # Check if resolved IP is not the wildcard IP
    if [[ "$resolved_ip" != "$wildcard_ip" && -n "$resolved_ip" ]]; then
        echo "$subdomain" >> "$output_file"
    fi
done < "$input_file"

echo "Filtering complete. Results saved in $output_file"

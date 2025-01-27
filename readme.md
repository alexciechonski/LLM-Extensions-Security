
# Crawling Infrastructure Setup and Usage Guide

This README introduces a crawling infrastructure with clear and easy-to-follow instructions.

---

## Prerequisites

- A compatible operating system (Windows, macOS, Linux)
- Google Chrome browser installed
- Access to a terminal/command prompt

## Installation

1. **Download Mitmproxy**

   - Visit the [official Mitmproxy website](https://mitmproxy.org/) and follow the installation guidelines for your operating system.

2. **Install Mitmproxy Certificate**

   - Start Mitmproxy or Mitmweb by running the `mitmweb` command in the terminal.
   - Create a new Chrome profile:
     - Open Chrome.
     - At the top-right, click on the Profile icon (a circle with your account picture) and select Add.
     - In the pop-up window, choose **Continue without an account**.
     - Enter a name.
     - Click **Done**.
     - For more detailed instructions, refer to the [official Chrome help page](https://support.google.com/chrome/answer/2364824?hl=en).
     - Open Chrome and navigate to `chrome://version/`.
     - Take note of the `Executable Path` and `Profile Path`. These paths may be useful for setting up the proxy.

3. **Configure Chrome with Mitmproxy**

   - Open the terminal and navigate to the Chrome executable. For Windows 11, the typical path is:
     ```
     C:\Program Files\Google\Chrome\Application\chrome.exe
     ```
   - Run the following command to start Chrome with the Mitmproxy proxy server:
     ```
     .\chrome.exe --proxy-server="localhost:8080" --user-data-dir="C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Profile<ProfileNumber>"
     ```
     Replace `<YourUsername>` and `<ProfileNumber>` with appropriate values.

4. **Download and Install the Certificate**

   - Visit `mitm.it` in the Chrome instance configured above.
   - Download the Mitmproxy certificate.
   - Install the certificate by:
     - Navigating to Chrome's settings: `Settings → Privacy and Security → Security`.
     - Selecting **Manage Certificates** and importing the downloaded certificate into the **Trusted Root Certification Authorities**.
   - Follow the prompts to complete the installation.

5. **Verify Certificate Installation**

   - Open Chrome and navigate to:
     ```
     Settings → Privacy and Security → Security → Manage Certificates.
     ```
   - Under **Trusted Root Certification Authorities**, confirm the Mitmproxy certificate is listed.

---

## Usage

1. **Start Mitmproxy Web Interface**

   - Run the following command to start Mitmproxy with a flow file to log intercepted traffic:
     ```
     mitmweb.exe -w profile2.flow
     ```

2. **Launch Chrome with Proxy Configuration**

   - In another terminal, execute:
     ```
     .\chrome.exe --proxy-server="localhost:8080" --user-data-dir="C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data\Profile2"
     ```
     - This command creates `Profile2` if it does not already exist. You can replace `Profile2` with your desired profile name or number (e.g., `Profile3`). The "2" is simply provided as an example..
     - Traffic from this Chrome instance will now be routed through Mitmproxy.

3. **Install Generative AI Extension**

   - Install a Generative AI browser extension from the official Chrome Web Store.

4. **Inspect Traffic**

   - Use Mitmproxy’s web interface to monitor and analyze intercepted HTTP/S traffic.

5. **Inspect Flow File** (Optional)

   - To inspect previously saved flows, use the `-r` flag with the flow file:
     ```
     mitmweb.exe -r profile2.flow
     ```

---

## Notes

- The installation and certificate import process may vary slightly depending on your operating system. For detailed instructions, refer to [this blog post](https://scrapfly.io/blog/how-to-install-mitmproxy-certificate/).
- Ensure all applications, including Mitmproxy and Chrome, are closed after your activities to release resources.

---

## Troubleshooting

If you encounter issues:

- Verify the Mitmproxy certificate is correctly installed under **Trusted Root Certification Authorities**.
- Double-check the Chrome executable and profile paths.
- Consult the [Mitmproxy documentation](https://mitmproxy.org/) for further assistance.

---

# Flow File Analyzer
This tool analyzes `.flow` files and extract data into CSV format.

## Features

- Parse `.flow` files and save network data to CSV.
- Extract WebSocket messages into a CSV file.


## Usage

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Analyze Flow Files**:

To analyze `.flow` files and categorize requests:
 - Place your `.flow` files in the directory specified within `parse_flows_to_csvs.py`.
 - Run the script:

      ```bash
      python parse_flows_to_csvs.py
      ```

3. **Extract WebSocket Messages**:

To extract WebSocket messages and save them as a CSV:
 - Update the file path in `websocket_extractor.py` to point to your `.flow` files.
 - Run the script:

      ```bash
      python websocket_extractor.py
      ```

Output files will be saved in the `Output` folder.
 
 ---

## License

This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.
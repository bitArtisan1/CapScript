<p align="center">
 <a href="https://ko-fi.com/D1D11CZNM1">
   <img src="https://github.com/user-attachments/assets/ba118768-9054-416f-b7b2-adaa69a53434" alt="Support me on Ko-fi" width="200" />
 </a>
 </p>
  
  # YouTube Caption Search Tool (CapScript)
  
  ## Overview
  CapScript is a Python console script that utilizes the YouTube Data API and the YouTube Transcript API to search for specific words or phrases within the captions (subtitles) of YouTube videos. The tool allows users to perform targeted searches across individual videos, multiple videos specified through a list, or videos associated with a particular YouTube channel. The matching captions and corresponding timestamps are collected and saved to a text file for easy reference.
  
  <p align="center">
    <img src="https://github.com/user-attachments/assets/23e754c6-915e-4fd7-8c58-e6b93da97b13" alt="Image Description" width=600 height=400>
  </p>
  
  
  ## Features
  - Supports search for words or phrases in YouTube video captions.
  - Three search modes available: Video ID(s), Channel ID, or Video ID(s) from a file.
  - User can specify the number of videos to search for when searching by channel.
  - Allows selection of the language for caption search (default: English - "en").
  - Saves and loads preferences, including the YouTube Data API key.
  - Displays progress during the search and estimated time of completion.
  
  ## Prerequisites
  1. **YouTube Data API Key**: The script requires a valid YouTube Data API key. If you don't have one, you can obtain it by following the [YouTube API Documentation](https://developers.google.com/youtube/registering_an_application).
  2. **Python version >= 3.7**: [Download Python](https://www.python.org/downloads/)
  3. **Python Libraries**: Ensure you have the following Python libraries installed:
     - youtube_transcript_api
     - googleapiclient
     - google-auth-oauthlib
     - configparser
  
     You can install them using `pip`:
  
     ```
     pip install youtube-transcript-api google-api-python-client google-auth-httplib2 google-auth-oauthlib configparser
     ```
  4. **Monospaced Font for Terminal**: To ensure proper display of Unicode characters in the terminal, it's recommended to use a monospaced font. Most modern terminals and command prompts support Unicode characters, but a monospaced font can improve readability. Some common monospaced fonts include "Courier New," "Consolas," "DejaVu Sans Mono," or "Monaco." [Most terminals opt for a (ttf) by default]
  
  ## Usage
  1. **API Key Configuration**: Before running the script, you need to configure the YouTube Data API key. If you have not set it previously or want to change it, the script will prompt you to enter a valid API key.
  2. Download the `CapScript.py` file or use `git clone`:
     ```
     git clone https://github.com/yanpuri/CapScript.git
     ```
  3. Install requirements.txt (if not already installed):
     ```
     pip install -r requirements.txt
     ```
     
  5. Inside the directory of the installation, run the script:
     ```
     python CapScript.py
     ```
  6. **Search Mode Selection**: The script will prompt you to choose a search mode: "Channel" or "Video". 
     - "Channel": You will be asked to enter the YouTube channel ID, the number of videos to search, and the caption language.
     - "Video": You can either enter individual video IDs separated by commas or provide a path to a file containing the video IDs.
  
  7. **Search Term Input**: After selecting the search mode, enter the word or phrase you want to search for within the captions.
  
  8. **Results**: The script will begin the search process and display a progress indicator. After completion, it will show the total number of matches found. The matching captions and corresponding timestamps will be saved in a text file inside the "transcripts" folder.
  
  ## Obtaining a YouTube Data API Key
  To use CapScript, you need a valid YouTube Data API key. Follow the steps below to obtain one:
  
  1. **Create a Google Developer Console Project**: Go to the [Google Developer Console](https://console.cloud.google.com/) and create a new project.
  
  2. **Enable YouTube Data API**: Inside your project, navigate to the "APIs & Services" > "Dashboard" and click on the "+ ENABLE APIS AND SERVICES" button. Search for "YouTube Data API v3" and enable it.
  
  3. **Create Credentials**: In the left-hand menu, click on "Credentials" > "Create Credentials" > "API key". A pop-up will appear, showing your API key.
  
  4. **Restrict API Key (Optional but Recommended)**: To improve security, restrict the API key usage to only the APIs you need. You can set restrictions for the YouTube Data API within the "Credentials" settings.
  
  ## Finding a YouTube Channel ID
  To search for videos associated with a specific YouTube channel, you need a unique Channel ID. Here's how you can find it:
  
  1. **Open YouTube Channel**: Go to the YouTube channel you want to search within your web browser.
  
  2. **View Page Source**: Right-click on the page (anywhere) and select "View Page Source" or "Inspect" from the context menu.
  
  3. **Search for Channel ID**: In the page source view, press `Ctrl+F` (Windows/Linux) or `Cmd+F` (Mac) to open the search function. Enter `?channel_id` in the search box.
  
  4. **Locate the Channel ID**: The search will highlight the "?channel_id" parameter in the page source, and the value next to it will be the Channel ID. It will typically be a string of letters and numbers.
     
  ## Notes
  - The `preferences.ini` file will be created and used to store the API key. This ensures you don't need to re-enter the key each time you run the script.
  - The script will skip videos without available captions or with disabled subtitles.
  - If you run the script multiple times, make sure to use the same API key to avoid API usage issues.
  
  **Important**: The script uses the YouTube Data API, which has request quotas and limitations. Make sure to respect the API usage guidelines to avoid potential restrictions.
  
  ## Images
  ### Channel search:
  ![channel](https://github.com/yanpuri/CapScript/assets/121260820/59ef38af-1cfb-43bd-abe6-b348d3708b18)
  ### Video search (list):
  ![video](https://github.com/yanpuri/CapScript/assets/121260820/5e016164-daca-4388-a8c8-5ff86f436d26)
  ### Output:
  ![god_caption](https://github.com/yanpuri/CapScript/assets/121260820/d96ece6e-949c-4cfd-81d7-5c75e0c2d305)
  
  ## Support Me
  If you find RepoUp useful, consider supporting me by:
  
  - Starring the repository on GitHub
  - Sharing the tool with others
  - Providing feedback and suggestions
  - Follow me for more :)
  
<a href="https://ko-fi.com/D1D11CZNM1">
  <img src="https://github.com/user-attachments/assets/ba118768-9054-416f-b7b2-adaa69a53434" alt="Support me on Ko-fi" width="200" />
</a>
  <center>
      
  ---
  For any issues or feature requests, please open an issue on GitHub. Happy coding!
  
  <div style="text-align: center;">
    <p align="center">
      <img src="https://github.com/user-attachments/assets/36a3e590-bad2-463d-a25e-f56d65c26761" alt="octodance" width="100" height="100" style="margin-right: 10px;"/>
    </p>
  </div>

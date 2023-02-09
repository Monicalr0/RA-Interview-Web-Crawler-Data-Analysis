# RA-Interview-Web-Crawler-Data-Analysis

Use **python {website_name}.py** to run crawler. For detail please checkout the demo video. 

DiLogics RA Interview Tasks
			
Researched Questions: 
The analysis uses data of TOP 100 questions scraped from StackOverflow under tag “ui-automation”, “web automation” and “web-scraping” (100 questions for each tag with answer, description, vote and view, sorted by frequency.

Getting the Data:
Demo video, program and generated data can be found at this REPO: 
https://github.com/Monicalr0/RA-Interview-Web-Crawler-Data-Analysis 

Keywords:
Since the research is focusing on investigating requests that require conditionals (e.g. existence of element, certain value), I tried to use multiple keywords to filter the data and find relevance questions. Selected keywords including: “Specific, condition, conditional, filter, certain value, exist”

Observation:
The filtered question can mainly be classified into three types of questions: 
How to find a specific element or get an inner element after finding a specific element . (e.g. UIAutomation won't retrieve children of an element) 
How to find hidden elements of certain types.(e.g. For example the Slack icon from the notification area: And how can we get a specific icon in case of "show hidden" icons option?) 
In more complex cases, the edge case condition when trying to filter, check existence using certain functions (limited by programming languages, data type) and encounter error. (e.g. I'm trying to locate element by element=driver.find_element_by_partial_link_text("text") in Python selenium and the element does not always exist. Is there a quick line to check if it exists and get NULL or FALSE in place of the error message when it doesn't exist?)

The third type is most observed cases as people usually have done some trials, then they are stuck at certain edge cases when following the tutorial or documentation, then trying to seek help. In this case, people have more specific goals and conditions, they already know the type of website/data they’re dealing with, the function they’re using, the specific data type they want to filter or check existence etc.

Attachments:

Use this link to view the filtered data for Explorative Data Analysis: https://colab.research.google.com/drive/1iZ5fbJ0LeHDOlZ2MtM46UTan_bYImMIH?usp=sharing 

Demo Video: https://drive.google.com/file/d/1D7C5vNenWgArELNe2B-IcmJPNdrmAUsu/view?usp=sharing 

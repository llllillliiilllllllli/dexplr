# LINKEDIN SEARCH ENPOINTS
# Each sid contains three letters including special characters
# Each currentJobId encompasses ten digits unique for each search

URL_SEARCH_ALL = "https://www.linkedin.com/search/results/all/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_PEOPLE = "https://www.linkedin.com/search/results/people/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_JOBS = "https://www.linkedin.com/jobs/search/?keywords={keywords}&currentJobId={currentJobId}"
URL_SEARCH_POSTS = "https://www.linkedin.com/search/results/content/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_COMPANIES = "https://www.linkedin.com/search/results/companies/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_SCHOOLS = "https://www.linkedin.com/search/results/schools/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_GROUPS = "https://www.linkedin.com/search/results/groups/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_EVENTS = "https://www.linkedin.com/search/results/events/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"
URL_SEARCH_COURSES = "https://www.linkedin.com/search/results/learning/?keywords={keywords}&origin=GLOBAL_SEARCH_HEADER&sid={sid}"

# LINKEDIN PROFILE ENDPOINTS
# A profile contains member name and linkedin id 
# The interest endpoint requires four tab clicks

URL_PROFILE = "https://www.linkedin.com/in/{profile}/"
URL_PROFILE_CONTACT_INFO = "https://www.linkedin.com/in/{profile}/overlay/contact-info/"
URL_PROFILE_ACTIVITY = "https://www.linkedin.com/in/{profile}/recent-activity/"
URL_PROFILE_EXPERIENCE = "https://www.linkedin.com/in/{profile}/details/experience/"
URL_PROFILE_EDUCATION = "https://www.linkedin.com/in/{profile}/details/education/"
URL_PROFILE_SKILLS = "https://www.linkedin.com/in/{profile}/details/skills/"
URL_PROFILE_COURSES = "https://www.linkedin.com/in/{profile}/details/courses/"
URL_PROFILE_LANGUAGES = "https://www.linkedin.com/in/{profile}/details/languages/"
URL_PROFILE_INTERESTS = "https://www.linkedin.com/in/{profile}/details/interests/"

# LINKEDIN COMPANY ENPOINTS
# Company is the name of company and currentCompany is its id on LinkedIn 
# Employee field reports essential statistics about employees at the firm

URL_COMPANY_HOME = "https://www.linkedin.com/company/{company}/"
URL_COMPANY_EMPLOYEES = "https://www.linkedin.com/search/results/people/?currentCompany={currentCompany}&origin=COMPANY_PAGE_CANNED_SEARCH&sid={sid}"
URL_COMPANY_ABOUT = "https://www.linkedin.com/company/{company}/about/"
URL_COMPANY_POST = "https://www.linkedin.com/company/{company}/posts/?feedView=all" 
URL_COMPANY_JOBS = "https://www.linkedin.com/company/{company}/jobs/"
URL_COMPANY_PEOPLE = "https://www.linkedin.com/company/{company}/people/"

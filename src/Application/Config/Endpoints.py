# XE ENDPOINTS
# https://www.xe.com/

URL_XE_RATE = "https://www.xe.com/currencyconverter/convert/?Amount=1&From={src}&To={des}"

# GOOGLE PATENT ENDPOINTS
# https://support.google.com/faqs/answer/7049475

# Search by keywords or classifications: "Road Infrastructure System", "A01K1", "G06F3"
# Search by patent publication or application number: US9014905B1, 9014905, US 14/166,502
# Search with metadata retricts: assignee:"Google Inc", inventor:page, before:2001, country:US
# Search for prior art or results from Google Scholar: "Include non-patent literature"
# Searching by chemical names or formulas: atrazine, SSS=atrazine, SMILES, SMARTS, InChIKey 

URL_KEYWORD = "https://patents.google.com/?q={query}"
URL_CLASSIFICATION = "https://patents.google.com/?cpc={cpc}"
URL_PARTENT_NUMBER = "https://patents.google.com/patent/{number}/en"
URL_METADATA_PARAMS = "https://patents.google.com/"\
    +"?q={query}"\
    +"&before={before}"\
    +"&after={after}"\
    +"&inventor={inventor}"\
    +"&assignee={assignee}"\
    +"&country={country}"\
    +"&language={language}"\
    +"&status={status}"\
    +"&type={type}"\
    +"&litigation={litigation}"

from typing import Any, List
from datetime import datetime
import os

import numpy as np
import pandas as pd  
import requests
import dateparser
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup

from Application.Config.Endpoints import EP_XE_RATE
from Application.Config.Paths import PATH_CURRENCY_CODES
from Application.Config.Paths import PATH_CURRENCY_RATES
from Micros.DataValidation import *
from Micros.DataValidation.Validation import is_numeric

class CrunchBase: 

    ### Data Collection

    def config_selectors() -> List[str]:

        ORG_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.sticky-column-2.column-id-identifier.ng-star-inserted > div > field-formatter"
        FOUNDED_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-founded_on.ng-star-inserted > div > field-formatter"
        INDUSTRIES_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-categories.ng-star-inserted > div > field-formatter"
        HQ_LOCATION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-location_identifiers.ng-star-inserted > div > field-formatter"
        DESCRIPTION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-short_description.ng-star-inserted > div > field-formatter"
        CB_RANK_COM_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_org_company.ng-star-inserted > div > field-formatter"
        HQ_REGION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-location_group_identifiers.ng-star-inserted > div > field-formatter"
        DIVERSITY_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-diversity_spotlights.ng-star-inserted > div > field-formatter"
        EST_REVENUE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-revenue_range.ng-star-inserted > div > field-formatter"
        STATUS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-operating_status.ng-star-inserted > div > field-formatter"
        EXIT_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-exited_on.ng-star-inserted > div > field-formatter"
        CLOSING_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-closed_on.ng-star-inserted > div > field-formatter"
        COM_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-company_type.ng-star-inserted > div > field-formatter"
        WEBSITE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-website.ng-star-inserted > div > field-formatter > link-formatter"
        TWITTER_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-twitter.ng-star-inserted > div > field-formatter > link-formatter"
        FACEBOOK_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-facebook.ng-star-inserted > div > field-formatter > link-formatter"
        LINKEDIN_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-linkedin.ng-star-inserted > div > field-formatter > link-formatter"
        EMAIL_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-contact_email.ng-star-inserted > div > field-formatter"
        PHONE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-phone_number.ng-star-inserted > div > field-formatter"
        NUM_ARTICLE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_articles.ng-star-inserted > div > field-formatter"
        HUB_TAGS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-hub_tags.ng-star-inserted > div > field-formatter > enum-multi-formatter"    
        FULL_DESCRIPTION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-description.ng-star-inserted > div > field-formatter"    
        ACTIVE_HIRE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-job_posting_link_source.ng-star-inserted > div > field-formatter"
        INVESTOR_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-investor_type.ng-star-inserted > div > field-formatter"
        INVESTMENT_STAGE = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-investor_stage.ng-star-inserted > div > field-formatter"
        SCHOOL_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-school_type.ng-star-inserted > div > field-formatter"
        SCHOOL_PROGRAM_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-school_program.ng-star-inserted > div > field-formatter"
        NUM_ENROLL_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_enrollments.ng-star-inserted > div > field-formatter"
        SCHOOL_METHOD = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-school_method.ng-star-inserted > div > field-formatter"
        NUM_FOUNDER_ALUM_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_founder_alumni.ng-star-inserted > div > field-formatter"
        INDUSTRY_GROUP_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-category_groups.ng-star-inserted > div > field-formatter"
        NUM_FOUNDER_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_founders.ng-star-inserted > div > field-formatter"
        FOUNDERS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-founder_identifiers.ng-star-inserted > div > field-formatter"
        NUM_EMPLOYEES_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_employees_enum.ng-star-inserted > div > field-formatter"
        NUM_FUNDING_ROUNDS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_funding_rounds.ng-star-inserted > div > field-formatter"
        FUNDING_STATUS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-funding_stage.ng-star-inserted > div > field-formatter"
        LAST_FUNDING_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_funding_at.ng-star-inserted > div > field-formatter"
        LAST_FUNDING_AMOUNT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_funding_total.ng-star-inserted > div > field-formatter"
        LAST_FUNDING_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_funding_type.ng-star-inserted > div > field-formatter"
        LAST_EQUITY_FUNDING_AMOUNT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_equity_funding_total.ng-star-inserted > div > field-formatter"
        LAST_EQUITY_FUNDING_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_equity_funding_type.ng-star-inserted > div > field-formatter"
        TOTAL_EQUITY_FUNDING_AMOUNT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-equity_funding_total.ng-star-inserted > div > field-formatter"
        TOTAL_FUNDING_AMOUNT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-funding_total.ng-star-inserted > div > field-formatter"
        TOP_FIVE_INVESTORS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-investor_identifiers.ng-star-inserted > div > field-formatter"
        NUM_LEAD_INVESTORS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_lead_investors.ng-star-inserted > div > field-formatter"
        NUM_INVESTORS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_investors.ng-star-inserted > div > field-formatter"
        NUM_ACQUISITIONS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_acquisitions.ng-star-inserted > div > field-formatter"
        ACQUISITIONS_STATUS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_status.ng-star-inserted > div > field-formatter"
        TRANSACTION_NAME_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_identifier.ng-star-inserted > div > field-formatter"
        ACQUIRED_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquirer_identifier.ng-star-inserted > div > field-formatter"
        ANNOUNCED_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_announced_on.ng-star-inserted > div > field-formatter"
        PRICE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_price.ng-star-inserted > div > field-formatter"
        ACQUISITION_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_type.ng-star-inserted > div > field-formatter"
        ACQUISITION_TERMS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-acquisition_terms.ng-star-inserted > div > field-formatter"
        IPO_STATUS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipo_status.ng-star-inserted > div > field-formatter"
        IPO_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-went_public_on.ng-star-inserted > div > field-formatter"
        DELISTED_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-delisted_on.ng-star-inserted > div > field-formatter"
        MONEY_RAISED_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipo_amount_raised.ng-star-inserted > div > field-formatter"
        VALUATION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipo_valuation.ng-star-inserted > div > field-formatter"
        STOCK_SYMBOL_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-stock_symbol.ng-star-inserted > div > field-formatter"
        STOCK_EXCHANGE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-stock_exchange_symbol.ng-star-inserted > div > field-formatter"
        LAST_LEADER_HIRE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_key_employee_change_date.ng-star-inserted > div > field-formatter"
        LAST_LAYOFF_MENTION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-last_layoff_date.ng-star-inserted > div > field-formatter"
        NUM_EVENTS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_event_appearances.ng-star-inserted > div > field-formatter"
        CB_RANK_ORG_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_org.ng-star-inserted > div > field-formatter"
        CB_RANK_SCHOOL_CSSSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_org_school.ng-star-inserted > div > field-formatter"
        TREND_SCORE_7D_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_delta_d7.ng-star-inserted > div > field-formatter"
        TREND_SCORE_30D_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_delta_d30.ng-star-inserted > div > field-formatter"
        TREND_SCORE_90D_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-rank_delta_d90.ng-star-inserted > div > field-formatter"
        SIMILAR_COM_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_org_similarities.ng-star-inserted > div > field-formatter"
        JOB_DEPT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-contact_job_departments.ng-star-inserted > div > field-formatter"
        NUM_CONTACTS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_contacts.ng-star-inserted > div > field-formatter"
        MONTHLY_VISITS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visits_latest_month.ng-star-inserted > div > field-formatter"
        AVG_VISITS_6M_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visits_latest_6_months_avg.ng-star-inserted > div > field-formatter"
        MONTHLY_VISITS_GROWTH_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visits_mom_pct.ng-star-inserted > div > field-formatter"
        VISIT_DURATION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visit_duration.ng-star-inserted > div > field-formatter"
        VISIT_DURATION_GROWTH_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visit_duration_mom_pct.ng-star-inserted > div > field-formatter"
        PAGE_VIEW_VISITS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visit_pageviews.ng-star-inserted > div > field-formatter"
        PAGE_VIEW_VISITS_GROWTH_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_visit_pageview_mom_pct.ng-star-inserted > div > field-formatter"
        BOUNCE_RATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_bounce_rate.ng-star-inserted > div > field-formatter"
        BOUNCE_RATE_GROWTH_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_bounce_rate_mom_pct.ng-star-inserted > div > field-formatter"
        GLOBAL_TRAFFIC_RANK_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_global_rank.ng-star-inserted > div > field-formatter"
        MONTHLY_RANK_CHANGE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_global_rank_mom.ng-star-inserted > div > field-formatter"
        MONTHLY_RANK_GROWTH_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-semrush_global_rank_mom_pct.ng-star-inserted > div > field-formatter"
        ACTIVE_TECH_COUNT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-builtwith_num_technologies_used.ng-star-inserted > div > field-formatter"
        NUM_APPS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-apptopia_total_apps.ng-star-inserted > div > field-formatter"
        DOWNLOADS_LAST_30D_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-apptopia_total_downloads.ng-star-inserted > div > field-formatter"
        TOTAL_ACTIVE_PRODUCT_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-siftery_num_products.ng-star-inserted > div > field-formatter"
        PATENTS_GRANTED_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipqwery_num_patent_granted.ng-star-inserted > div > field-formatter"
        TRADEMARKS_REGISTERED_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipqwery_num_trademark_registered.ng-star-inserted > div > field-formatter"
        POPULAR_PATENT_CLASS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipqwery_popular_patent_category.ng-star-inserted > div > field-formatter"
        POPULAR_TRADEMARK_CLASS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-ipqwery_popular_trademark_class.ng-star-inserted > div > field-formatter"
        IT_SPEND_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-aberdeen_site_it_spend.ng-star-inserted > div > field-formatter"
        RECENT_VAL_RANGE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-privco_valuation_range.ng-star-inserted > div > field-formatter"
        RECENT_VAL_DATE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-privco_valuation_timestamp.ng-star-inserted > div > field-formatter"
        NUM_PORFOLIOS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_portfolio_organizations.ng-star-inserted > div > field-formatter"
        NUM_INVESTMENTS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_investments_funding_rounds.ng-star-inserted > div > field-formatter"
        NUM_LEAD_INVESTMENTS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_lead_investments.ng-star-inserted > div > field-formatter"
        NUM_DIVERSITY_INVESTMENTS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_diversity_spotlight_investments.ng-star-inserted > div > field-formatter"
        NUM_EXITS_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_exits.ng-star-inserted > div > field-formatter"
        NUM_EXITS_IPO_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_exits_ipo.ng-star-inserted > div > field-formatter"
        ACC_PROGRAM_TYPE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-program_type.ng-star-inserted > div > field-formatter"
        ACC_APPLICATION_DEADLINE_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-program_application_deadline.ng-star-inserted > div > field-formatter"
        ACC_DURATION_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-program_duration.ng-star-inserted > div > field-formatter"
        NUM_ALUMNI_CSS = "#cdk-drop-list-0 > div > div > grid-body > div > grid-row:nth-child({index}) > grid-cell.column-id-num_alumni.ng-star-inserted > div > field-formatter"

        css_selectors = [
            ORG_CSS, 
            FOUNDED_CSS, 
            INDUSTRIES_CSS, 
            HQ_LOCATION_CSS, 
            DESCRIPTION_CSS, 
            CB_RANK_COM_CSS, 
            HQ_REGION_CSS, 
            DIVERSITY_CSS, 
            EST_REVENUE_CSS, 
            STATUS_CSS, 
            EXIT_DATE_CSS, 
            CLOSING_DATE_CSS, 
            COM_TYPE_CSS, 
            WEBSITE_CSS, 
            TWITTER_CSS, 
            FACEBOOK_CSS, 
            LINKEDIN_CSS, 
            EMAIL_CSS, 
            PHONE_CSS, 
            NUM_ARTICLE_CSS, 
            HUB_TAGS_CSS, 
            FULL_DESCRIPTION_CSS, 
            ACTIVE_HIRE_CSS, 
            INVESTOR_TYPE_CSS, 
            INVESTMENT_STAGE, 
            SCHOOL_TYPE_CSS, 
            SCHOOL_PROGRAM_CSS, 
            NUM_ENROLL_CSS, 
            SCHOOL_METHOD, 
            NUM_FOUNDER_ALUM_CSS, 
            INDUSTRY_GROUP_CSS, 
            NUM_FOUNDER_CSS, 
            FOUNDERS_CSS, 
            NUM_EMPLOYEES_CSS, 
            NUM_FUNDING_ROUNDS_CSS, 
            FUNDING_STATUS_CSS, 
            LAST_FUNDING_DATE_CSS, 
            LAST_FUNDING_AMOUNT_CSS, 
            LAST_FUNDING_TYPE_CSS, 
            LAST_EQUITY_FUNDING_AMOUNT_CSS, 
            LAST_EQUITY_FUNDING_TYPE_CSS, 
            TOTAL_EQUITY_FUNDING_AMOUNT_CSS, 
            TOTAL_FUNDING_AMOUNT_CSS, 
            TOP_FIVE_INVESTORS_CSS, 
            NUM_LEAD_INVESTORS_CSS, 
            NUM_INVESTORS_CSS, 
            NUM_ACQUISITIONS_CSS, 
            ACQUISITIONS_STATUS_CSS, 
            TRANSACTION_NAME_CSS, 
            ACQUIRED_CSS, 
            ANNOUNCED_DATE_CSS, 
            PRICE_CSS, 
            ACQUISITION_TYPE_CSS, 
            ACQUISITION_TERMS_CSS, 
            IPO_STATUS_CSS, 
            IPO_DATE_CSS, 
            DELISTED_DATE_CSS, 
            MONEY_RAISED_CSS, 
            VALUATION_CSS, 
            STOCK_SYMBOL_CSS, 
            STOCK_EXCHANGE_CSS, 
            LAST_LEADER_HIRE_CSS, 
            LAST_LAYOFF_MENTION_CSS, 
            NUM_EVENTS_CSS, 
            CB_RANK_ORG_CSS, 
            CB_RANK_SCHOOL_CSSSS, 
            TREND_SCORE_7D_CSS, 
            TREND_SCORE_30D_CSS, 
            TREND_SCORE_90D_CSS, 
            SIMILAR_COM_CSS, 
            JOB_DEPT_CSS, 
            NUM_CONTACTS_CSS, 
            MONTHLY_VISITS_CSS, 
            AVG_VISITS_6M_CSS, 
            MONTHLY_VISITS_GROWTH_CSS, 
            VISIT_DURATION_CSS, 
            VISIT_DURATION_GROWTH_CSS, 
            PAGE_VIEW_VISITS_CSS, 
            PAGE_VIEW_VISITS_GROWTH_CSS, 
            BOUNCE_RATE_CSS, 
            BOUNCE_RATE_GROWTH_CSS, 
            GLOBAL_TRAFFIC_RANK_CSS, 
            MONTHLY_RANK_CHANGE_CSS, 
            MONTHLY_RANK_GROWTH_CSS, 
            ACTIVE_TECH_COUNT_CSS, 
            NUM_APPS_CSS, 
            DOWNLOADS_LAST_30D_CSS, 
            TOTAL_ACTIVE_PRODUCT_CSS, 
            PATENTS_GRANTED_CSS, 
            TRADEMARKS_REGISTERED_CSS, 
            POPULAR_PATENT_CLASS_CSS, 
            POPULAR_TRADEMARK_CLASS_CSS, 
            IT_SPEND_CSS, 
            RECENT_VAL_RANGE_CSS, 
            RECENT_VAL_DATE_CSS, 
            NUM_PORFOLIOS_CSS, 
            NUM_INVESTMENTS_CSS, 
            NUM_LEAD_INVESTMENTS_CSS, 
            NUM_DIVERSITY_INVESTMENTS_CSS, 
            NUM_EXITS_CSS, 
            NUM_EXITS_IPO_CSS, 
            ACC_PROGRAM_TYPE_CSS, 
            ACC_APPLICATION_DEADLINE_CSS, 
            ACC_DURATION_CSS, 
            NUM_ALUMNI_CSS
        ] 

        return css_selectors

    def config_header() -> str: 
        header = ""
        header = header + "Organization Name,Founded Date,Industries,Headquarters Location,Description,"
        header = header + "CB Rank (Company),Headerquarters Regions,Diversity Spotlight (US Only),"
        header = header + "Estimated Revenue Range,Operating Status,Exit Date,Closed Date,Company Type,"
        header = header + "Website,Twitter,Facebook,LinkedIn,Contact Email,Phone Number,Number of Articles,"
        header = header + "Hub Tags,Full Description,Actively Hiring,Investor Type,Investment Stage,"
        header = header + "School Type, School Program,Number of Enrollments,School Method,"
        header = header + "Number of Founders (Alumni),Industry Groups,Number of Founders,Founders,"
        header = header + "Number of Employees,Number of Funding Rounds,Funding Status,"
        header = header + "Last Funding Date,Last Funding Amount,Last Funding Type,"
        header = header + "Last Equity Funding Amount,Last Equity Funding Type,Total Equity Funding Amount,"
        header = header + "Total Funding Amount,Top Five Investors,Number of Lead Investors,"
        header = header + "Number of Investors,Number of Acquisitions,Acquisition Status,Transaction Name,"
        header = header + "Acquired by,Announced Date,Price,Acquisition Type,Acquisition Terms,"
        header = header + "IPO Status,IPO Date,Delisted Date,Money Raised at IPO,Valuation at IPO,"
        header = header + "Stock Symbol,Stock Exchange,Last Leadership Hiring Date,Last Layoff Mention Date,"
        header = header + "Number of Events,CB Rank (Organization),CB Rank (School),"
        header = header + "Trend Score (7 Days),Trend Score (30 Days),Trend Score (90 Days),Similar Companies,"
        header = header + "Contact Job Departments,Number of Contacts,"
        header = header + "Monthly Visits,Average Visits (6 Months),Monthly Visits Growth,Visit Duration,Visit Duration Growth,"
        header = header + "Page Views / Visit,Page Views / Visit Growth,Bounce Rate,Bounce Rate Growth,"
        header = header + "Global Traffic Rank,Monthly Rank Change (#),Monthly Rank Growth,"
        header = header + "Active Tech Count,Number of Apps,Download Last 30 Days,Total Product Active,"
        header = header + "Patents Granted,Trademarks Registered,Most Popular Patent Class,Most Popular Trademark Class,"
        header = header + "IT Spend,Most Recent Valuation Range,Date of Most Recent Valuation,"
        header = header + "Number of Portfolio Organizations,Number of Investment,Number of Lead Investments,"
        header = header + "Number of Diversity Investments,Number of Exits,Number of Exits (IPO),"
        header = header + "Accelerator Program Type,Accelerator Application Deadline,Accelerator Duration (in Weeks),"
        header = header + "Number of Alumni, Number of Private Contacts, Number of Private Notes,Tags"

        return header

    def extract_datapoints() -> None: 
        print("Enter input file: ", end="")
        i_fil = input().replace("\"", "")

        print("Enter output folder: ", end="")
        o_fol = input().replace("\"", "")

        with open(i_fil, mode="r", encoding="utf-8-sig") as file:
            paths = file.readlines()
            paths = [path.replace("\"", "").strip() for path in paths]

        header = CrunchBase.config_header()
        selectors = CrunchBase.config_selectors()

        for path in paths: 
            dataframe = []
            dataframe.append(header)

            with open(path, mode="r", encoding="utf-8-sig") as file:
                html = file.read()
                soup = BeautifulSoup(html, "lxml")
            
            for i in range(50):      
                dataline = []      
                for selector in selectors:
                    element = soup.select_one(selector.replace("{index}", str(i+2)))

                    if selector.__contains__("id-twitter"):
                        try:
                            href = str(element.contents[0]).split("href=\"")[1].split("\"")[0]
                            dataline.append(href)
                            continue
                        except:
                            dataline.append("—")
                            continue

                    if selector.__contains__("id-facebook"):
                        try:
                            href = str(element.contents[0]).split("href=\"")[1].split("\"")[0]
                            dataline.append(href)
                            continue
                        except:
                            dataline.append("—")
                            continue                  

                    if selector.__contains__("id-linkedin"):
                        try:
                            href = str(element.contents[0]).split("href=\"")[1].split("\"")[0]
                            dataline.append(href)
                            continue
                        except:
                            dataline.append("—")
                            continue
                    
                    dataline.append("\"" + element.text.replace("\"", "\"\"").strip() + "\"")

                print(f"{dataline}", end="\n\n")
                dataframe.append(",".join(dataline))
 
            o_fil = f"{o_fol}\\Dataset @CrunchBaseCompanies #-------------- .csv"
            with open(o_fil, mode="w", encoding="utf-8-sig") as file:
                lines = [dataline + "\n" for dataline in dataframe]
                file.writelines(lines)

            timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
            os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None

    ### Data Preprocessing

    def convert_strings() -> None:
        return NotImplemented

    def convert_numbers() -> None: 
        return NotImplemented

    def convert_datetimes(value: Any) -> None:  
        if type(value) == float:
            if np.isnan(value):
                return np.NaN

        if type(value) == str and value != "—":
            return dateparser.parse(value).strftime("%Y-%m-%d")

    def convert_currencies(value: Any, src: str = None, des: str = "USD") -> float:
        currency_codes_df = pd.read_json(PATH_CURRENCY_CODES)
        currency_rates_df = pd.read_json(PATH_CURRENCY_RATES)

        if src == None:      
            if type(value) == float:                
                if np.isnan(value):
                    return np.NaN  

            if type(value) == str:   
                if "$" in value and "A$" not in value and "CA$" not in value: 
                    src = "USD"
                    value = value.replace("$", "")
                    return float(value)
                if "A$" in value and "CA$" not in value: 
                    src = "AUD"
                    value = value.replace("A$", "") 
                if "CA$" in value: 
                    src = "CAD"
                    value = value.replace("CA$", "") 
                if "€" in value: 
                    src = "EUR"
                    value = value.replace("€", "")
                if "£" in value: 
                    src = "GBP"
                    value = value.replace("£", "")
                if "₹" in value: 
                    src = "INR"
                    value = value.replace("₹", "")
                if "₩" in value: 
                    src = "KRW"
                    value = value.replace("₩", "")
                if "¥" in value and "CN¥" not in value: 
                    src = "JPY"
                    value = value.replace("¥", "")
                if "CN¥" in value: 
                    src = "CNY"
                    value = value.replace("CN¥", "")
                if "SGD" in value: 
                    src = "SGD"
                    value = value.replace("SGD", "")
                if "CHF" in value: 
                    src = "CHF"
                    value = value.replace("CHF", "")
                if "SEK" in value: 
                    src = "SEK"
                    value = value.replace("SEK", "")
                if "ZAR" in value: 
                    src = "ZAR"
                    value = value.replace("ZAR", "")

        for index, symbol in currency_rates_df["From"].iteritems():            
            if src == symbol and des == currency_rates_df["To"].iloc[index]:
                rate = currency_rates_df["Rate"].iloc[index]
                print(f"Exchange rate from {src} to {des}: {rate:.3f}")
                return float(value) * currency_rates_df["Rate"].iloc[index] 

        return np.NaN

    def update_exchange_rates() -> None:
        currency_codes_df = pd.read_json(PATH_CURRENCY_CODES, encoding="utf-8-sig")
        currency_rates_df = pd.DataFrame(columns=["Amount", "From", "To", "Rate"])
        for _, code in currency_codes_df["Code"].iteritems():
            src = code
            des = "USD"

            endpoint = EP_XE_RATE.replace("{src}", src).replace("{des}", des)
            response = requests.get(endpoint)
            soup = BeautifulSoup(response.text, "lxml")
            element = soup.select_one("#__next > div:nth-child(2) > div.fluid-container__BaseFluidContainer-qoidzu-0.gJBOzk > section > div:nth-child(2) > div > main > form > div:nth-child(2) > div:nth-child(1) > p.result__BigRate-sc-1bsijpp-1.iGrAod")
            ex_rate = float(element.text
                .replace(" US Dollars", "")
                .replace(" US Dollar", "").strip())                

            print(f"Exchange rate from {src} to {des}: {ex_rate:.3f}")

            currency_rates_df.loc[len(currency_rates_df.index)] = [1, src, des, ex_rate]

        currency_rates_df.to_json(PATH_CURRENCY_RATES)

        return None 

    def clean_dataset() -> None: 
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Clean companies dataset collected from CrunchBase
        >>> param: None # no param required 
        >>> funct: 0    # read companies data from file
        >>> funct: 1    # clean data, fill and drop NaN values
        >>> funct: 2    # use default pandas conversion functions  
        >>> funct: 3    # apply elementwise function for type conversion
        >>> funct: 4    # apply conversion functions for datetime
        >>> funct: 5    # apply conversion functions for currencies
        >>> funct: 6    # export cleaned data to file with timestamp
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        print("Enter input file: ", end="")
        i_fil = input().replace("\"", "")  

        print("Enter output folder: ", end="")
        o_fol = input().replace("\"", "")  

        try:
            df = pd.read_csv(i_fil)
        except:
            raise Exception("cannot read data from file")

        ### 1        
        df = df.replace(r"—", np.NaN)     
        df = df.convert_dtypes()

        ### 2
        df["Number of Lead Investors"] = pd.to_numeric(df["Number of Lead Investors"])
        df["Number of Investors"] = pd.to_numeric(df["Number of Investors"])
        df["Number of Acquisitions"] = pd.to_numeric(df["Number of Acquisitions"])
        df["Number of Events"] = pd.to_numeric(df["Number of Events"])
        df["Number of Apps"] = pd.to_numeric(df["Number of Apps"])
        df["Number of Alumni"] = pd.to_numeric(df["Number of Alumni"])
        df["Number of Private Contacts"] = pd.to_numeric(df["Number of Private Contacts"])
        df["Number of Private Notes"] = pd.to_numeric(df["Number of Private Notes"])
        df["Active Tech Count"] = pd.to_numeric(df["Active Tech Count"])
        df["Accelerator Duration (in Weeks)"] = pd.to_numeric(df["Accelerator Duration (in Weeks)"])

        ### 3    
        df["Founded Year"] = df["Founded Year"]\
            .apply(CrunchBase.convert_datetimes)
        df["Founded Year"] = df["Founded Year"]\
            .apply(lambda x: f"{x}"[:4] if type(x) == str else np.NaN)

        df["CB Rank (Company)"] = df["CB Rank (Company)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["CB Rank (Organization)"] = df["CB Rank (Organization)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["CB Rank (School)"] = df["CB Rank (School)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        
        df["Similar Companies"] = df["Similar Companies"]\
            .apply(lambda x: int(x) if type(x) == str else np.NaN)
        df["Number of Articles"] = df["Number of Articles"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Number of Funding Rounds"] =  df["Number of Funding Rounds"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Number of Employees"] = df["Number of Employees"]\
            .apply(lambda x: x.replace("+", "-inf").split("-") if type(x)==str else np.NaN)
        df["Number of Contacts"] = df["Number of Contacts"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)

        df["Trend Score (7 Days)"] = df["Trend Score (7 Days)"]\
            .apply(lambda x: float(x) if type(x) == str else np.NaN)
        df["Trend Score (30 Days)"] = df["Trend Score (30 Days)"]\
            .apply(lambda x: float(x) if type(x) == str else np.NaN)
        df["Trend Score (90 Days)"] = df["Trend Score (90 Days)"]\
            .apply(lambda x: float(x) if type(x) == str else np.NaN)

        df["Monthly Visits"] = df["Monthly Visits"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Average Visits (6 Months)"] = df["Average Visits (6 Months)"]\
            .apply(lambda x: float(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Monthly Visits Growth"] = df["Monthly Visits Growth"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)
        df["Visit Duration"] = df["Visit Duration"]\
            .apply(lambda x: int(x.replace(r",", r""))/100 if type(x) == str else np.NaN)
        df["Visit Duration Growth"] = df["Visit Duration Growth"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)
        df["Page Views / Visit"] = df["Page Views / Visit"]\
            .apply(lambda x: float(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Page Views / Visit Growth"] = df["Page Views / Visit Growth"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)
        df["Bounce Rate"] = df["Bounce Rate"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)
        df["Bounce Rate Growth"] = df["Bounce Rate Growth"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)

        df["Global Traffic Rank"] = df["Global Traffic Rank"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Monthly Rank Change (#)"] = df["Monthly Rank Change (#)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN)
        df["Monthly Rank Growth"] = df["Monthly Rank Growth"]\
            .apply(lambda x: float(x.replace(r",", r"").replace(r"%", r""))/100 if type(x) == str else np.NaN)

        df["Download Last 30 Days"] = df["Download Last 30 Days"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Total Product Active"] = df["Total Product Active"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Patents Granted"] = df["Patents Granted"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Trademarks Registered"] = df["Trademarks Registered"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 

        df["Number of Portfolio Organizations"] = df["Number of Portfolio Organizations"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Number of Investments"] = df["Number of Investments"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Number of Lead Investments"] = df["Number of Lead Investments"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Number of Diversity Investments"] = df["Number of Diversity Investments"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Number of Exits"] = df["Number of Exits (IPO)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 
        df["Number of Exits"] = df["Number of Exits (IPO)"]\
            .apply(lambda x: int(x.replace(r",", r"")) if type(x) == str else np.NaN) 

        ### 4
        df["Exit Date"] = df["Exit Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Closed Date"] = df["Closed Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Last Funding Date"] = df["Last Funding Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Announced Date"] = df["Announced Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["IPO Date"] = df["IPO Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(CrunchBase.convert_datetimes)

        df["Announced Date"] = df["Announced Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["IPO Date"] = df["IPO Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Delisted Date"] = df["Delisted Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Last Leadership Hiring Date"] = df["Last Leadership Hiring Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Last Layoff Mention Date"] = df["Last Layoff Mention Date"]\
            .apply(CrunchBase.convert_datetimes)

        df["Date of Most Recent Valuation"] = df["Date of Most Recent Valuation"]\
            .apply(CrunchBase.convert_datetimes)

        df["Accelerator Application Deadline"] = df["Accelerator Application Deadline"]\
            .apply(CrunchBase.convert_datetimes)

        ### 5
        df["Last Funding Amount"] = df["Last Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Last Funding Amount"] = df["Last Funding Amount"]\
            .apply(CrunchBase.convert_currencies)
        
        df["Last Equity Funding Amount"] = df["Last Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Last Equity Funding Amount"] = df["Last Equity Funding Amount"]\
            .apply(CrunchBase.convert_currencies)
        
        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Total Equity Funding Amount"] = df["Total Equity Funding Amount"]\
            .apply(CrunchBase.convert_currencies)
        
        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Total Funding Amount"] = df["Total Funding Amount"]\
            .apply(CrunchBase.convert_currencies)

        df["Price"] = df["Price"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Price"] = df["Price"]\
            .apply(CrunchBase.convert_currencies)

        df["Money Raised at IPO"] = df["Money Raised at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Money Raised at IPO"] = df["Money Raised at IPO"]\
            .apply(CrunchBase.convert_currencies)

        df["Valuation at IPO"] = df["Valuation at IPO"]\
            .apply(lambda x: x.replace(",", "").strip() if type(x)==str else np.NaN)
        df["Valuation at IPO"] = df["Valuation at IPO"]\
            .apply(CrunchBase.convert_currencies)      

        df["Estimated Revenue Range"] = df["Estimated Revenue Range"]\
            .apply(lambda x: x.replace("$", "").replace("M", 6*"0").replace("B", 9*"0").strip() if type(x)==str else np.NaN)
        df["Estimated Revenue Range"] = df["Estimated Revenue Range"]\
            .apply(lambda x: x.replace("+", " to inf") if type(x)==str else np.NaN)
        df["Estimated Revenue Range"] = df["Estimated Revenue Range"]\
            .apply(lambda x: x.split(" to ") if type(x)==str else np.NaN)

        ### 6
        o_fil = f"{o_fol}\\Dataset @1000CrunchBaseCompanies #-------------- .csv"
        df.to_csv(o_fil, index=False, encoding="utf-8-sig")

        timestamp = datetime.fromtimestamp(os.path.getctime(o_fil)).strftime("%Y%m%d%H%M%S")      
        os.rename(o_fil, o_fil.replace("#--------------", f"#{timestamp}"))

        return None

    def join_datasets():
        print("Enter input file: ", end="")
        i_fil = input().replace("\"", "")

        print("Enter output file: ", end="")
        o_fil = input().replace("\"", "")

        with open(i_fil, mode="r", encoding="utf-8-sig") as file:
            paths = file.readlines()
            paths = [path.replace("\"", "").strip() for path in paths]

        dataframe = []
        dataframe.append(CrunchBase.header)
        for path in paths: 
            with open(path, mode="r", encoding="utf-8-sig") as file:
                datalines = file.readlines()
                for dataline in datalines:
                    dataframe.append(dataline)
            
        with open(o_fil, mode="w", encoding="utf-8-sig") as file:
            file.writelines(dataframe)

    ### Data Analytics

    def describe_numeric_data() -> None:
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Describe companies dataset collected from CrunchBase
        >>> param: None # no param required 
        >>> funct: 0    # read data from comma-delimited file
        >>> funct: 1    # convert data into the right types
        >>> funct: 2    # show general information about dataset
        >>> funct: 3    # show detailed data records in dataset
        >>> funct: 4    # describe key stats of numeric fields
        >>> funct: 5    # visualize univariate data with histograms
        >>> funct: 6    # visualize multivariate data with scatterplots
        >>> funct: 7    # include correlation analysis for relevant pairs
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        ### 0
        print("Enter input file: ", end="")
        i_fil = input().replace("\"", "")  

        try:
            df = pd.read_csv(i_fil)
        except:
            raise Exception("cannot read data from file")  

        ### 1
        df = df.convert_dtypes()

        ### 2
        print("\nGENERAL INFORMATION: Top 1000 Most Innovative Companies on CrunchBase")
        print("=" * os.get_terminal_size().columns)
        
        df.info(verbose=True)
        print(end="\n\n")

        ### 3
        print("\nDETAILED TABLE: Top 1000 Most Innovative Companies on CrunchBase")
        print("=" * os.get_terminal_size().columns)
        print(df, end="\n\n")

        ### 4
        selection = input("Show histograms [Y/N]: ")
        print(end="\n\n")

        print("\nDESCRIPTIVE STATS: Top 1000 Most Innovative Companies on CrunchBase")
        print("=" * os.get_terminal_size().columns)
        pd.set_option("display.precision", 3)

        for label, series in df.iteritems():
            if label in ["Monthly Visits", "Average Visits (6 Months)"]:
                continue 

            if series.count() != 0 and is_numeric(series) == True: 
                stats = series.describe()
                skew = series.skew()
                kurt = series.kurtosis()
                stats = pd.concat([stats, pd.Series(data={"skewness": skew, "kurtosis": kurt})])

                print(f"{label}:\n{stats}", end="\n\n")  
        ### 5
                if selection == "Y":
                    IQR = stats["75%"] - stats["25%"]
                    if IQR == 0: continue
                    diff_range = stats["max"] - stats["min"]
                    bin_width = 2 * IQR / pow(series.count(), 1/3) 
                    num_bins = int(diff_range / bin_width)
                    series.hist(bins=num_bins) 
                    plt.title(label)
                    plt.show()
        
        ### 6
        selection = input("Show scatter plots [Y/N]: ")
        print(end="\n")

        if selection == "Y":
            labels = input("Enter data labels: ")
            labels = [label.strip() for label in labels.split(",")]

            collection = pd.DataFrame()
            for label in labels:
                collection = pd.concat([collection, df[label]], axis=1) 

            try:    
                pd.plotting.scatter_matrix(collection)
                plt.show()     
            except:
                print(f"ERROR: Cannot plot scatter matrix for {', '.join(labels)}")     

        return None 

    def describe_categorical_data() -> None:
        # text analysis
        # . Text Classification
        # . Text Extraction
        # . Word Frequency
        # . Collocation
        # . Concordance
        # . Word Sense Disambiguation
        # . Clustering
        #
        # natural language processing 
        # . 
        # . 
        # . 
        # . 
        # . 
        # . 
        # . 
        # E.g. best brand names are mesmerizing because 
        # they are short, concise, easy to memorize and pronounce

        pass 

    def infer_field_1_based_on_features_1_2_3_using_technique_A() -> None:
        
        # Question 1: How did a startup succeed?  

        # for analyzing numeric data fields
        # for analyzing categorical data

        # extract a subset containing crutial metrics:
        # for marketing, finance, team, ...
        # including ranks, revenues, fundings, founders, investors, investments
        # price, valuation, money raised, 
        # digital marketing stats: trend scores, visits, traffic, 
        # tech stats: number of tech, products, patents, trademarks, IT spends
        
        # define key success factors: 
        # attractiveness by the amount of investment
        # profitability by the total return or 
        # potential by return from investments
        # ...  


        # Question 2: Will a startup succeed?  

        # find the model that best present the features
        # use the model to predict the change of success
        # ...


        # Question 3: How did a startup fail?

        # Reverse the conditions as mentioned above

        pass 

    def infer_field_2_based_on_features_a_b_c_using_technique_B() -> None:
        pass 

    def infer_field_3_based_on_features_x_y_z_using_technique_C() -> None:
        pass 

    # ...

    # the project supports decisions on techs, startups, and invesments
    # by providing insights about which factors contribute to fruitful companies
    # to learn from the past about what make novel ideas become influential 
    # to determine new ventures that are most probable to succeed 

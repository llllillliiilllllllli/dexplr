from datetime import datetime
from bs4 import BeautifulSoup
import os 

class CrunchBase: 

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
    header = header + "Number of Alumni"

    def extract() -> None: 
        print("Enter input file: ", end="")
        i_fil = input().replace("\"", "")

        print("Enter output folder: ", end="")
        o_fol = input().replace("\"", "")

        with open(i_fil, mode="r", encoding="utf-8-sig") as file:
            paths = file.readlines()
            paths = [path.replace("\"", "").strip() for path in paths]

        for path in paths: 
            dataframe = []
            dataframe.append(CrunchBase.header)

            with open(path, mode="r", encoding="utf-8-sig") as file:
                html = file.read()
                soup = BeautifulSoup(html, "lxml")
            
            for i in range(50):      
                dataline = []      
                for selector in CrunchBase.css_selectors:
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
 
            filename = f"{o_fol}\\Dataset @CrunchBaseCompanies #-------------- .csv"
            with open(filename, mode="w", encoding="utf-8-sig") as file:
                lines = [dataline + "\n" for dataline in dataframe]
                file.writelines(lines)

            timestamp = datetime.fromtimestamp(os.path.getctime(filename)).strftime("%Y%m%d%H%M%S")      
            os.rename(filename, filename.replace("#--------------", timestamp))

    def join_dataset():
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

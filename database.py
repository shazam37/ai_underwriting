from sqlalchemy import create_engine, Column, String, Date, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Database setup

database_url = os.environ.get('DATABASE_URL')

# SQLALCHEMY_DATABASE_URL = "sqlite:///./documents.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
class DrivingLicense(Base):
    __tablename__ = "driving_licenses"
    
    id = Column(String, primary_key=True, index=True)
    license_number = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    address = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    sex = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class SSNRecord(Base):
    __tablename__ = "ssn_records"
    
    id = Column(String, primary_key=True, index=True)
    ssn = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Bureau(Base):
    __tablename__ = "bureau"
    
    id = Column(String, primary_key=True, index=True)
    ssn = Column(String, unique=True, index=True)  # Foreign key to SSN
    dti = Column(String)
    delinq_2yrs = Column(Integer)
    earliest_cr_line = Column(String)
    fico_range_low = Column(Integer)
    fico_range_high = Column(Integer)
    inq_last_6mths = Column(Integer)
    mths_since_last_delinq = Column(Integer)
    mths_since_last_record = Column(Integer)
    open_acc = Column(Integer)
    pub_rec = Column(Integer)
    revol_bal = Column(String)
    revol_util = Column(String)
    total_acc = Column(Integer)
    initial_list_status = Column(String)
    out_prncp = Column(String)
    out_prncp_inv = Column(String)
    total_pymnt = Column(String)
    total_pymnt_inv = Column(String)
    total_rec_prncp = Column(String)
    total_rec_int = Column(String)
    total_rec_late_fee = Column(String)
    recoveries = Column(String)
    collection_recovery_fee = Column(String)
    last_pymnt_d = Column(String)
    last_pymnt_amnt = Column(String)
    next_pymnt_d = Column(String)
    last_credit_pull_d = Column(String)
    last_fico_range_high = Column(Integer)
    last_fico_range_low = Column(Integer)
    collections_12_mths_ex_med = Column(Integer)
    mths_since_last_major_derog = Column(Integer)
    policy_code = Column(String)
    application_type = Column(String)
    annual_inc_joint = Column(String)
    dti_joint = Column(String)
    verification_status_joint = Column(String)
    acc_now_delinq = Column(Integer)
    tot_coll_amt = Column(String)
    tot_cur_bal = Column(String)
    open_acc_6m = Column(Integer)
    open_act_il = Column(Integer)
    open_il_12m = Column(Integer)
    open_il_24m = Column(Integer)
    mths_since_rcnt_il = Column(Integer)
    total_bal_il = Column(String)
    il_util = Column(String)
    open_rv_12m = Column(Integer)
    open_rv_24m = Column(Integer)
    max_bal_bc = Column(String)
    all_util = Column(String)
    total_rev_hi_lim = Column(String)
    inq_fi = Column(Integer)
    total_cu_tl = Column(Integer)
    inq_last_12m = Column(Integer)
    acc_open_past_24mths = Column(Integer)
    avg_cur_bal = Column(String)
    bc_open_to_buy = Column(String)
    bc_util = Column(String)
    chargeoff_within_12_mths = Column(Integer)
    delinq_amnt = Column(String)
    mo_sin_old_il_acct = Column(Integer)
    mo_sin_old_rev_tl_op = Column(Integer)
    mo_sin_rcnt_rev_tl_op = Column(Integer)
    mo_sin_rcnt_tl = Column(Integer)
    mort_acc = Column(Integer)
    mths_since_recent_bc = Column(Integer)
    mths_since_recent_bc_dlq = Column(Integer)
    mths_since_recent_inq = Column(Integer)
    mths_since_recent_revol_delinq = Column(Integer)
    num_accts_ever_120_pd = Column(Integer)
    num_actv_bc_tl = Column(Integer)
    num_actv_rev_tl = Column(Integer)
    num_bc_sats = Column(Integer)
    num_bc_tl = Column(Integer)
    num_il_tl = Column(Integer)
    num_op_rev_tl = Column(Integer)
    num_rev_accts = Column(Integer)
    num_rev_tl_bal_gt_0 = Column(Integer)
    num_sats = Column(Integer)
    num_tl_120dpd_2m = Column(Integer)
    num_tl_30dpd = Column(Integer)
    num_tl_90g_dpd_24m = Column(Integer)
    num_tl_op_past_12m = Column(Integer)
    pct_tl_nvr_dlq = Column(String)
    percent_bc_gt_75 = Column(String)
    pub_rec_bankruptcies = Column(Integer)
    tax_liens = Column(Integer)
    tot_hi_cred_lim = Column(String)
    total_bal_ex_mort = Column(String)
    total_bc_limit = Column(String)
    total_il_high_credit_limit = Column(String)
    revol_bal_joint = Column(String)
    sec_app_fico_range_low = Column(Integer)
    sec_app_fico_range_high = Column(Integer)
    sec_app_earliest_cr_line = Column(String)
    sec_app_inq_last_6mths = Column(Integer)
    sec_app_mort_acc = Column(Integer)
    sec_app_open_acc = Column(Integer)
    sec_app_revol_util = Column(String)
    sec_app_open_act_il = Column(Integer)
    sec_app_num_rev_accts = Column(Integer)
    sec_app_chargeoff_within_12_mths = Column(Integer)
    sec_app_collections_12_mths_ex_med = Column(Integer)
    hardship_flag = Column(String)
    hardship_type = Column(String)
    hardship_reason = Column(String)
    hardship_status = Column(String)
    deferral_term = Column(Integer)
    hardship_amount = Column(String)
    hardship_start_date = Column(String)
    hardship_end_date = Column(String)
    payment_plan_start_date = Column(String)
    hardship_length = Column(Integer)
    hardship_dpd = Column(Integer)
    hardship_loan_status = Column(String)
    orig_projected_additional_accrued_interest = Column(String)
    hardship_payoff_balance_amount = Column(String)
    hardship_last_payment_amount = Column(String)
    debt_settlement_flag = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class KYC(Base):
    __tablename__ = "kyc"
    
    id = Column(String, primary_key=True, index=True)
    ssn = Column(String, unique=True, index=True)
    zip_code = Column(String)
    addr_state = Column(String)

class DocumentUploadSave(Base):
    __tablename__ = "document_upload"

    id = Column(String, primary_key=True, index=True)
    document_type = Column(String)
    extracted_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ApplicationUploadSave(Base):
    __tablename__ = "application_upload"

    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    application_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class UnderstatementResult(Base):
    __tablename__ = "understatement_result"

    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

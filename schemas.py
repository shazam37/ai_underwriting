from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class ApplicationDocumentType(str, Enum):
    DRIVING_LICENSE = "driving_license"
    SSN = "ssn"

class StatementDocumentType(str, Enum):
    BANK_APPLICATION = "bank_application"
    BANK_STATEMENT = "bank_statement"

# Pydantic models for responses
class DrivingLicenseResponse(BaseModel):
    id: str
    license_number: str
    first_name: str
    last_name: str
    date_of_birth: date
    address: str
    issue_date: date
    expiration_date: date
    sex: str
    created_at: datetime

class SSNResponse(BaseModel):
    id: str
    ssn: str
    first_name: str
    last_name: str
    address: str
    created_at: datetime

class DocumentUploadMessage(BaseModel):
    success: bool
    message: str
    document_type: str
    extracted_number: str
    file_path: str

class ApplicationUploadMessage(BaseModel):
    success: bool
    message: str
    application_type: str
    content: str
    file_path: str

class BureauResponse(BaseModel):
    id: str
    ssn: str
    dti: Optional[str]
    delinq_2yrs: Optional[int]
    earliest_cr_line: Optional[str]
    fico_range_low: Optional[int]
    fico_range_high: Optional[int]
    inq_last_6mths: Optional[int]
    mths_since_last_delinq: Optional[int]
    mths_since_last_record: Optional[int]
    open_acc: Optional[int]
    pub_rec: Optional[int]
    revol_bal: Optional[str]
    revol_util: Optional[str]
    total_acc: Optional[int]
    initial_list_status: Optional[str]
    out_prncp: Optional[str]
    out_prncp_inv: Optional[str]
    total_pymnt: Optional[str]
    total_pymnt_inv: Optional[str]
    total_rec_prncp: Optional[str]
    total_rec_int: Optional[str]
    total_rec_late_fee: Optional[str]
    recoveries: Optional[str]
    collection_recovery_fee: Optional[str]
    last_pymnt_d: Optional[str]
    last_pymnt_amnt: Optional[str]
    next_pymnt_d: Optional[str]
    last_credit_pull_d: Optional[str]
    last_fico_range_high: Optional[int]
    last_fico_range_low: Optional[int]
    collections_12_mths_ex_med: Optional[int]
    mths_since_last_major_derog: Optional[int]
    policy_code: Optional[str]
    application_type: Optional[str]
    annual_inc_joint: Optional[str]
    dti_joint: Optional[str]
    verification_status_joint: Optional[str]
    acc_now_delinq: Optional[int]
    tot_coll_amt: Optional[str]
    tot_cur_bal: Optional[str]
    open_acc_6m: Optional[int]
    open_act_il: Optional[int]
    open_il_12m: Optional[int]
    open_il_24m: Optional[int]
    mths_since_rcnt_il: Optional[int]
    total_bal_il: Optional[str]
    il_util: Optional[str]
    open_rv_12m: Optional[int]
    open_rv_24m: Optional[int]
    max_bal_bc: Optional[str]
    all_util: Optional[str]
    total_rev_hi_lim: Optional[str]
    inq_fi: Optional[int]
    total_cu_tl: Optional[int]
    inq_last_12m: Optional[int]
    acc_open_past_24mths: Optional[int]
    avg_cur_bal: Optional[str]
    bc_open_to_buy: Optional[str]
    bc_util: Optional[str]
    chargeoff_within_12_mths: Optional[int]
    delinq_amnt: Optional[str]
    mo_sin_old_il_acct: Optional[int]
    mo_sin_old_rev_tl_op: Optional[int]
    mo_sin_rcnt_rev_tl_op: Optional[int]
    mo_sin_rcnt_tl: Optional[int]
    mort_acc: Optional[int]
    mths_since_recent_bc: Optional[int]
    mths_since_recent_bc_dlq: Optional[int]
    mths_since_recent_inq: Optional[int]
    mths_since_recent_revol_delinq: Optional[int]
    num_accts_ever_120_pd: Optional[int]
    num_actv_bc_tl: Optional[int]
    num_actv_rev_tl: Optional[int]
    num_bc_sats: Optional[int]
    num_bc_tl: Optional[int]
    num_il_tl: Optional[int]
    num_op_rev_tl: Optional[int]
    num_rev_accts: Optional[int]
    num_rev_tl_bal_gt_0: Optional[int]
    num_sats: Optional[int]
    num_tl_120dpd_2m: Optional[int]
    num_tl_30dpd: Optional[int]
    num_tl_90g_dpd_24m: Optional[int]
    num_tl_op_past_12m: Optional[int]
    pct_tl_nvr_dlq: Optional[str]
    percent_bc_gt_75: Optional[str]
    pub_rec_bankruptcies: Optional[int]
    tax_liens: Optional[int]
    tot_hi_cred_lim: Optional[str]
    total_bal_ex_mort: Optional[str]
    total_bc_limit: Optional[str]
    total_il_high_credit_limit: Optional[str]
    revol_bal_joint: Optional[str]
    sec_app_fico_range_low: Optional[int]
    sec_app_fico_range_high: Optional[int]
    sec_app_earliest_cr_line: Optional[str]
    sec_app_inq_last_6mths: Optional[int]
    sec_app_mort_acc: Optional[int]
    sec_app_open_acc: Optional[int]
    sec_app_revol_util: Optional[str]
    sec_app_open_act_il: Optional[int]
    sec_app_num_rev_accts: Optional[int]
    sec_app_chargeoff_within_12_mths: Optional[int]
    sec_app_collections_12_mths_ex_med: Optional[int]
    hardship_flag: Optional[str]
    hardship_type: Optional[str]
    hardship_reason: Optional[str]
    hardship_status: Optional[str]
    deferral_term: Optional[int]
    hardship_amount: Optional[str]
    hardship_start_date: Optional[str]
    hardship_end_date: Optional[str]
    payment_plan_start_date: Optional[str]
    hardship_length: Optional[int]
    hardship_dpd: Optional[int]
    hardship_loan_status: Optional[str]
    orig_projected_additional_accrued_interest: Optional[str]
    hardship_payoff_balance_amount: Optional[str]
    hardship_last_payment_amount: Optional[str]
    debt_settlement_flag: Optional[str]
    created_at: datetime

class KYCResponse(BaseModel):
    id: str
    ssn: str
    zip_code: str
    addr_state: str

class DocumentUploadResponse(BaseModel):
    id: Optional[str] = None
    document_type: str
    extracted_number: str
    created_at: Optional[datetime] = None

class ApplicationUploadResponse(BaseModel):
    id: Optional[str] = None
    content: str
    application_type: str
    created_at: Optional[datetime] = None

class UnderstatementResponse(BaseModel):
    id: Optional[str] = None
    content: str
    created_at: datetime

class UnderwritingInput(BaseModel):
    payload_content: str

class BankApplicationSchema(BaseModel):
    content: str
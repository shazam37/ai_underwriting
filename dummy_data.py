import uuid
from datetime import date
from database import SessionLocal, DrivingLicense, SSNRecord, Bureau, KYC

# Initialize dummy data
def init_dummy_data():
    """Initialize database with dummy data"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(DrivingLicense).first() or db.query(SSNRecord).first() or db.query(Bureau).first() or db.query(KYC).first():
        db.close()
        return
    
    # Dummy driving licenses
    dummy_licenses = [
        DrivingLicense(
            id=str(uuid.uuid4()),
            license_number="123456789",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 5, 15),
            address="123 Main St, Anytown, CA 90210",
            issue_date=date(2020, 1, 15),
            expiration_date=date(2025, 1, 15),
            sex="M"
        ),
        DrivingLicense(
            id=str(uuid.uuid4()),
            license_number="B9876543",
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1985, 8, 22),
            address="456 Oak Ave, Springfield, NY 12345",
            issue_date=date(2019, 3, 10),
            expiration_date=date(2024, 3, 10),
            sex="F"
        )
    ]

    # Dummy SSN records
    dummy_ssns = [
        SSNRecord(
            id=str(uuid.uuid4()),
            ssn="854659582",
            first_name="John",
            last_name="Doe",
            address="123 Main St, Anytown, CA 90210",
    
        ),
        SSNRecord(
            id=str(uuid.uuid4()),
            ssn="987-65-4321",
            first_name="Jane",
            last_name="Smith",
            address="456 Oak Ave, Springfield, NY 12345",
        )
    ]

    # Dummy Bureau records
    dummy_bureaus = [
        Bureau(
            id=str(uuid.uuid4()),
            ssn="854659582",
            dti="15.25",
            delinq_2yrs=0,
            earliest_cr_line="2010-01-01",
            fico_range_low=740,
            fico_range_high=744,
            inq_last_6mths=1,
            mths_since_last_delinq=None,
            mths_since_last_record=None,
            open_acc=12,
            pub_rec=0,
            revol_bal="8500.00",
            revol_util="22.5",
            total_acc=18,
            initial_list_status="f",
            out_prncp="0.00",
            out_prncp_inv="0.00",
            total_pymnt="15000.00",
            total_pymnt_inv="15000.00",
            total_rec_prncp="12000.00",
            total_rec_int="3000.00",
            total_rec_late_fee="0.00",
            recoveries="0.00",
            collection_recovery_fee="0.00",
            last_pymnt_d="2024-01-15",
            last_pymnt_amnt="450.00",
            next_pymnt_d="2024-02-15",
            last_credit_pull_d="2024-01-10",
            last_fico_range_high=750,
            last_fico_range_low=746,
            collections_12_mths_ex_med=0,
            mths_since_last_major_derog=None,
            policy_code="1",
            application_type="Individual",
            annual_inc_joint=None,
            dti_joint=None,
            verification_status_joint=None,
            acc_now_delinq=0,
            tot_coll_amt="0.00",
            tot_cur_bal="85000.00",
            open_acc_6m=0,
            open_act_il=2,
            open_il_12m=0,
            open_il_24m=1,
            mths_since_rcnt_il=8,
            total_bal_il="25000.00",
            il_util="65.5",
            open_rv_12m=1,
            open_rv_24m=2,
            max_bal_bc="12000.00",
            all_util="22.5",
            total_rev_hi_lim="38000.00",
            inq_fi=1,
            total_cu_tl=2,
            inq_last_12m=3,
            acc_open_past_24mths=2,
            avg_cur_bal="7083.33",
            bc_open_to_buy="29500.00",
            bc_util="22.5",
            chargeoff_within_12_mths=0,
            delinq_amnt="0.00",
            mo_sin_old_il_acct=168,
            mo_sin_old_rev_tl_op=95,
            mo_sin_rcnt_rev_tl_op=8,
            mo_sin_rcnt_tl=8,
            mort_acc=1,
            mths_since_recent_bc=8,
            mths_since_recent_bc_dlq=None,
            mths_since_recent_inq=2,
            mths_since_recent_revol_delinq=None,
            num_accts_ever_120_pd=0,
            num_actv_bc_tl=8,
            num_actv_rev_tl=8,
            num_bc_sats=8,
            num_bc_tl=12,
            num_il_tl=6,
            num_op_rev_tl=8,
            num_rev_accts=12,
            num_rev_tl_bal_gt_0=8,
            num_sats=16,
            num_tl_120dpd_2m=0,
            num_tl_30dpd=0,
            num_tl_90g_dpd_24m=0,
            num_tl_op_past_12m=2,
            pct_tl_nvr_dlq="100.0",
            percent_bc_gt_75="0.0",
            pub_rec_bankruptcies=0,
            tax_liens=0,
            tot_hi_cred_lim="185000.00",
            total_bal_ex_mort="33500.00",
            total_bc_limit="38000.00",
            total_il_high_credit_limit="50000.00",
            revol_bal_joint=None,
            sec_app_fico_range_low=None,
            sec_app_fico_range_high=None,
            sec_app_earliest_cr_line=None,
            sec_app_inq_last_6mths=None,
            sec_app_mort_acc=None,
            sec_app_open_acc=None,
            sec_app_revol_util=None,
            sec_app_open_act_il=None,
            sec_app_num_rev_accts=None,
            sec_app_chargeoff_within_12_mths=None,
            sec_app_collections_12_mths_ex_med=None,
            hardship_flag="N",
            hardship_type=None,
            hardship_reason=None,
            hardship_status=None,
            deferral_term=None,
            hardship_amount=None,
            hardship_start_date=None,
            hardship_end_date=None,
            payment_plan_start_date=None,
            hardship_length=None,
            hardship_dpd=None,
            hardship_loan_status=None,
            orig_projected_additional_accrued_interest=None,
            hardship_payoff_balance_amount=None,
            hardship_last_payment_amount=None,
            debt_settlement_flag="N"
        )]
    
    dummy_kyc = [
        KYC(
            id=str(uuid.uuid4()),
            ssn="854659582",
            zip_code="90210",
            addr_state="123 Main St, Anytown, CA"
        )
    ]
    
    try:
        db.add_all(dummy_licenses)
        db.add_all(dummy_ssns)
        db.add_all(dummy_bureaus)
        db.add_all(dummy_kyc)
        db.commit()
        print("Dummy data initialized successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error initializing dummy data: {e}")
    finally:
        db.close()
"""Mock data used for simulating account aggregator responses for FI types."""

dummy_accounts_data = {
    ###########################################################################
    # TERM_DEPOSIT
    ###########################################################################
    "TERM_DEPOSIT": """<Account type="term_deposit" maskedAccNumber="XXXXX6251" version="1.1" linkedAccRef="CUSP071586251"
    xmlns="http://api.rebit.org.in/FISchema/term_deposit"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/term_deposit ../FISchema/term_deposit.xsd">
    <Profile>
        <Holders type="SINGLE">
            <Holder name="fName mName lName" dob="1992-09-24" mobile="9724242632"
                nominee="NOT-REGISTERED" email="info@cookiejar.co.in" pan="JHCEC4263C"
                ckycCompliance="true" />
        </Holders>
    </Profile>
    <Summary branch="SB Road Pune [SB]" openingDate="2023-10-28" ifsc="SBP0000136"
        accountType="FIXED" maturityAmount="69300.0" maturityDate="2024-10-28" description=""
        interestPayout="HALF-YEARLY" interestRate="10.00" principalAmount="60000.00" tenureDays=""
        tenureMonths="12" tenureYears="1" interestComputation="COMPOUND"
        compoundingFrequency="HALF-YEARLY" interestPeriodicPayoutAmount="5000.00"
        interestOnMaturity="9300.00" currentValue="69300.00" />
    <Transactions startDate="2023-10-28" endDate="2024-10-28" />
</Account>""",
    ###########################################################################
    # RECURRING_DEPOSIT
    ###########################################################################
    "RECURRING_DEPOSIT": """<Account type="recurring_deposit" maskedAccNumber="XXXXX7997" version="1.1"
    linkedAccRef="CUSP943217997" xmlns="http://api.rebit.org.in/FISchema/recurring_deposit"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/recurring_deposit https://specifications.rebit.org.in/api_schema/account_aggregator/FISchema/recurring_deposit.xsd">
    <Profile>
        <Holders type="SINGLE">
            <Holder name="fName mName lName" dob="1981-08-24" mobile="9724242632"
                nominee="NOT-REGISTERED" email="info@cookiejar.in" pan="JHCEC4263C"
                ckycCompliance="false" />
        </Holders>
    </Profile>
    <Summary branch="SB Road Pune [SB]" openingDate="2023-10-28" ifsc="SBP0000136"
        accountType="RECURRING" maturityAmount="64027.42" maturityDate="2023-10-28"
        description="RDLTF" interestPayout="OnMaturity" interestRate="6.712383"
        principalAmount="5000.0" tenureDays="" tenureMonths="0" tenureYears="0"
        recurringAmount="60000.00" recurringDepositDay="1" interestComputation="COMPOUND"
        compoundingFrequency="YEARLY" interestPeriodicPayoutAmount="0" interestOnMaturity="4027.42"
        currentValue="64027.42" />
    <Transactions startDate="2023-10-28" endDate="2023-10-28" />
</Account>""",
    ###########################################################################
    # DEPOSIT
    ###########################################################################
    "DEPOSIT": """<Account type="deposit" maskedAccNumber="XXXXX0717" version="1.1" linkedAccRef="CUSP835050717"
    xmlns="http://api.rebit.org.in/FISchema/deposit"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/deposit https://specifications.rebit.org.in/api_schema/account_aggregator/FISchema/deposit.xsd">
    <Profile>
        <Holders type="SINGLE">
            <Holder name="fName mName lName" dob="1966-06-08" mobile="9724242632"
                nominee="NOT-REGISTERED" landline=""
                address="Senapati Bapat Road,Pune,Maharashtra,India,411016"
                email="info@cookiejar.co.in" pan="JHCEC4263C" ckycCompliance="false" />
        </Holders>
    </Profile>
    <Summary currentBalance="86260.00" currency="INR" exchgeRate=""
        balanceDateTime="2024-10-26T00:00:00.000+00:00" type="SAVINGS" branch="SB Road Pune [SB]"
        facility="OD" ifscCode="SBP0000136" micrCode="" openingDate="2023-10-26"
        currentODLimit="2500000.0000" drawingLimit="2500000.0000" status="ACTIVE">
        <Pending transactionType="DEBIT" amount="6000.0" />
    </Summary>
    <Transactions startDate="2023-10-26" endDate="2024-10-26">
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="116260.00"
            transactionTimestamp="2023-11-01T00:00:00.000+00:00" valueDate="2023-11-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="113760.00"
            transactionTimestamp="2023-11-05T00:00:00.000+00:00" valueDate="2023-11-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="200.0" currentBalance="113960.00"
            transactionTimestamp="2023-11-06T00:00:00.000+00:00" valueDate="2023-11-06" txnId=""
            narration="NEFT/Dividend/BajajFinsv " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="113660.00"
            transactionTimestamp="2023-11-08T00:00:00.000+00:00" valueDate="2023-11-08" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="111160.00"
            transactionTimestamp="2023-11-08T00:00:00.000+00:00" valueDate="2023-11-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="103160.00"
            transactionTimestamp="2023-11-15T00:00:00.000+00:00" valueDate="2023-11-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="40.0" currentBalance="103120.00"
            transactionTimestamp="2023-11-16T00:00:00.000+00:00" valueDate="2023-11-16" txnId=""
            narration="Chrg: Daily Bal Alerts charges for Dec 20" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1000.0" currentBalance="102120.00"
            transactionTimestamp="2023-11-19T00:00:00.000+00:00" valueDate="2023-11-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="101420.00"
            transactionTimestamp="2023-11-20T00:00:00.000+00:00" valueDate="2023-11-20" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="5000.0" currentBalance="96420.00"
            transactionTimestamp="2023-11-25T00:00:00.000+00:00" valueDate="2023-11-25" txnId=""
            narration="UPI/218128539608/Amazon online" reference="" />
        <Transaction type="DEBIT" mode="ATM" amount="10000.0" currentBalance="86420.00"
            transactionTimestamp="2023-11-29T00:00:00.000+00:00" valueDate="2023-11-29" txnId=""
            narration="ATW/536799XXXXXX7446/HDFC ATM" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="116420.00"
            transactionTimestamp="2023-12-01T00:00:00.000+00:00" valueDate="2023-12-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="40000.0" currentBalance="76420.00"
            transactionTimestamp="2023-12-01T00:00:00.000+00:00" valueDate="2023-12-01" txnId=""
            narration="NEFT/Tution Fee/ " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="76120.00"
            transactionTimestamp="2023-12-04T00:00:00.000+00:00" valueDate="2023-12-04" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="73620.00"
            transactionTimestamp="2023-12-05T00:00:00.000+00:00" valueDate="2023-12-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="71120.00"
            transactionTimestamp="2023-12-08T00:00:00.000+00:00" valueDate="2023-12-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="70420.00"
            transactionTimestamp="2023-12-10T00:00:00.000+00:00" valueDate="2023-12-10" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="62420.00"
            transactionTimestamp="2023-12-15T00:00:00.000+00:00" valueDate="2023-12-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="62120.00"
            transactionTimestamp="2023-12-17T00:00:00.000+00:00" valueDate="2023-12-17" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1200.0" currentBalance="60920.00"
            transactionTimestamp="2023-12-19T00:00:00.000+00:00" valueDate="2023-12-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="20.0" currentBalance="60900.00"
            transactionTimestamp="2023-12-21T00:00:00.000+00:00" valueDate="2023-12-21" txnId=""
            narration="ATM Usage Charges" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="9100.0" currentBalance="70000.00"
            transactionTimestamp="2023-12-27T00:00:00.000+00:00" valueDate="2023-12-27" txnId=""
            narration="RTGS/LIC" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="100000.00"
            transactionTimestamp="2024-01-01T00:00:00.000+00:00" valueDate="2024-01-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="4000.0" currentBalance="96000.00"
            transactionTimestamp="2024-01-03T00:00:00.000+00:00" valueDate="2024-01-03" txnId=""
            narration="UPI/122609308010/From:7044223776@ybl/To:MYNTRA@ybl/ Payment for 7eff99fa66c0483184a1c0052342e624"
            reference="" />
        <Transaction type="CREDIT" mode="UPI" amount="100.0" currentBalance="96100.00"
            transactionTimestamp="2024-01-03T00:00:00.000+00:00" valueDate="2024-01-03" txnId=""
            narration="UPI/122609308010/From:7044223776@ybl/To:MYNTRA@ybl/ Payment for 7eff99fa66c0483184a1c0052342e624"
            reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="93600.00"
            transactionTimestamp="2024-01-05T00:00:00.000+00:00" valueDate="2024-01-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="250.0" currentBalance="93350.00"
            transactionTimestamp="2024-01-07T00:00:00.000+00:00" valueDate="2024-01-07" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="500.0" currentBalance="92850.00"
            transactionTimestamp="2024-01-07T00:00:00.000+00:00" valueDate="2024-01-07" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="90350.00"
            transactionTimestamp="2024-01-08T00:00:00.000+00:00" valueDate="2024-01-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="150.0" currentBalance="90200.00"
            transactionTimestamp="2024-01-12T00:00:00.000+00:00" valueDate="2024-01-12" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="82200.00"
            transactionTimestamp="2024-01-15T00:00:00.000+00:00" valueDate="2024-01-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1000.0" currentBalance="81200.00"
            transactionTimestamp="2024-01-19T00:00:00.000+00:00" valueDate="2024-01-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1500.0" currentBalance="79700.00"
            transactionTimestamp="2024-01-24T00:00:00.000+00:00" valueDate="2024-01-24" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="CREDIT" mode="UPI" amount="300.0" currentBalance="80000.00"
            transactionTimestamp="2024-01-26T00:00:00.000+00:00" valueDate="2024-01-26" txnId=""
            narration="UPI/218128539608/Received from 9546215863@ybl" reference="" />
        <Transaction type="CREDIT" mode="UPI" amount="500.0" currentBalance="80500.00"
            transactionTimestamp="2024-01-27T00:00:00.000+00:00" valueDate="2024-01-27" txnId=""
            narration="UPI/218128539608/Received from 9881425632@oksbi/GooglePay" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="110500.00"
            transactionTimestamp="2024-02-01T00:00:00.000+00:00" valueDate="2024-02-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="150.0" currentBalance="110350.00"
            transactionTimestamp="2024-02-02T00:00:00.000+00:00" valueDate="2024-02-02" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="107850.00"
            transactionTimestamp="2024-02-05T00:00:00.000+00:00" valueDate="2024-02-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="105350.00"
            transactionTimestamp="2024-02-08T00:00:00.000+00:00" valueDate="2024-02-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="500.0" currentBalance="104850.00"
            transactionTimestamp="2024-02-10T00:00:00.000+00:00" valueDate="2024-02-10" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1500.0" currentBalance="103350.00"
            transactionTimestamp="2024-02-13T00:00:00.000+00:00" valueDate="2024-02-13" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="95350.00"
            transactionTimestamp="2024-02-15T00:00:00.000+00:00" valueDate="2024-02-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1200.0" currentBalance="94150.00"
            transactionTimestamp="2024-02-19T00:00:00.000+00:00" valueDate="2024-02-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="30000.0" currentBalance="94150.00"
            transactionTimestamp="2024-02-22T00:00:00.000+00:00" valueDate="2024-02-22" txnId=""
            narration="Check to Mr. XYZ" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="94150.00"
            transactionTimestamp="2024-02-25T00:00:00.000+00:00" valueDate="2024-02-25" txnId=""
            narration="I/W CHQ RTN:38:AMOUNT / NAME DIFFER ON ADVICE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="93450.00"
            transactionTimestamp="2024-02-27T00:00:00.000+00:00" valueDate="2024-02-27" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="123450.00"
            transactionTimestamp="2024-03-01T00:00:00.000+00:00" valueDate="2024-03-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="ATM" amount="5000.0" currentBalance="118450.00"
            transactionTimestamp="2024-03-01T00:00:00.000+00:00" valueDate="2024-03-01" txnId=""
            narration="ATW/536799XXXXXX7446/IDBI JALNA RD VIDY NGR AURAGA" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="115950.00"
            transactionTimestamp="2024-03-05T00:00:00.000+00:00" valueDate="2024-03-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="113450.00"
            transactionTimestamp="2024-03-08T00:00:00.000+00:00" valueDate="2024-03-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="500.0" currentBalance="112950.00"
            transactionTimestamp="2024-03-10T00:00:00.000+00:00" valueDate="2024-03-10" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="400.0" currentBalance="112550.00"
            transactionTimestamp="2024-03-12T00:00:00.000+00:00" valueDate="2024-03-12" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="104550.00"
            transactionTimestamp="2024-03-15T00:00:00.000+00:00" valueDate="2024-03-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1400.0" currentBalance="103150.00"
            transactionTimestamp="2024-03-19T00:00:00.000+00:00" valueDate="2024-03-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="12000.0" currentBalance="91150.00"
            transactionTimestamp="2024-03-30T00:00:00.000+00:00" valueDate="2024-03-30" txnId=""
            narration="ITR" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="121150.00"
            transactionTimestamp="2024-04-01T00:00:00.000+00:00" valueDate="2024-04-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="118650.00"
            transactionTimestamp="2024-04-05T00:00:00.000+00:00" valueDate="2024-04-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="500.0" currentBalance="118150.00"
            transactionTimestamp="2024-04-06T00:00:00.000+00:00" valueDate="2024-04-06" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="115650.00"
            transactionTimestamp="2024-04-08T00:00:00.000+00:00" valueDate="2024-04-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="80.0" currentBalance="115570.00"
            transactionTimestamp="2024-04-12T00:00:00.000+00:00" valueDate="2024-04-12" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="150.0" currentBalance="115720.00"
            transactionTimestamp="2024-04-14T00:00:00.000+00:00" valueDate="2024-04-14" txnId=""
            narration="NEFT/Dividend/Reliance " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="107720.00"
            transactionTimestamp="2024-04-15T00:00:00.000+00:00" valueDate="2024-04-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2800.0" currentBalance="104920.00"
            transactionTimestamp="2024-04-18T00:00:00.000+00:00" valueDate="2024-04-18" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="900.0" currentBalance="104020.00"
            transactionTimestamp="2024-04-19T00:00:00.000+00:00" valueDate="2024-04-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="29900.0" currentBalance="74120.00"
            transactionTimestamp="2024-04-27T00:00:00.000+00:00" valueDate="2024-04-27" txnId=""
            narration="UPI/mandate for IPO" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2100.0" currentBalance="72020.00"
            transactionTimestamp="2024-04-29T00:00:00.000+00:00" valueDate="2024-04-29" txnId=""
            narration="UPI/122609308010/From:7044223776@ybl/To:MYNTRA@ybl/ Payment for 7eff99fa66c0483184a1c0052342e624"
            reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="102020.00"
            transactionTimestamp="2024-05-01T00:00:00.000+00:00" valueDate="2024-05-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="ATM" amount="10000.0" currentBalance="92020.00"
            transactionTimestamp="2024-05-03T00:00:00.000+00:00" valueDate="2024-05-03" txnId=""
            narration="ATW/536799XXXXXX7446/HDFC ATM " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="89520.00"
            transactionTimestamp="2024-05-05T00:00:00.000+00:00" valueDate="2024-05-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="3600.0" currentBalance="85920.00"
            transactionTimestamp="2024-05-05T00:00:00.000+00:00" valueDate="2024-05-05" txnId=""
            narration="UPI/IRCTC" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="83420.00"
            transactionTimestamp="2024-05-08T00:00:00.000+00:00" valueDate="2024-05-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="ATM" amount="10000.0" currentBalance="73420.00"
            transactionTimestamp="2024-05-13T00:00:00.000+00:00" valueDate="2024-05-13" txnId=""
            narration="ATW/536799XXXXXX7446/HDFC ATM " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="65420.00"
            transactionTimestamp="2024-05-15T00:00:00.000+00:00" valueDate="2024-05-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="800.0" currentBalance="64620.00"
            transactionTimestamp="2024-05-19T00:00:00.000+00:00" valueDate="2024-05-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1300.0" currentBalance="63320.00"
            transactionTimestamp="2024-05-23T00:00:00.000+00:00" valueDate="2024-05-23" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="600.0" currentBalance="62720.00"
            transactionTimestamp="2024-05-27T00:00:00.000+00:00" valueDate="2024-05-27" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="92720.00"
            transactionTimestamp="2024-06-01T00:00:00.000+00:00" valueDate="2024-06-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="ATM" amount="7000.0" currentBalance="85720.00"
            transactionTimestamp="2024-06-03T00:00:00.000+00:00" valueDate="2024-06-03" txnId=""
            narration="ATW/536799XXXXXX7446/HDFC ATM " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="83220.00"
            transactionTimestamp="2024-06-05T00:00:00.000+00:00" valueDate="2024-06-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="80720.00"
            transactionTimestamp="2024-06-08T00:00:00.000+00:00" valueDate="2024-06-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="80020.00"
            transactionTimestamp="2024-06-10T00:00:00.000+00:00" valueDate="2024-06-10" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="72020.00"
            transactionTimestamp="2024-06-15T00:00:00.000+00:00" valueDate="2024-06-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="200.0" currentBalance="72220.00"
            transactionTimestamp="2024-06-17T00:00:00.000+00:00" valueDate="2024-06-17" txnId=""
            narration="NEFT/Dividend/Axis " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1150.0" currentBalance="71070.00"
            transactionTimestamp="2024-06-19T00:00:00.000+00:00" valueDate="2024-06-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="70770.00"
            transactionTimestamp="2024-06-23T00:00:00.000+00:00" valueDate="2024-06-23" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="40000.0" currentBalance="30770.00"
            transactionTimestamp="2024-06-25T00:00:00.000+00:00" valueDate="2024-06-25" txnId=""
            narration="NEFT/Tution Fee/ " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="180.0" currentBalance="30590.00"
            transactionTimestamp="2024-06-27T00:00:00.000+00:00" valueDate="2024-06-27" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="60590.00"
            transactionTimestamp="2024-07-01T00:00:00.000+00:00" valueDate="2024-07-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="60290.00"
            transactionTimestamp="2024-07-02T00:00:00.000+00:00" valueDate="2024-07-02" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="59590.00"
            transactionTimestamp="2024-07-03T00:00:00.000+00:00" valueDate="2024-07-03" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="57090.00"
            transactionTimestamp="2024-07-05T00:00:00.000+00:00" valueDate="2024-07-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="54590.00"
            transactionTimestamp="2024-07-08T00:00:00.000+00:00" valueDate="2024-07-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="54290.00"
            transactionTimestamp="2024-07-13T00:00:00.000+00:00" valueDate="2024-07-13" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="46290.00"
            transactionTimestamp="2024-07-15T00:00:00.000+00:00" valueDate="2024-07-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="45590.00"
            transactionTimestamp="2024-07-18T00:00:00.000+00:00" valueDate="2024-07-18" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1000.0" currentBalance="44590.00"
            transactionTimestamp="2024-07-19T00:00:00.000+00:00" valueDate="2024-07-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="74590.00"
            transactionTimestamp="2024-08-01T00:00:00.000+00:00" valueDate="2024-08-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="72090.00"
            transactionTimestamp="2024-08-05T00:00:00.000+00:00" valueDate="2024-08-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="71390.00"
            transactionTimestamp="2024-08-06T00:00:00.000+00:00" valueDate="2024-08-06" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="71090.00"
            transactionTimestamp="2024-08-07T00:00:00.000+00:00" valueDate="2024-08-07" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="68590.00"
            transactionTimestamp="2024-08-08T00:00:00.000+00:00" valueDate="2024-08-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="60590.00"
            transactionTimestamp="2024-08-15T00:00:00.000+00:00" valueDate="2024-08-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1500.0" currentBalance="59090.00"
            transactionTimestamp="2024-08-19T00:00:00.000+00:00" valueDate="2024-08-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2000.0" currentBalance="57090.00"
            transactionTimestamp="2024-08-20T00:00:00.000+00:00" valueDate="2024-08-20" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="730.0" currentBalance="56360.00"
            transactionTimestamp="2024-08-23T00:00:00.000+00:00" valueDate="2024-08-23" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="350.0" currentBalance="56710.00"
            transactionTimestamp="2024-08-27T00:00:00.000+00:00" valueDate="2024-08-27" txnId=""
            narration="NEFT/Interest " reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="86710.00"
            transactionTimestamp="2024-09-01T00:00:00.000+00:00" valueDate="2024-09-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="84210.00"
            transactionTimestamp="2024-09-05T00:00:00.000+00:00" valueDate="2024-09-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="83510.00"
            transactionTimestamp="2024-09-07T00:00:00.000+00:00" valueDate="2024-09-07" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="81010.00"
            transactionTimestamp="2024-09-08T00:00:00.000+00:00" valueDate="2024-09-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="73010.00"
            transactionTimestamp="2024-09-15T00:00:00.000+00:00" valueDate="2024-09-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="450.0" currentBalance="72560.00"
            transactionTimestamp="2024-09-17T00:00:00.000+00:00" valueDate="2024-09-17" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1000.0" currentBalance="71560.00"
            transactionTimestamp="2024-09-19T00:00:00.000+00:00" valueDate="2024-09-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="CREDIT" mode="OTHERS" amount="30000.0" currentBalance="101560.00"
            transactionTimestamp="2024-10-01T00:00:00.000+00:00" valueDate="2024-10-01" txnId=""
            narration="NEFT/SBIN322147057322/PENSION " reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="101260.00"
            transactionTimestamp="2024-10-04T00:00:00.000+00:00" valueDate="2024-10-04" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="2500.0" currentBalance="98760.00"
            transactionTimestamp="2024-10-05T00:00:00.000+00:00" valueDate="2024-10-05" txnId=""
            narration="PCD/536799XXXXXX7446/POLICYBAZAAR" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="2500.0" currentBalance="96260.00"
            transactionTimestamp="2024-10-08T00:00:00.000+00:00" valueDate="2024-10-08" txnId=""
            narration="UPI/515429XXXXXX7446/MutualFunds" reference="" />
        <Transaction type="DEBIT" mode="OTHERS" amount="700.0" currentBalance="95560.00"
            transactionTimestamp="2024-10-10T00:00:00.000+00:00" valueDate="2024-10-10" txnId=""
            narration="PCD/536799XXXXXX7446/HP PETROLEUM" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="8000.0" currentBalance="87560.00"
            transactionTimestamp="2024-10-15T00:00:00.000+00:00" valueDate="2024-10-15" txnId=""
            narration="UPI/231948XXXXXX7446/Rent" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="1000.0" currentBalance="86560.00"
            transactionTimestamp="2024-10-19T00:00:00.000+00:00" valueDate="2024-10-19" txnId=""
            narration="UPI/218128539608/Electricity/tpslqr@MSEB" reference="" />
        <Transaction type="DEBIT" mode="UPI" amount="300.0" currentBalance="86260.00"
            transactionTimestamp="2024-10-23T00:00:00.000+00:00" valueDate="2024-10-23" txnId=""
            narration="UPI/218128539608/Pay to BharatPe Merchant/BHARATPE" reference="" />
    </Transactions>
</Account>""",
    ###########################################################################
    # EQUITIES
    ###########################################################################
    "EQUITIES": """<Account linkedAccRef="CUSPFN94081779581001" maskedDematId="XXXXXXXXXXXX1001" version="1.0.0"
    type="equities" xmlns="http://api.rebit.org.in/FISchema/equities"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/equities https://specifications.rebit.org.in/api_schema/account_aggregator/FISchema/equities.xsd">
    <Profile>
        <Holders>
            <Holder name="" dob="1980-01-01" mobile="9724242632" nominee="NOT-REGISTERED"
                dematId="1208160088348123" landline=""
                address="S/OTEST 417/193 K RADHAPURAM ROAD Delhi" email="info@cookiejar.in"
                pan="JHCEC4263C" kycCompliance="false" />
        </Holders>
    </Profile>
    <Summary currentValue="582.14">
        <Investment>
            <Holdings type="DEMAT">
                <Holding issuerName="VINTRON INFORMATICS LIMITED" isin="INE043B01028"
                    isinDescription="VINTRON INFORM-EQ1/-" units="12" lastTradedPrice="5.85" />
                <Holding
                    issuerName="TRIVENI ENTERPRISES LIMITED# FORMERLY TRIVENI ENTERPRISES PRIVATE LIMITED"
                    isin="INE916P01025" isinDescription="TRIVENI-EQ FV 1" units="24"
                    lastTradedPrice="3.25" />
                <Holding issuerName="SHALIMAR PRODUCTIONS LTD- FORMERLY SHALIMAR AGRO PRODUCTS LTD"
                    isin="INE435E01020" isinDescription="SHALIMAR PRODU" units="113"
                    lastTradedPrice="0.49" />
                <Holding
                    issuerName="AMRAWORLD AGRICO LIMITED [FORMERLY GUJARAT NARMADA SPINNING LTD]"
                    isin="INE735C01027" isinDescription="AMRAWORLD -EQ RS 1" units="269"
                    lastTradedPrice="0.78" />
                <Holding
                    issuerName="LUHARUKA MEDIA &amp; INFRA LIMITED#FORMERLY HINDUSTAN STOCKLAND LTD,SPLASH MEDIAWORKS LTD"
                    isin="INE195E01020" isinDescription="LUHARUKA MEDIA-EQ1/-" units="16"
                    lastTradedPrice="3.6" />
                <Holding issuerName="PMC CUSPCORP LIMITED#FORMERLY PRITI MERCANTILE COMPANY LIMITED"
                    isin="INE793G01035" isinDescription="PMC CUSPCO-EQ" units="27"
                    lastTradedPrice="1.95" />
                <Holding
                    issuerName="LLOYDS STEELS INDUSTRIES LIMITED#FORMERLY ENCON TECHNOLOGIES LTD"
                    isin="INE093R01011" isinDescription="LLOYDS STEELS-EQ" units="10"
                    lastTradedPrice="5.85" />
            </Holdings>
        </Investment>
    </Summary>
</Account>""",
    ###########################################################################
    # MUTUAL_FUNDS
    ###########################################################################
    "MUTUAL_FUNDS": """<Account linkedAccRef="CUSPFN60424330284950" maskedDematID="XXXXXXXXXXXX4950"
    maskedFolioNo="XXXX5054" version="1.0.0" type="mutualfunds"
    xmlns="http://api.rebit.org.in/FISchema/mutual_funds"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/mutual_funds ../FISchema/mutual_funds.xsd">
    <Profile>
        <Holders>
            <Holder name="" dob="1977-08-02" mobile="9724242632" nominee="REGISTERED"
                dematId="XXXXXXXXXXXX0987" folioNo="XXXXX4567" landline=""
                address="Address1 of Folio: 16375054, Address2 of Folio: 16375054, Address3 of Folio: 16375054"
                email="info@cookiejar.in" pan="JHCEC4263C" kycCompliance="true" />
        </Holders>
    </Profile>
    <Summary costValue="372186.67" currentValue="2.025018787E7">
        <Investment>
            <Holdings>
                <Holding amc="Kotak Mutual Fund" registrar="CUSPMONEY"
                    schemeCode="Kotak Low Duration Fund Direct Growth" schemeOption="GROWTH_TYPE"
                    schemeTypes="EQUITY_SCHEMES" schemeCategory="SMALL_CAP_FUND" isin="INF178L01AX4"
                    isinDescription="" ucc="" amfiCode="186740" folioNo="11933230" FatcaStatus="Y"
                    closingUnits="6.45" lienUnits="0" nav="3103.1880" navDate="2024-05-31"
                    lockinUnits="0" />
                <Holding amc="MFSBI Test amc" registrar="CAMS" schemeCode="DIRECT"
                    schemeOption="GROWTH_TYPE" schemeTypes="EQUITY_SCHEMES"
                    schemeCategory="LARGE_CAP_FUND" isin="INF200K01180" isinDescription="" ucc=""
                    amfiCode="103504" folioNo="16375054" FatcaStatus="Y" closingUnits="5908.24"
                    lienUnits="0" nav="62.6655" navDate="2024-05-31" lockinUnits="0" />
                <Holding amc="HDFC Mutual Fund" registrar="CAMS" schemeCode="DIRECT"
                    schemeOption="GROWTH_TYPE" schemeTypes="EQUITY_SCHEMES"
                    schemeCategory="SMALL_CAP_FUND" isin="INF179K01756" isinDescription="" ucc=""
                    amfiCode="125494" folioNo="21536800" FatcaStatus="Y" closingUnits="375.87"
                    lienUnits="0" nav="53.2841" navDate="2024-05-31" lockinUnits="0" />
            </Holdings>
        </Investment>
    </Summary>
</Account>""",
    ###########################################################################
    # INSURANCE_POLICIES
    ###########################################################################
    "INSURANCE_POLICIES": """<Account type="life_insurance" maskedPolicyNumber="1088806820000" version="1.0.0"
    linkedAccRef="CUSP1088806820000" xmlns="http://api.rebit.org.in/FISchema/life_insurance"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/life_insurance ../FISchema/life_insurance.xsd">
    <Profile>
        <Holders>
            <Holder name="" />
        </Holders>
    </Profile>
    <Summary policyType="TERM" policyStatus="ACTIVE" sumAssured="150000.0" tenureYears="2"
        premiumPaymentYears="2" premiumAmount="120000.0" premiumFrequency="MONTHLY"
        policyLoanStatus="NOT_OPTED" currentValue="100000.0" assignment="NO"
        surrenderValue="100000.0" exclusions="exclusion details" />
    <Transactions>
        <Transaction txnId="734117" txnDate="2023-01-01" narration="" type="BONUS" amount="120000.0" />
    </Transactions>
</Account>""",
    ###########################################################################
    # GENERAL_INSURANCE
    ###########################################################################
    "GENERAL_INSURANCE": """<Account type="general_insurance" maskedPolicyNumber="128109038" version="1.0.0"
    linkedAccRef="CUSP128109038" xmlns="http://api.rebit.org.in/FISchema/general_insurance"
    xmlns:wstxns1="http://www.w3.org/2001/XMLSchema-instance"
    wstxns1:schemaLocation="http://api.rebit.org.in/FISchema/general_insurance ../FISchema/general_insurance.xsd">
    <Profile>
        <Holders>
            <Holder name="" />
        </Holders>
    </Profile>
    <Summary policyName="Supreme Health" policyNumber="1234567890" uinNumber=""
        policyDescription="This plan offers health insurance services to individual customers."
        sumAssured="200000.0" tenureMonths="36" premiumAmount="5000.0" policyStartDate="2023-04-12"
        policyExpiryDate="2026-04-12" policyType="FIXED_BENEFIT" insuranceType="HEALTH"
        premiumFrequency="ANNUALLY" premiumPaymentYears="3" nextPremiumDueDate="2024-04-12"
        policyStatus="ACTIVE">
        <Covers>
            <Cover uinNumber="" coverName="Annual Health Check-up"
                coverDescription="Rider To Cover Annual Health Checkup." sumAssured="10000.0"
                sumInsured="0.0" tenureYears="3" tenureMonths="36" premiumAmount="1000.0"
                coverStartDate="2023-04-12" coverEndDate="2023-08-12" />
        </Covers>
    </Summary>
    <Transactions startDate="2023-04-01" endDate="2023-05-31">
        <Transaction txnId="a3c722ac4d99cdr4" txnDate="2023-04-12" narration="narration1"
            type="PREMIUM_PAYMENT" amount="6000.0" />
    </Transactions>
</Account>""",
}

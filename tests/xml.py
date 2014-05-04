# vim: set fileencoding=utf-8

# flake8: noqa

finance_transactions_211 = u"""
<xmlDoc>
    <metadata>
        <errorcode>0</errorcode>
        <returnvalue>0</returnvalue>
    </metadata>
    <data>
        <enclosure id="626" required="" label="Transaction Pages" showtabs="" swipe="" active="true">
            <encid>626</encid>
            <xmlcontrol id="626" form="1">
                <xmlcurrenttitle insert="" delete="" nosearch="1" special="1">RCC FERRET FANCIERS (211)</xmlcurrenttitle>
            </xmlcontrol>
            <div class="formenc">
                <enclosure id="654" required="" label="Transaction Pages Years" showtabs="" swipe="" active="true">
                    <encid>654</encid>
                    <tabenclosure id="654-0" required="" label="13-14" showtabs="1" active="true">
                        <encid>654-0</encid>
                        <enclosure id="655" required="" label="Overview" showtabs="" swipe="" active="true">
                            <encid>655</encid>
                            <div class="formenc">
                                <infoenclosure layout="ul">
                                    <infofield id="667-0" fieldtype="nvarchar" alias="MemDetails">Number of Full Members: 342 of 120 (285%)</infofield>
                                    <infofield id="667-1" fieldtype="nvarchar" alias="MemNum">Number of Life/Associate members: 11</infofield>
                                    <infofield id="667-2" fieldtype="nvarchar" alias="YearDetails">Membership costs £5.00</infofield>
                                </infoenclosure>
                                <label removereadonly="">FULL MEMBERSHIP PERCENTAGE</label>
                                <infobars>
                                    <infobar>285</infobar>
                                </infobars>
                                <infoenclosure>
                                    <infofield id="4014-0" fieldtype="int" alias="Download Transactions" linkobj="finance/transactions/overview/csv" imglink="excelicon.gif" linktitle="Download Transaction Report">172</infofield>
                                </infoenclosure>
                                <label removereadonly="">FUNDING OVERVIEW</label>
                                <infotable tablekey="0" tableid="658">
                                    <infotableheadrow>
                                        <infotablehead>Funding (Code)</infotablehead>
                                        <infotablehead>Total Amount (£)</infotablehead>
                                    </infotableheadrow>
                                    <infotablerow>
                                        <infotablecell fieldtype="nvarchar" alias="Funding (Code)" event="changeTab(eObj.controlObj, 52, '0');">Grant (0)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Total Amount (£)">0</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldtype="nvarchar" alias="Funding (Code)" event="changeTab(eObj.controlObj, 52, '1');">SGI (1)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Total Amount (£)">1179.25</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldtype="nvarchar" alias="Funding (Code)" event="changeTab(eObj.controlObj, 52, '2');">Harlington (2)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Total Amount (£)">0</infotablecell>
                                    </infotablerow>
                                    <infotablefootrow>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot fieldcon="">1,179.25</infotablefoot>
                                    </infotablefootrow>
                                </infotable>
                                <infotable tablekey="Grant (0)" tableid="660" title="Grant (0)" event="changeTab(eObj.controlObj, 52, '0');">
                                    <infotableheadrow>
                                        <infotablehead>Account (Code)</infotablehead>
                                        <infotablehead>General (00)</infotablehead>
                                        <infotablehead>Staff Recharging (05)</infotablehead>
                                        <infotablehead>Winter All-Nighter (52)</infotablehead>
                                        <infotablehead>Spring All-Nighter (53)</infotablehead>
                                        <infotablehead>Post-Grad Cinema Nights (55)</infotablehead>
                                        <infotablehead>Cinema Hire (57)</infotablehead>
                                        <infotablehead>Equipment Renewal Fund Raising (58)</infotablehead>
                                        <infotablehead>Accounts Payable Reserves (59)</infotablehead>
                                    </infotableheadrow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Copyright &amp; Royalties (725)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-300</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Equipment Purchase (685)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-200.28</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Grant Receivable (470)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">500.28</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablefootrow>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot fieldcon="1">0.00</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                    </infotablefootrow>
                                </infotable>
                                <infotable tablekey="SGI (1)" tableid="660" title="SGI (1)" event="changeTab(eObj.controlObj, 52, '1');">
                                    <infotableheadrow>
                                        <infotablehead>Account (Code)</infotablehead>
                                        <infotablehead>General (00)</infotablehead>
                                        <infotablehead>Staff Recharging (05)</infotablehead>
                                        <infotablehead>Winter All-Nighter (52)</infotablehead>
                                        <infotablehead>Spring All-Nighter (53)</infotablehead>
                                        <infotablehead>Post-Grad Cinema Nights (55)</infotablehead>
                                        <infotablehead>Cinema Hire (57)</infotablehead>
                                        <infotablehead>Equipment Renewal Fund Raising (58)</infotablehead>
                                        <infotablehead>Accounts Payable Reserves (59)</infotablehead>
                                    </infotableheadrow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Carriage (630)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-988.23</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Consumables (640)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-84.55</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">-95.34</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">-376.83</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Copyright &amp; Royalties (725)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-2752.61</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">-653.99</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">-550</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">-439.55</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">-166</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">-85</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Cultural Activities (650)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-26.04</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">-20.82</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">-13.68</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Donations (430)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">857</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Engraving &amp; Signwriting (670)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-9</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Equipment Hire (690)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-15</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Equipment Purchase (685)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-806.13</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">-79.05</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">-1927.94</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Goods &amp; Services (450)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Staff Recharging (05)">359.7</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Post-Grad Cinema Nights (55)">120</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Cinema Hire (57)">919.45</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Goods for Resale (705)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-1476.8</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">-176.23</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">-107.43</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Hospitality (730)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">-190.17</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Maintenance &amp; Repairs (770)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-305</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Members Funds (225)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">2502.88</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">-6652.52</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Accounts Payable Reserves (59)">185</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Printing Costs (820)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-359</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Rental Income (510)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">1027.4</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Sales General (520)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">2095.97</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Winter All-Nighter (52)">333.33</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Spring All-Nighter (53)">312.5</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Sponsorship (550)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">1500</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Staff Subsistence (850)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-87.89</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">-67.21</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">-68.68</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Subscriptions (570)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">1450.1</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Ticket Income (580)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">5062.92</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Winter All-Nighter (52)">1215.81</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Spring All-Nighter (53)">1421.65</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="Post-Grad Cinema Nights (55)">396.23</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablefootrow>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot fieldcon="">6,729.02</infotablefoot>
                                        <infotablefoot fieldcon="">359.70</infotablefoot>
                                        <infotablefoot fieldcon="">477.32</infotablefoot>
                                        <infotablefoot fieldcon="">1,008.04</infotablefoot>
                                        <infotablefoot fieldcon="">55.86</infotablefoot>
                                        <infotablefoot fieldcon="">549.60</infotablefoot>
                                        <infotablefoot fieldcon="1">-8,100.29</infotablefoot>
                                        <infotablefoot fieldcon="">100.00</infotablefoot>
                                    </infotablefootrow>
                                </infotable>
                                <infotable tablekey="Harlington (2)" tableid="660" title="Harlington (2)" event="changeTab(eObj.controlObj, 52, '2');">
                                    <infotableheadrow>
                                        <infotablehead>Account (Code)</infotablehead>
                                        <infotablehead>General (00)</infotablehead>
                                        <infotablehead>Staff Recharging (05)</infotablehead>
                                        <infotablehead>Winter All-Nighter (52)</infotablehead>
                                        <infotablehead>Spring All-Nighter (53)</infotablehead>
                                        <infotablehead>Post-Grad Cinema Nights (55)</infotablehead>
                                        <infotablehead>Cinema Hire (57)</infotablehead>
                                        <infotablehead>Equipment Renewal Fund Raising (58)</infotablehead>
                                        <infotablehead>Accounts Payable Reserves (59)</infotablehead>
                                    </infotableheadrow>
                                    <infotablerow>
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Grant Receivable (470)</infotablecell>
                                        <infotablecell fieldcon="" fieldtype="float" alias="General (00)">13095.89</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablerow rowclass="even">
                                        <infotablecell fieldcon="" fieldtype="nvarchar" alias="Account (Code)">Members Funds (225)</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="General (00)">-13095.89</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Staff Recharging (05)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Winter All-Nighter (52)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Spring All-Nighter (53)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Post-Grad Cinema Nights (55)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Cinema Hire (57)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Equipment Renewal Fund Raising (58)">&#x00a0;</infotablecell>
                                        <infotablecell fieldcon="1" fieldtype="float" alias="Accounts Payable Reserves (59)">&#x00a0;</infotablecell>
                                    </infotablerow>
                                    <infotablefootrow>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot fieldcon="1">0.00</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                        <infotablefoot>&#x00a0;</infotablefoot>
                                    </infotablefootrow>
                                </infotable>
                            </div>
                        </enclosure>
                        <enclosure id="52" required="" label="Transaction Lines" showtabs="" swipe="" active="false" />
                        <enclosure id="656" required="" label="Budget for 14-15" showtabs="" swipe="" active="false" />
                        <enclosure id="659" required="" label="Outstanding Invoices" showtabs="" swipe="" active="false" />
                        <enclosure id="5065" required="" label="Trend Graphs" showtabs="" swipe="" active="false" />
                    </tabenclosure>
                    <tabenclosure id="654-1" required="" label="12-13" showtabs="1" active="false" />
                    <tabenclosure id="654-2" required="" label="11-12" showtabs="1" active="false" />
                    <tabenclosure id="654-3" required="" label="10-11" showtabs="1" active="false" />
                    <tabenclosure id="654-4" required="" label="09-10" showtabs="1" active="false" />
                    <tabenclosure id="654-5" required="" label="08-09" showtabs="1" active="false" />
                    <tabenclosure id="654-6" required="" label="07-08" showtabs="1" active="false" />
                    <tabenclosure id="654-7" required="" label="06-07" showtabs="1" active="false" />
                    <tabenclosure id="654-8" required="" label="05-06" showtabs="1" active="false" />
                    <tabenclosure id="654-9" required="" label="04-05" showtabs="1" active="false" />
                    <tabenclosure id="654-10" required="" label="03-04" showtabs="1" active="false" />
                    <tabenclosure id="654-11" required="" label="02-03" showtabs="1" active="false" />
                    <tabenclosure id="654-12" required="" label="01-02" showtabs="1" active="false" />
                    <tabenclosure id="654-13" required="" label="00-01" showtabs="1" active="false" />
                    <tabenclosure id="654-14" required="" label="99-00" showtabs="1" active="false" />
                    <tabenclosure id="654-15" required="" label="98-99" showtabs="1" active="false" />
                </enclosure>
            </div>
        </enclosure>
    </data>
</xmlDoc>
"""

admin_csp_details_211 = u"""
<xmlDoc>
    <metadata>
        <errorcode>0</errorcode>
        <returnvalue>0</returnvalue>
    </metadata>
    <data>
        <enclosure id="41" required="" label="Details" showtabs="" swipe="" active="true">
            <encid>41</encid>
            <xmlcontrol id="41" form="1">
                <xmlcurrenttitle insert="" delete="" nosearch="1" special="1">RCC FERRET FANCIERS (211)</xmlcurrenttitle>
            </xmlcontrol>
            <div class="formenc">
                <enclosure id="392" required="" label="Overview" showtabs="" swipe="" active="true">
                    <encid>392</encid>
                    <div class="formenc">
                        <label removereadonly="">STATUS</label>
                        <infoenclosure>
                            <infofield id="352-0" fieldtype="varchar" hidelabel="1">Active</infofield>
                        </infoenclosure>
                        <label removereadonly="">WEBSITE</label>
                        <infoenclosure>
                            <infofield id="676-0" fieldtype="nvarchar" link="http://www.union.ic.ac.uk/" classname="infolink" hidelabel="1">rcc/ffanciers</infofield>
                        </infoenclosure>
                        <label removereadonly="">EMAIL</label>
                        <infoenclosure>
                            <infofield id="677-0" fieldtype="nvarchar" link="mailto:" classname="infolink" hidelabel="1">ffanciers</infofield>
                        </infoenclosure>
                        <label removereadonly="">SAC PRINTER PIN</label>
                        <infoenclosure>
                            <infofield id="602-0" fieldtype="int" hidelabel="1">2222</infofield>
                        </infoenclosure>
                        <label removereadonly="">CURRENT PROFILE ENTRY</label>
                        <infoenclosure layout="ul">
                            <infofield id="353-0" fieldtype="nvarchar" hidelabel="1">A short description.</infofield>
                            <infofield id="353-1" fieldtype="text" hidelabel="1">A long description.</infofield>
                        </infoenclosure>
                    </div>
                </enclosure>
                <enclosure id="395" required="" label="Members" showtabs="" swipe="" active="false" />
            </div>
        </enclosure>
    </data>
</xmlDoc>
"""

norecords = """
<xmlDoc>
    <metadata>
        <errorcode>0</errorcode>
        <returnvalue>0</returnvalue>
    </metadata>
    <data>
        <enclosure id="41" required="" label="Details" showtabs="" swipe="" active="true">
            <encid>41</encid>
            <xmlcontrol id="41" form="0">
                <xmlcurrenttitle insert="" delete="" nosearch="1" special="1">NO RECORDS</xmlcurrenttitle>
            </xmlcontrol>
        </enclosure>
    </data>
</xmlDoc>
"""

admin_csp_details_211_tab395 = """
<xmlDoc>
    <metadata>
        <errorcode>0</errorcode>
        <returnvalue>0</returnvalue>
    </metadata>
    <data>
        <encid>395</encid>
        <div class="formenc">
            <label removereadonly="">FULL MEMBERSHIP</label>
            <infoenclosure>
                <infofield id="354-0" fieldtype="nvarchar" hidelabel="1">Number of Full Members: 342 of 120 (285%)</infofield>
                <infofield id="354-1" fieldtype="nvarchar" hidelabel="1">Membership costs £5.00</infofield>
            </infoenclosure>
            <label removereadonly="">FULL MEMBERSHIP</label>
            <infobars>
                <infobar>285</infobar>
            </infobars>
            <label removereadonly="">OTHER MEMBERSHIP</label>
            <infoenclosure>
                <infofield id="355-0" fieldtype="nvarchar" hidelabel="1">Number of Life/Associate members: 11</infofield>
            </infoenclosure>
            <label removereadonly="">MEMBERS</label>
            <infoenclosure layout="ul" title="Full" classname="infosubblock">
                <infofield id="1083-0" fieldtype="nvarchar" alias="Name">Shanell Loftin (00523715)</infofield>                                                                           [41/1584]
                <infofield id="1083-1" fieldtype="nvarchar" alias="Name">Lessie Wolff (00013036)</infofield>
                <infofield id="1083-2" fieldtype="nvarchar" alias="Name">Angelita Orlando (00370929)</infofield>
                <infofield id="1083-3" fieldtype="nvarchar" alias="Name">Ellsworth Kent (00477379)</infofield>
                <infofield id="1083-4" fieldtype="nvarchar" alias="Name">Jodee Seaman (00906954)</infofield>
                <infofield id="1083-5" fieldtype="nvarchar" alias="Name">Jeneva John (00222872)</infofield>
                <infofield id="1083-6" fieldtype="nvarchar" alias="Name">Joe Portillo (00431662)</infofield>
                <infofield id="1083-7" fieldtype="nvarchar" alias="Name">Wes Whitlow (00655604)</infofield>
                <infofield id="1083-8" fieldtype="nvarchar" alias="Name">Pearle Bourque (00601598)</infofield>
                <infofield id="1083-9" fieldtype="nvarchar" alias="Name">Petronila Jacques (00791188)</infofield>
                <infofield id="1083-10" fieldtype="nvarchar" alias="Name">Corine Mcbee (00487889)</infofield>
                <infofield id="1083-11" fieldtype="nvarchar" alias="Name">Paris Hendrix (00809609)</infofield>
                <infofield id="1083-12" fieldtype="nvarchar" alias="Name">Robt Ennis (00760662)</infofield>
                <infofield id="1083-13" fieldtype="nvarchar" alias="Name">Otha Borders (00391464)</infofield>
                <infofield id="1083-14" fieldtype="nvarchar" alias="Name">Margene Christiansen (00533115)</infofield>
                <infofield id="1083-15" fieldtype="nvarchar" alias="Name">Le Wasson (00563264)</infofield>
                <infofield id="1083-16" fieldtype="nvarchar" alias="Name">Coreen Noonan (00675804)</infofield>
                <infofield id="1083-17" fieldtype="nvarchar" alias="Name">Tiny Bean (00274393)</infofield>
                <infofield id="1083-18" fieldtype="nvarchar" alias="Name">Grayce Atwood (00026050)</infofield>
                <infofield id="1083-19" fieldtype="nvarchar" alias="Name">Nikki Ferry (00813381)</infofield>
                <infofield id="1083-20" fieldtype="nvarchar" alias="Name">Jewell Stratton (00510261)</infofield>
                <infofield id="1083-21" fieldtype="nvarchar" alias="Name">Clair Grice (00166255)</infofield>
                <infofield id="1083-22" fieldtype="nvarchar" alias="Name">Angelika Mcpherson (00183317)</infofield>
                <infofield id="1083-23" fieldtype="nvarchar" alias="Name">Willa Numbers (00241784)</infofield>
                <infofield id="1083-24" fieldtype="nvarchar" alias="Name">Maybell Creighton (00423760)</infofield>
                <infofield id="1083-25" fieldtype="nvarchar" alias="Name">Cassy Barkley (00127887)</infofield>
                <infofield id="1083-26" fieldtype="nvarchar" alias="Name">Heriberto Connolly (00131677)</infofield>
                <infofield id="1083-27" fieldtype="nvarchar" alias="Name">Kimberlee Cerda (00448183)</infofield>
                <infofield id="1083-28" fieldtype="nvarchar" alias="Name">Fernanda Lemieux (00112725)</infofield>
                <infofield id="1083-29" fieldtype="nvarchar" alias="Name">Angelena Gardiner (00284843)</infofield>
                <infofield id="1083-30" fieldtype="nvarchar" alias="Name">Cherri Mccartney (00016952)</infofield>
                <infofield id="1083-31" fieldtype="nvarchar" alias="Name">Shirleen Basham (00780591)</infofield>
                <infofield id="1083-32" fieldtype="nvarchar" alias="Name">Claudie Clifford (00987459)</infofield>
                <infofield id="1083-33" fieldtype="nvarchar" alias="Name">Deane Farias (00492379)</infofield>
                <infofield id="1083-34" fieldtype="nvarchar" alias="Name">Hayley Power (00440645)</infofield>
                <infofield id="1083-35" fieldtype="nvarchar" alias="Name">Marquerite Vu (00497182)</infofield>
                <infofield id="1083-36" fieldtype="nvarchar" alias="Name">Winnifred Singer (00077409)</infofield>
                <infofield id="1083-37" fieldtype="nvarchar" alias="Name">Elene Beltran (00259541)</infofield>
                <infofield id="1083-38" fieldtype="nvarchar" alias="Name">Tristan Ibarra (00678266)</infofield>
                <infofield id="1083-39" fieldtype="nvarchar" alias="Name">Edgardo Farrow (00012773)</infofield>
                <infofield id="1083-40" fieldtype="nvarchar" alias="Name">Tanesha Ruff (00828188)</infofield>
                <infofield id="1083-41" fieldtype="nvarchar" alias="Name">Carlie Conroy (00517419)</infofield>
                <infofield id="1083-42" fieldtype="nvarchar" alias="Name">Iesha Bohannon (00743510)</infofield>
                <infofield id="1083-43" fieldtype="nvarchar" alias="Name">Eulah Duggan (00869762)</infofield>
                <infofield id="1083-44" fieldtype="nvarchar" alias="Name">Lien Mccain (00844931)</infofield>
                <infofield id="1083-45" fieldtype="nvarchar" alias="Name">Emeline Hollins (00790721)</infofield>
                <infofield id="1083-46" fieldtype="nvarchar" alias="Name">Candyce Guest (00915353)</infofield>
                <infofield id="1083-47" fieldtype="nvarchar" alias="Name">Norberto Orellana (00384467)</infofield>
                <infofield id="1083-48" fieldtype="nvarchar" alias="Name">Rich Cormier (00444576)</infofield>
                <infofield id="1083-49" fieldtype="nvarchar" alias="Name">Flo Steiner (00247871)</infofield>
                <infofield id="1083-50" fieldtype="nvarchar" alias="Name">Wynona Hickey (00000019)</infofield>
                <infofield id="1083-51" fieldtype="nvarchar" alias="Name">Mikki Bostic (00894879)</infofield>
                <infofield id="1083-52" fieldtype="nvarchar" alias="Name">Roxana Mobley (00331246)</infofield>
                <infofield id="1083-53" fieldtype="nvarchar" alias="Name">January Esposito (00223322)</infofield>
                <infofield id="1083-54" fieldtype="nvarchar" alias="Name">Stacey Frazer (00663333)</infofield>
                <infofield id="1083-55" fieldtype="nvarchar" alias="Name">Jeri Ratcliff (00148310)</infofield>
                <infofield id="1083-56" fieldtype="nvarchar" alias="Name">Jeffrey Canfield (00300992)</infofield>
                <infofield id="1083-57" fieldtype="nvarchar" alias="Name">Saundra Medley (00915172)</infofield>
                <infofield id="1083-58" fieldtype="nvarchar" alias="Name">Kathaleen Barajas (00210614)</infofield>
                <infofield id="1083-59" fieldtype="nvarchar" alias="Name">Jacinda Streeter (00666049)</infofield>
                <infofield id="1083-60" fieldtype="nvarchar" alias="Name">Salina Clemens (00130302)</infofield>
                <infofield id="1083-61" fieldtype="nvarchar" alias="Name">Sharilyn Broyles (00877310)</infofield>
                <infofield id="1083-62" fieldtype="nvarchar" alias="Name">Shayla Lovejoy (00120621)</infofield>
                <infofield id="1083-63" fieldtype="nvarchar" alias="Name">Lieselotte Hamrick (00779370)</infofield>
                <infofield id="1083-64" fieldtype="nvarchar" alias="Name">Valery Falcon (00302105)</infofield>
                <infofield id="1083-65" fieldtype="nvarchar" alias="Name">Nannette Grooms (00453493)</infofield>
                <infofield id="1083-66" fieldtype="nvarchar" alias="Name">Yasmin Beale (00256216)</infofield>
                <infofield id="1083-67" fieldtype="nvarchar" alias="Name">Candelaria Loomis (00097753)</infofield>
                <infofield id="1083-68" fieldtype="nvarchar" alias="Name">Renda Ison (00060126)</infofield>
                <infofield id="1083-69" fieldtype="nvarchar" alias="Name">Elenore Mcfadden (00091780)</infofield>
                <infofield id="1083-70" fieldtype="nvarchar" alias="Name">Fanny Gaylord (00207529)</infofield>
                <infofield id="1083-71" fieldtype="nvarchar" alias="Name">Geri Mcewen (00448572)</infofield>
                <infofield id="1083-72" fieldtype="nvarchar" alias="Name">Talia Boland (00561058)</infofield>
                <infofield id="1083-73" fieldtype="nvarchar" alias="Name">Bethann Marion (00629589)</infofield>
                <infofield id="1083-74" fieldtype="nvarchar" alias="Name">Cristin Juarez (00814284)</infofield>
                <infofield id="1083-75" fieldtype="nvarchar" alias="Name">Rochel Armenta (00387304)</infofield>
                <infofield id="1083-76" fieldtype="nvarchar" alias="Name">Normand Enriquez (00998525)</infofield>
                <infofield id="1083-77" fieldtype="nvarchar" alias="Name">Chuck Hendricks (00350716)</infofield>
                <infofield id="1083-78" fieldtype="nvarchar" alias="Name">Yessenia Goodrich (00123319)</infofield>
                <infofield id="1083-79" fieldtype="nvarchar" alias="Name">Classie Bourgeois (00434790)</infofield>
                <infofield id="1083-80" fieldtype="nvarchar" alias="Name">Mia Romano (00775832)</infofield>
                <infofield id="1083-81" fieldtype="nvarchar" alias="Name">Holley Gruber (00501080)</infofield>
                <infofield id="1083-82" fieldtype="nvarchar" alias="Name">Ta Rowell (00289217)</infofield>
                <infofield id="1083-83" fieldtype="nvarchar" alias="Name">Johnny Scales (00746754)</infofield>
                <infofield id="1083-84" fieldtype="nvarchar" alias="Name">Sonny Mcgraw (00139151)</infofield>
                <infofield id="1083-85" fieldtype="nvarchar" alias="Name">Yolando Ferrara (00617172)</infofield>
                <infofield id="1083-86" fieldtype="nvarchar" alias="Name">Marlo Chong (00587744)</infofield>
                <infofield id="1083-87" fieldtype="nvarchar" alias="Name">Ninfa Frye (00092739)</infofield>
                <infofield id="1083-88" fieldtype="nvarchar" alias="Name">Treasa Furr (00147203)</infofield>
                <infofield id="1083-89" fieldtype="nvarchar" alias="Name">Wilton Creel (00837449)</infofield>
                <infofield id="1083-90" fieldtype="nvarchar" alias="Name">Mee Gregg (00017048)</infofield>
                <infofield id="1083-91" fieldtype="nvarchar" alias="Name">Ria Gale (00895127)</infofield>
                <infofield id="1083-92" fieldtype="nvarchar" alias="Name">Ayana Fernandes (00036656)</infofield>
                <infofield id="1083-93" fieldtype="nvarchar" alias="Name">Allena Royer (00970156)</infofield>
                <infofield id="1083-94" fieldtype="nvarchar" alias="Name">Norine Couture (00188503)</infofield>
                <infofield id="1083-95" fieldtype="nvarchar" alias="Name">Gia Kimbrell (00606634)</infofield>
                <infofield id="1083-96" fieldtype="nvarchar" alias="Name">Elinore Medrano (00008558)</infofield>
                <infofield id="1083-97" fieldtype="nvarchar" alias="Name">Shanti Starnes (00362029)</infofield>
                <infofield id="1083-98" fieldtype="nvarchar" alias="Name">Taina Alaniz (00753922)</infofield>
                <infofield id="1083-99" fieldtype="nvarchar" alias="Name">Tera Horn (00719608)</infofield>
            </infoenclosure>
            <infoenclosure layout="ul" title="Life / Associate" classname="infosubblock">
                <infofield id="1083-100" fieldtype="nvarchar" alias="Name">James Smith</infofield>
                <infofield id="1083-100" fieldtype="nvarchar" alias="Name">Shanti Couture (00184222)</infofield>
            </infoenclosure>
            <infoenclosure>
                <infofield id="1699-0" fieldtype="int" alias="Download" linkobj="admin/csp/details/csv" imglink="excelicon.gif" linktitle="Download Members Report">172</infofield>
            </infoenclosure>
        </div>
    </data>
</xmlDoc>
"""

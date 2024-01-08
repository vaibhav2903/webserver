## Risk Assessment

In this document, we describe the assessed risk for the web server attacks which we explained in the web server.
These are the following attacks we will assess.

## SQL Injection Vulnerability Assessment
Overall Risk Assessment

Assessment: Critical
Reasoning: SQL Injection can provide unauthorized access to the entire database, leading to data theft, alteration, or deletion.
Likelihood of Exploitation

Assessment: High
Explanation: The simplicity of the exploit (using basic SQL payloads in user input fields) and the prevalence of knowledge about such attacks increase the likelihood.

Impact of Exploitation

Assessment: Critical
Explanation: Successful exploitation can compromise the integrity, confidentiality, and availability of data, and potentially provide administrative database access.
Base CVSS Score

List CWEs: CWE-89 (SQL Injection)
Explanation: Directly relates to the method of exploiting SQL commands through user input fields.
Impact under ASVS

ASVS Requirements Not Met: V5 (Validation, Sanitization, and Encoding), V14 (Configuration)
Explanation: The vulnerability indicates a failure in validating and sanitizing user inputs, and inadequate configuration of database query handling.

## Cross-site Scripting (XSS) Vulnerability Assessment
Overall Risk Assessment

Assessment: High
Reasoning: XSS can lead to unauthorized script execution in user contexts, potentially leading to data theft, session hijacking, and defacement.
Likelihood of Exploitation

Assessment: Medium
Explanation: Requires the attacker to inject a malicious script and a victim to trigger it. Knowledge about XSS is widespread.

Impact of Exploitation

Assessment: High
Explanation: Can lead to loss of user data privacy, unauthorized actions on behalf of the user, and erosion of user trust.

List CWEs: CWE-79 (Cross-site Scripting)
Explanation: Pertains to the vulnerability of executing untrusted scripts in the context of a user’s browser.
Impact under ASVS

ASVS Requirements Not Met: V5 (Validation, Sanitization, and Encoding), V7 (Cross-Site Scripting)
Explanation: Indicates a lack of effective input validation and output encoding to prevent XSS attacks.




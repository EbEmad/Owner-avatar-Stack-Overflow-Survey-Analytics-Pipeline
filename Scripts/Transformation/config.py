relevant_cols = [
    'ResponseId', 'MainBranch', 'Age', 'Employment', 'RemoteWork', 'EdLevel', 'YearsCode', 'YearsCodePro', 
    'DevType', 'OrgSize', 'Country', 'Currency', 'CompTotal', 'LanguageHaveWorkedWith', 
    'DatabaseHaveWorkedWith', 'WebframeHaveWorkedWith', 'WorkExp','MiscTechHaveWorkedWith', 'Industry'
]

cols_to_rename = {
    'MainBranch': 'DeveloperStatus',
    'Age': 'AgeRange',
    'EdLevel': 'EducationLevel',
    'YearsCode': 'YearsCoding',
    'YearsCodePro': 'YearsCodingProfessionally',
    'DevType': 'DeveloperType',
    'OrgSize': 'OrganizationSize'
}

cols_with_parentheses = ['EducationLevel', 'RemoteWork']

dev_cols = ['DeveloperStatus', 'AgeRange', 'RemoteWork', 'EducationLevel', 'YearsCoding', 'YearsCodingProfessionally', 'DeveloperType', 'OrganizationSize', 'Country', 'Industry']

technologies = {
    'LanguageHaveWorkedWith': 'Language', 
    'DatabaseHaveWorkedWith': 'Database', 
    'WebframeHaveWorkedWith': 'Web Framework',
    'MiscTechHaveWorkedWith': 'Miscellaneous Technology'
}
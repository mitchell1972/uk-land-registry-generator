"""
UK Land Registry Application Types

This module provides a comprehensive list of application types commonly processed by 
the UK Land Registry (specifically HM Land Registry for England and Wales).
"""

uk_land_registry_applications = {
    "core_application_types": [
        {
            "name": "First Registrations",
            "description": "Involves registering a property or land for the first time with the Land Registry when it has not previously been registered. Common scenarios include new property purchases from unregistered land or voluntary registrations.",
            "forms": ["FR1 (Application for First Registration)"]
        },
        {
            "name": "Transfers of Ownership",
            "description": "Registers the change of ownership for an already registered property (whole or part). Examples include sales, gifts, or inheritance transfers.",
            "forms": ["TR1 (Transfer of Whole of Registered Title)", "TP1 (Transfer of Part of Registered Title)"]
        },
        {
            "name": "Leases and Lease Extensions",
            "description": "Registers new leases or extends existing leases on properties. Includes registration of commercial and residential leases with terms exceeding 7 years.",
            "forms": ["LR1 (Application to Register a Lease)", "LE1 (Application for Extension of Lease)"]
        },
        {
            "name": "Charges/Mortgages",
            "description": "Registers a legal charge (mortgage) against a property title. This includes new mortgages, remortgages, and the discharge of existing mortgages.",
            "forms": ["CH1 (Application to Register a Charge)", "DS1 (Application to Cancel a Charge)"]
        },
        {
            "name": "Restrictions/Notices",
            "description": "Adds or removes restrictions or notices on a title that limit how the property can be dealt with or notify of third-party interests.",
            "forms": ["RX1 (Application to Enter a Restriction)", "UN1 (Application to Cancel/Withdraw a Notice)"]
        },
        {
            "name": "Title Corrections",
            "description": "Corrects errors or updates information on a registered title, ranging from minor details to substantive changes requiring evidence.",
            "forms": ["AP1 (Application to Change the Register)", "FR2 (Application to Fix a Boundary)"]
        }
    ],
    "additional_application_types": [
        {
            "name": "Assents",
            "description": "Transfers property ownership from a deceased owner's estate to beneficiaries according to a will or intestacy rules.",
            "forms": ["AS1 (Assent of Whole of Registered Title)", "AS2 (Assent of Part of Registered Title)"]
        },
        {
            "name": "Cautions Against First Registration",
            "description": "Registers a caution to prevent first registration of unregistered land without notifying the cautioner, protecting a claimed interest.",
            "forms": ["CT1 (Application to Register a Caution Against First Registration)"]
        },
        {
            "name": "Adverse Possession",
            "description": "Claims ownership of land based on continuous occupation without the legal owner's permission for a defined period (typically 10 or 12 years).",
            "forms": ["ADV1 (Application for Registration Based on Adverse Possession)"]
        },
        {
            "name": "Change of Name or Address",
            "description": "Updates the registered name or address of a property owner following marriage, deed poll, or relocation.",
            "forms": ["AP1 (Application to Change the Register)", "ID1 (Evidence of Identity)"]
        },
        {
            "name": "Severance of Joint Tenancy",
            "description": "Converts joint ownership (where property passes automatically to survivors) to tenants in common (where each owner's share passes according to their will).",
            "forms": ["SEV (Form to Sever a Joint Tenancy)", "JO (Statement of Joint Ownership)"]
        },
        {
            "name": "Official Copies and Searches",
            "description": "Requests for official copies of the register or title plan, or searches to reveal pending applications affecting a property.",
            "forms": ["OC1 (Official Copy Application)", "OS1 (Official Search Application)"]
        },
        {
            "name": "Easements and Rights of Way",
            "description": "Registers new rights over land (such as access routes) or modifies existing rights affecting registered properties.",
            "forms": ["AP1 (Application to Change the Register)", "EX1 (Application for Express Grant of Easement)"]
        },
        {
            "name": "Discharge of Restrictive Covenants",
            "description": "Removes or modifies restrictive covenants that limit how land can be used or developed.",
            "forms": ["TP2 (Transfer with Restrictive Covenant)", "RX3 (Application to Cancel a Restriction)"]
        },
        {
            "name": "Death of Proprietor",
            "description": "Registers the death of a property owner and transfers the property to personal representatives or directly to beneficiaries.",
            "forms": ["DJP (Death of Joint Proprietor)", "AP1 (Application to Change the Register)"]
        },
        {
            "name": "Equitable Charges",
            "description": "Registers an equitable charge or interest against a property, often used for securing loans other than mortgages.",
            "forms": ["CH2 (Application to Register an Equitable Charge)"]
        }
    ]
}


def get_application_types():
    """
    Return the complete dictionary of application types.
    
    Returns:
        dict: The complete collection of UK Land Registry application types
    """
    return uk_land_registry_applications


def get_application_type_names():
    """
    Get all application type names.
    
    Returns:
        list: List of all application type names
    """
    app_types = get_application_types()
    return [t["name"] for t in app_types["core_application_types"] + app_types["additional_application_types"]] 
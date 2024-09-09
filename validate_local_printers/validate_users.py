import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def validate_domain(config_data):
    """
    Validate if the domain exists in the system. If the domain does not exist, create it.
    If the domain exists, check if the field 'allowed' is set to True.
    """

    try:
        # Extract domain and other configuration details from config_data
        domain = config_data.get("FRAPPE_SOCKET_URL")

        # Validate if domain exists
        domain_doc = frappe.db.get_value("Allowed Domains", domain, ["name", "allowed"])

        if not domain_doc:
            # If the domain does not exist, create a new one and insert it into the database
            new_domain = frappe.get_doc({
                "doctype": "Allowed Domains",
                "domain": domain,
                "frappe_socket_url": config_data.get("FRAPPE_SOCKET_URL"),
                "login_url": config_data.get("LOGIN_URL"),
                "usr": config_data.get("AUTH_DATA").get("usr"),
                "pwd": config_data.get("AUTH_DATA").get("pwd"),
                "api_key": config_data.get("API_KEY"),
                "api_secret": config_data.get("API_SECRET"),
                "wkhtmltopdf": config_data.get("WKHTMLTOPDF"),
                "letterhead_image": config_data.get("LETTERHEAD_IMAGE"),
                "sumatra_pdf_path": config_data.get("SUMATRA_PDF_PATH"),
                "allowed": 1  # Set allowed as True by default
            })
            new_domain.insert(ignore_permissions=True)
            frappe.db.commit()
            
            return {"status": "valid", "message": f"Domain '{domain}' created successfully."}
        
        else:
            # If the domain exists and is allowed
            if domain_doc[1]:
                try:
                    # Fetch the existing document for the domain
                    existing_domain_doc = frappe.get_doc("Allowed Domains", domain_doc[0])

                    # Update the fields with new values from config_data
                    existing_domain_doc.update({
                        "frappe_socket_url": config_data.get("FRAPPE_SOCKET_URL"),
                        "login_url": config_data.get("LOGIN_URL"),
                        "usr": config_data.get("AUTH_DATA").get("usr"),
                        "pwd": config_data.get("AUTH_DATA").get("pwd"),
                        "api_key": config_data.get("API_KEY"),
                        "api_secret": config_data.get("API_SECRET"),
                        "wkhtmltopdf": config_data.get("WKHTMLTOPDF"),
                        "letterhead_image": config_data.get("LETTERHEAD_IMAGE"),
                        "sumatra_pdf_path": config_data.get("SUMATRA_PDF_PATH"),
                    })

                    # Save the updated document
                    existing_domain_doc.save(ignore_permissions=True)
                    frappe.db.commit()

                    return {"status": "valid", "message": f"Domain '{domain}' updated successfully."}

                except Exception as e:
                    frappe.log_error(message=str(e), title="Domain Update Error")
                    return {"status": "error", "message": f"Failed to update domain '{domain}': {str(e)}"}
            else:
                # If the domain exists but is not allowed
                return {"status": "invalid", "message": f"Domain '{domain}' exists but is not allowed."}

    
    except Exception as e:
        frappe.log_error(message=str(e), title="Domain Validation Error")
        return {"status": "error", "message": str(e)}

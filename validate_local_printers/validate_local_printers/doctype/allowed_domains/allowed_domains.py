
import frappe
from frappe.model.document import Document

class AllowedDomains(Document):
	def validate(self):
		"""
		Log actions related to the Allowed Domain when it's created or updated.
		"""
		try:
			# Log the action of creating/updating the domain in the Allowed Domain Log doctype
			log_entry = frappe.get_doc({
				"doctype": "Allowed Domain Logs",  # Assuming this is a custom doctype for logging
				"allowed_domain": self.name,  # Link to the Allowed Domain document
				"domain": self.domain,  # Domain name field
				"allowed": self.allowed,  # Whether domain is allowed
				"frappe_socket_url": self.frappe_socket_url,
				"login_url": self.login_url,
				"usr": self.usr,
				"pwd": self.pwd,
				"api_key": self.api_key,
				"api_secret": self.api_secret,
				"wkhtmltopdf": self.wkhtmltopdf,
				"letterhead_image": self.letterhead_image,
				"sumatra_pdf_path": self.sumatra_pdf_path,
				"action": "Created" if self.is_new() else "Updated",  # Action: created or updated
				"created_by": frappe.session.user,  # Log the user who performed the action
				"timestamp": frappe.utils.now()  # Log the current timestamp
			})

			# Insert the log entry and commit the transaction
			log_entry.insert(ignore_permissions=True)
			frappe.db.commit()

		except Exception as e:
			# Log the error if anything goes wrong during the logging
			frappe.log_error(message=str(e), title="Allowed Domain Logging Error")


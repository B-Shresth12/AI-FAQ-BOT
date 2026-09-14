from app.models.document import Document


class KnowlegeLoader:
    def load(self) -> list[Document]:
        return [
            Document(
                id="faq-001",
                title="Password Reset",
                content="""
                To reset your password, open the account settings page.
                Go to the security section and select reset password.
                Enter your current password and your new password.
                Click save to complete the password reset process.
                """,
            ),
            Document(
                id="faq-002",
                title="Contact Support",
                content="""
                If you cannot access your account, contact customer support.
                Support is available Monday through Friday during business hours.
                """,
            ),
        ]

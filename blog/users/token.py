from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.profile.activated)
        )


account_activation_token=AccountActivationToken()
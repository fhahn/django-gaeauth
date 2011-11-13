from google.appengine.api import user_service_pb
from google.appengine.ext import testbed


class GaeUserApiTestMixin(object):
    def login_user(self, email, user_id, is_admin=False):
        self.testbed.setup_env(user_email=email or '', overwrite=True)
        self.testbed.setup_env(user_id=user_id or '', overwrite=True)
        self.testbed.setup_env(user_is_admin='1' if is_admin else '0',
                               overwrite=True)

    def logout_user(self):
        self.login_user(None, None)

    def setUp(self):
        super(GaeUserApiTestMixin, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()

    def tearDown(self):
        super(GaeUserApiTestMixin, self).tearDown()
        self.testbed.deactivate()


class GaeOauthUserApiTestMixin(GaeUserApiTestMixin):
    def login_user(self, email, user_id, is_admin=False):
        self.testbed.setup_env(oauth_error_code='', overwrite=True)
        self.testbed.setup_env(oauth_email=email, overwrite=True)
        self.testbed.setup_env(oauth_user_id=user_id or '', overwrite=True)
        self.testbed.setup_env(oauth_auth_domain='example.com',
                               overwrite=True)
        self.testbed.setup_env(oauth_is_admin='1' if is_admin else '0',
                               overwrite=True)

    def logout_user(self):
        error_code = user_service_pb.UserServiceError.OAUTH_INVALID_REQUEST
        self.testbed.setup_env(oauth_error_code=str(error_code), overwrite=True)

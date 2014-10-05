from frasco import Feature, Service, action, hook, abort, current_app, request, jsonify
import datetime
import base64
import hashlib
import uuid


class AuthenticatedService(Service):
    @hook('before_request')
    def authenticate_before_request(self):
        if not current_app.features.users.logged_in():
            return jsonify({"error": "Request an API key from your account"}), 403


class ApiFeature(Feature):
    name = 'api'
    requires = ['models', 'users']
    defaults = {"default_key_duration": None}

    def init_app(self, app):
        self.model = app.features.models.ensure_model('ApiKey',
            user=app.features.users.model,
            value=str,
            last_accessed_at=datetime.datetime,
            last_accessed_from=str,
            expires_at=datetime.datetime)

        @app.features.users.login_manager.header_loader
        def load_user_from_header(header_val):
            header_val = header_val.replace('Basic ', '', 1)
            try:
                header_val = base64.b64decode(header_val)
                key_value = header_val.split(':')[0]
            except Exception:
                return
            key = app.features.models.find_first('ApiKey', value=key_value)
            if key:
                now = datetime.datetime.utcnow()
                if key.expires_at and key.expires_at < now:
                    return None
                key.last_accessed_at = now
                key.last_accessed_from = request.remote_addr
                key.save()
                return key.user

    @action('create_api_key', default_option='user', as_='api_key')
    def create_key(self, user=None, expires_at=None):
        if not expires_at and self.options['default_key_duration']:
            expires_at = datetime.datetime.now() + datetime.timedelta(
                seconds=self.options['default_key_duration'])
        key = self.model()
        key.value = hashlib.sha1(str(uuid.uuid4)).hexdigest()
        key.user = user or current_app.features.users.current
        key.expires_at = expires_at
        key.save()
        return key
config_map = {
    'routing_prefix': '/api/v1',
    'debug_mode': True,
    'server_port': 5000,
    'mongodb_host': 'mongodb://localhost/koole-poshti',
    'mongodb_name': 'koole-poshti',
    'auth0_domain': 'dev--rjfqqmo.us.auth0.com',
    'api_audience': 'http://localhost:5000/api/v1/terms',
    'algorithms': ["RS256"],
    'jwt_secret_key': 'super_secret_key_for_jwt',
    'password_salt': 'KoOlEpOsHtI_SaLt',
    'tags_location' : "./static/tags/",
    'github_accesstoken': "ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    'semester_since_year' : 1396,
}

# This repo has been private & the Accesstoken is now revoked... So the AT above (also in the history) is not gonna work

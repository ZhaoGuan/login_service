import os

# localhost
# CLIENT_ID = "10e74a20-29ba-4615-a335-b1804ede475a"  # Application (client) ID of app registration
# CLIENT_SECRET = "9Cp7Q~wX2NoigLN16hRFv22UqtZ~4RBWvt7Xf"  # Placeholder - for use ONLY during testing.
# ONLINE
CLIENT_ID = "944461cd-bc1a-426c-9b7f-8ca4e7f518c9"  # Application (client) ID of app registration
CLIENT_SECRET = ".JH7Q~ErE021dOLGTGxMacLnbM.TJHsd-uUmg"  # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")
# tenant id：fd56dea9-97eb-4158-a08b-b11b570ecc07
AUTHORITY = "https://login.microsoftonline.com/fd56dea9-97eb-4158-a08b-b11b570ecc07"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"


REDIRECT_PATH = "/oauth"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadWrite"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session

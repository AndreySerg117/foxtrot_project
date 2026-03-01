from decouple import config

CLOUDFLARE_R2_CONFIG_OPTIONS = {
    "bucket_name": config("CLOUDFLARE_R2_BUCKET"),
    "default_acl": "public-read",  # "private"
    "signature_version": "s3v4",
    "endpoint_url": config("CLOUDFLARE_R2_BUCKET_ENDPOINT"),
    "access_key": config("CLOUDFLARE_R2_ACCESS_KEY"),
    "secret_key": config("CLOUDFLARE_R2_SECRET_KEY"),
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": CLOUDFLARE_R2_CONFIG_OPTIONS,
    },
}

import pyotp

# create OTP 

def generate_otp():
    base32_secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32_secret, interval=300)
    otp = totp.now()
    return otp, base32_secret
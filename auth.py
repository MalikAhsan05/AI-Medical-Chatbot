# ============================================================
# MEDRAG AI - AUTHENTICATION SYSTEM
# ============================================================

import re
import bcrypt

from database import (
    create_user,
    get_user_by_email,
)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def is_valid_email(email):
    """
    Check whether the email address has a valid basic format.
    """

    if not email:
        return False

    email = email.strip()

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


# ============================================================
# PASSWORD VALIDATION
# ============================================================

def validate_password(password):
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """

    if not password:
        return False, "Password is required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    return True, "Password is valid."


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Convert a normal password into a secure bcrypt hash.

    The original password is never stored in the database.
    """

    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(
        password_bytes,
        salt,
    )

    return hashed_password.decode("utf-8")


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(password, password_hash):
    """
    Compare a submitted password with the hash stored
    in the database.
    """

    try:

        password_bytes = password.encode("utf-8")

        hash_bytes = password_hash.encode("utf-8")

        return bcrypt.checkpw(
            password_bytes,
            hash_bytes,
        )

    except (ValueError, TypeError, AttributeError):

        return False


# ============================================================
# REGISTER USER
# ============================================================

def register_user(name, email, password, confirm_password):
    """
    Create a new MedRAG account.

    Returns:
        success: True / False
        message: Explanation
        user: User information when successful
    """

    # --------------------------------------------------------
    # Clean basic input
    # --------------------------------------------------------

    name = name.strip() if name else ""
    email = email.strip().lower() if email else ""


    # --------------------------------------------------------
    # Validate name
    # --------------------------------------------------------

    if not name:

        return (
            False,
            "Full name is required.",
            None,
        )

    if len(name) < 2:

        return (
            False,
            "Please enter a valid full name.",
            None,
        )


    # --------------------------------------------------------
    # Validate email
    # --------------------------------------------------------

    if not email:

        return (
            False,
            "Email address is required.",
            None,
        )

    if not is_valid_email(email):

        return (
            False,
            "Please enter a valid email address.",
            None,
        )


    # --------------------------------------------------------
    # Check duplicate account
    # --------------------------------------------------------

    existing_user = get_user_by_email(email)

    if existing_user:

        return (
            False,
            "An account with this email already exists.",
            None,
        )


    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    password_valid, password_message = (
        validate_password(password)
    )

    if not password_valid:

        return (
            False,
            password_message,
            None,
        )


    # --------------------------------------------------------
    # Confirm passwords match
    # --------------------------------------------------------

    if password != confirm_password:

        return (
            False,
            "Passwords do not match.",
            None,
        )


    # --------------------------------------------------------
    # Hash password
    # --------------------------------------------------------

    password_hash = hash_password(
        password
    )


    # --------------------------------------------------------
    # Store user
    # --------------------------------------------------------

    user_id = create_user(
        name=name,
        email=email,
        password_hash=password_hash,
    )


    if user_id is None:

        return (
            False,
            "Unable to create account. The email may already be registered.",
            None,
        )


    # --------------------------------------------------------
    # Return safe user information
    # --------------------------------------------------------

    user = {
        "id": user_id,
        "name": name,
        "email": email,
    }

    return (
        True,
        "Account created successfully.",
        user,
    )


# ============================================================
# LOGIN USER
# ============================================================

def login_user(email, password):
    """
    Authenticate an existing MedRAG user.

    Returns:
        success: True / False
        message: Explanation
        user: Safe user information if login succeeds
    """

    email = email.strip().lower() if email else ""


    # --------------------------------------------------------
    # Validate fields
    # --------------------------------------------------------

    if not email or not password:

        return (
            False,
            "Email and password are required.",
            None,
        )


    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    database_user = get_user_by_email(
        email
    )


    if database_user is None:

        return (
            False,
            "Invalid email or password.",
            None,
        )


    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    password_correct = verify_password(
        password,
        database_user["password_hash"],
    )


    if not password_correct:

        return (
            False,
            "Invalid email or password.",
            None,
        )


    # --------------------------------------------------------
    # Safe authenticated user object
    # --------------------------------------------------------

    user = {
        "id": database_user["id"],
        "name": database_user["name"],
        "email": database_user["email"],
    }


    return (
        True,
        "Login successful.",
        user,
    )